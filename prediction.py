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
import time  # Add this import

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
        # Default class names if not provided
        self.CLASS_NAMES = class_names or [
            "DR", "NORMAL", "MH", "ODC", "TSLN", "ARMD", "DN", "MYA", "BRVO", "ODP",
            "CRVO", "CNV", "RS", "ODE", "LS", "CSR", "HTR", "ASR", "CRS"
        ]
        
        self.MODEL_PATH = model_path
        self.THRESHOLD = threshold
        self.OUTPUT_DIR = output_dir
        
        # Device selection
        self.device = self._select_device()
        
        # Initialize and load the model
        self.model = self._initialize_model()
        
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
        model = CombinedModel(feature_extractor, vit_model, num_classes=19, dropout_rate=0.3)
        
        # Load best model
        try:
            checkpoint = torch.load(self.MODEL_PATH, map_location=self.device)
            model.load_state_dict(checkpoint['model_state_dict'])
            model.to(self.device)
            print("Model loaded successfully!")
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
            os.makedirs(self.OUTPUT_DIR, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(result['image_file']))[0]
            save_path = os.path.join(self.OUTPUT_DIR, f"{base_name}_result.json")
        
        with open(save_path, 'w') as f:
            json.dump(result, f, indent=4)
        print(f"Results saved to {save_path}")
        
    def predict(self, image_path):
        """Main prediction method"""
        print(f"Processing image: {image_path}")
        
        # Add delay before prediction
        time.sleep(5)
        
        # Predict probabilities
        probabilities = self.predict_single_image(image_path)
        
        # Print results
        print("\nPrediction Results:")
        for i, class_name in enumerate(self.CLASS_NAMES):
            print(f"{class_name}: {probabilities[i]:.4f} {'(Detected)' if probabilities[i] > self.THRESHOLD else ''}")
        
        # Create JSON output
        json_result = self.create_json_output(image_path, probabilities)
        print(json_result)
        
        # Save JSON result
        self.save_json_result(json_result)
        
        # Return the JSON result
        return json_result

class CombinedModel(nn.Module):
    def __init__(self, feature_extractor, vit_model, num_classes=19, dropout_rate=0.3):
        super(CombinedModel, self).__init__()

        self.feature_extractor = feature_extractor
        # Add dropout after flattening
        self.dropout1 = nn.Dropout(dropout_rate)
        self.fc = nn.Linear(2208 * 7 * 7, vit_model.config.hidden_size)
        # Add dropout after FC layer
        self.dropout2 = nn.Dropout(dropout_rate)
        self.vit_model = vit_model
        # Add dropout before final classifier
        self.dropout3 = nn.Dropout(dropout_rate)
        self.vit_model.classifier = nn.Linear(vit_model.config.hidden_size, num_classes)

    def forward(self, x):
        features = torch.utils.checkpoint.checkpoint(self.feature_extractor, x, use_reentrant=False)
        flattened_features = features.view(features.size(0), -1)
        # Apply dropout after flattening
        flattened_features = self.dropout1(flattened_features)
        adjusted_features = torch.utils.checkpoint.checkpoint(self.fc, flattened_features, use_reentrant=False)
        # Apply dropout after FC layer
        adjusted_features = self.dropout2(adjusted_features)
        batch_size = adjusted_features.size(0)
        sequence_length = adjusted_features.size(1) // self.vit_model.config.hidden_size
        adjusted_features = adjusted_features.view(batch_size, sequence_length, self.vit_model.config.hidden_size)
        outputs = self.vit_model.vit.encoder(adjusted_features).last_hidden_state
        # Apply dropout before classifier
        outputs_cls = self.dropout3(outputs[:, 0, :])
        outputs = self.vit_model.classifier(outputs_cls)
        return outputs, features  # Return both classification and feature maps

# def main():
#     print("===== Retinal Disease Prediction =====")
    
#     # Path to the model and image
#     MODEL_PATH = "retinal_model_best.pth"
#     INPUT_PATH = "Evaluation_Set\\Validation\\138.png"
    
#     # Create predictor
#     predictor = RetinaDiseasePredictor(
#         model_path=MODEL_PATH, 
#         threshold=0.5, 
#         output_dir="predictions"
#     )
    
#     # Predict
#     predictor.predict(INPUT_PATH)

# if __name__ == "__main__":
#     main()