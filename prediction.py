import torch
import torch.nn as nn
from torch.utils.data import Dataset
from torchvision import transforms, models
from transformers import ViTForImageClassification, ViTConfig
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import os
import json
import time
import warnings
import sys

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Arguments other than a weight enum or `None` for 'weights' are deprecated")
warnings.filterwarnings("ignore", category=UserWarning, message="torch.utils.checkpoint: the use_reentrant parameter should be passed explicitly")

class CombinedModel(nn.Module):
    def __init__(self, feature_extractor, vit_model, num_classes=19):
        super(CombinedModel, self).__init__()

        self.feature_extractor = feature_extractor
        # Use global average pooling instead of flattening to handle variable sizes
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        # Adjust the input size of the linear layer based on feature_extractor output channels
        self.fc = nn.Linear(2208, vit_model.config.hidden_size)  # 2208 is DenseNet161's output channels
        self.vit_model = vit_model
        self.vit_model.classifier = nn.Linear(vit_model.config.hidden_size, num_classes)

    def forward(self, x):
        features = torch.utils.checkpoint.checkpoint(self.feature_extractor, x, use_reentrant=False)
        # Use global pooling to get fixed-size feature regardless of input size
        pooled_features = self.global_pool(features).squeeze(-1).squeeze(-1)
        adjusted_features = torch.utils.checkpoint.checkpoint(self.fc, pooled_features, use_reentrant=False)
        batch_size = adjusted_features.size(0)
        # Reshape for ViT
        adjusted_features = adjusted_features.unsqueeze(1)  # Add sequence dimension
        outputs = self.vit_model.vit.encoder(adjusted_features).last_hidden_state
        outputs = self.vit_model.classifier(outputs[:, 0, :])
        return outputs, features
    
class RetinaDiseasePredictor:
    def __init__(self, 
                 model_path=None, 
                 class_names=None, 
                 threshold=0.5, 
                 output_dir=None):
        """
        Initialize the Retinal Disease Predictor
        
        Args:
            model_path (str): Path to the model checkpoint
            class_names (list): List of disease class names
            threshold (float): Prediction threshold for positive classification
            output_dir (str): Directory to save JSON results
        """
        
        if getattr(sys, 'frozen', False):  # Check if running in a PyInstaller bundle
            base_path = sys._MEIPASS  # Temporary folder created by PyInstaller
        else:
            base_path = os.path.dirname(__file__)

        # Ensure the model path includes the _internal subdirectory
        self.MODEL_PATH = model_path or os.path.join(base_path, "model", "non_augment_retinal_model_.pth")
                
                
        # Default class names if not provided
        self.CLASS_NAMES = class_names or [
            "DR", "NORMAL", "MH", "ODC", "TSLN", "ARMD", "DN", "MYA", "BRVO", "ODP",
            "CRVO", "CNV", "RS", "ODE", "LS", "CSR", "HTR", "ASR", "CRS"
        ]
        
        self.THRESHOLD = threshold
        self.OUTPUT_DIR = output_dir
        
        # Device selection
        self.device = self._select_device()
        
        # Initialize and load the model
        self.model = self._initialize_model()
        print(f"Resolved model path: {self.MODEL_PATH}")
        print(f"Looking for model at: {self.MODEL_PATH}")
        
    def _select_device(self):
        """Select the appropriate device for computation"""
        return torch.device("cuda" if torch.cuda.is_available() else
                           "xpu" if hasattr(torch, "xpu") and torch.xpu.is_available() else "cpu")
    
    def _initialize_model(self):
        """Initialize and load the combined model"""
        # Initialize model components
        densenet_model = models.densenet161(weights=None)
        feature_extractor = nn.Sequential(*list(densenet_model.children())[:-1])
        
        config = ViTConfig()
        config.num_labels = 19
        vit_model = ViTForImageClassification(config)
        vit_model.head = nn.Identity()
        
        # Create combined model
        model = CombinedModel(feature_extractor, vit_model, num_classes=19)
        
        # Load best model
        try:
            checkpoint = torch.load(self.MODEL_PATH, map_location=self.device)
            model.load_state_dict(checkpoint['model_state_dict'])
            model.to(self.device)
            print(f"Model loaded successfully from {self.MODEL_PATH}!")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
        
        return model
    
    def extract_fov(self, image):
        """Extract Field of View from an image"""
        np_img = np.array(image)
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        
        # Apply Otsu thresholding
        _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Use morphological operations to clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Ensure mask is of type uint8
        mask = mask.astype(np.uint8)
        
        # Apply the mask to keep only the FOV
        fov_image = cv2.bitwise_and(np_img, np_img, mask=mask)
        
        return Image.fromarray(fov_image), mask
    
    def predict_single_image(self, image_path):
        """Predict probabilities for a single image"""
        # Create dataset
        dataset = self._create_prediction_dataset(image_path)
        
        # Set model to evaluation mode
        self.model.eval()
        
        # Process image
        with torch.no_grad():
            image_tensor, _ = dataset[0]
            image_tensor = image_tensor.unsqueeze(0).to(self.device)
            outputs, _ = self.model(image_tensor)
            probabilities = torch.sigmoid(outputs).cpu().numpy()[0]
        
        return probabilities
    
    def _create_prediction_dataset(self, image_paths):
        """Create a dataset for prediction"""
        class _RetinalPredictionDataset(Dataset):
            def __init__(self, image_paths, extract_fov_func):
                self.image_paths = image_paths if isinstance(image_paths, list) else [image_paths]
                self.extract_fov = extract_fov_func
                self.transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                ])
                self.normalize = transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))

            def __len__(self):
                return len(self.image_paths)

            def __getitem__(self, idx):
                img_path = self.image_paths[idx]
                
                # Check if the image exists
                if not os.path.exists(img_path):
                    raise FileNotFoundError(f"Image not found: {img_path}")
                
                # Load image and extract FOV
                image = Image.open(img_path).convert("RGB")
                fov_image, mask = self.extract_fov(image)
                
                # Apply transformations
                transformed_image = self.transform(fov_image)
                
                # Convert to PIL for masking
                transformed_pil = transforms.ToPILImage()(transformed_image)
                
                # Convert to numpy for masking
                np_image = np.array(transformed_pil)
                
                # Resize mask to match transformed image dimensions
                mask_resized = cv2.resize(mask, (np_image.shape[1], np_image.shape[0]))
                
                # Make sure mask is 3-channel for RGB image
                if len(mask_resized.shape) == 2:
                    mask_resized = cv2.cvtColor(mask_resized, cv2.COLOR_GRAY2RGB)
                
                # Ensure both arrays have the same type
                np_image = np_image.astype(np.uint8)
                mask_resized = mask_resized.astype(np.uint8)
                
                # Apply mask
                masked_image = cv2.bitwise_and(np_image, mask_resized)
                
                # Convert back to tensor
                masked_tensor = transforms.ToTensor()(masked_image)
                
                # Apply normalization
                normalized_tensor = self.normalize(masked_tensor)
                
                return normalized_tensor, img_path

        return _RetinalPredictionDataset(image_paths, self.extract_fov)
    
    def create_json_output(self, image_path, probabilities):
        """Create JSON output in the specified format"""
        # Get the image filename
        image_file = os.path.basename(image_path)
        
        # Apply threshold to get binary predictions
        predictions = (probabilities > self.THRESHOLD).astype(int)
        
        # Get list of positive classes
        positive_classes = [self.CLASS_NAMES[i] for i in range(len(self.CLASS_NAMES)) if predictions[i] == 1]
        
        # Create the class predictions dictionary
        class_predictions = {}
        for i, class_name in enumerate(self.CLASS_NAMES):
            class_predictions[class_name] = {
                "probability": float(probabilities[i]),
                "prediction": int(predictions[i])
            }
        
        # Create the final JSON structure
        result = {
            "image_file": image_file,
            "positive_classes": positive_classes,
            "class_predictions": class_predictions
        }
        
        return result
    
    def save_json_result(self, result, save_path=None):
        """Save result to JSON file"""
        # If no save path is provided, generate one
        if save_path is None:
            if self.OUTPUT_DIR is None:
                print("Warning: No output directory specified. Results will not be saved.")
                return
            
            os.makedirs(self.OUTPUT_DIR, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(result['image_file']))[0]
            save_path = os.path.join(self.OUTPUT_DIR, f"{base_name}_result.json")
        
        with open(save_path, 'w') as f:
            json.dump(result, f, indent=4)
        print(f"Results saved to {save_path}")
        
    def predict(self, image_path):
        """Main prediction method"""
        print(f"Processing image: {image_path}")
        
        # Predict probabilities
        probabilities = self.predict_single_image(image_path)
        
        # Print results
        print("\nPrediction Results:")
        for i, class_name in enumerate(self.CLASS_NAMES):
            print(f"{class_name}: {probabilities[i]:.4f} {'(Detected)' if probabilities[i] > self.THRESHOLD else ''}")
        
        # Create JSON output
        json_result = self.create_json_output(image_path, probabilities)
        
        # Save JSON result if output directory is specified
        if self.OUTPUT_DIR:
            self.save_json_result(json_result)
        
        # Return the JSON result
        return json_result

    def predict_multiple_images(self, folder_path):
        """Predict probabilities for all images in a folder and save results in separate folders based on results"""
        # Ensure folder path exists
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")
            
        # Get all image paths from the folder
        image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
                      if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tif', 'tiff'))]

        print(f"Found {len(image_paths)} images in folder: {folder_path}")

        # Ensure output directory exists if specified
        if self.OUTPUT_DIR:
            os.makedirs(self.OUTPUT_DIR, exist_ok=True)

        # Set model to evaluation mode
        self.model.eval()
        
        results = []

        # Process each image
        for image_path in image_paths:
            try:
                # Predict probabilities for the image
                probabilities = self.predict_single_image(image_path)

                # Create JSON output
                json_result = self.create_json_output(image_path, probabilities)
                results.append(json_result)

                # If output directory is specified, save results
                if self.OUTPUT_DIR:
                    # Determine folder based on positive classes
                    positive_classes = json_result["positive_classes"]
                    folder_name = "_".join(positive_classes) if positive_classes else "Unclassified"
                    result_folder = os.path.join(self.OUTPUT_DIR, folder_name)
                    os.makedirs(result_folder, exist_ok=True)

                    # Save JSON result in the folder
                    base_name = os.path.splitext(os.path.basename(image_path))[0]
                    save_path = os.path.join(result_folder, f"{base_name}_result.json")
                    self.save_json_result(json_result, save_path)

            except Exception as e:
                print(f"Error processing image {image_path}: {e}")
        
        return results


# # Usage example
# if __name__ == "__main__":
#     # Set up the predictor
#     predictor = RetinaDiseasePredictor(
#         model_path="path/to/best_model.pth",
#         output_dir="./results"
#     )
    
#     # Example single image prediction
#     # result = predictor.predict("path/to/image.jpg")
    
#     # Example folder prediction
#     # results = predictor.predict_multiple_images("path/to/images_folder")