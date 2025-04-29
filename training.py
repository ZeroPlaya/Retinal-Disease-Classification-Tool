import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import pandas as pd
import numpy as np
from torchvision import transforms, models
from torchvision.transforms import functional as F
from PIL import Image
import cv2
import os
from transformers import ViTForImageClassification, ViTConfig
import random
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tqdm import tqdm
import csv
import warnings
from sklearn.model_selection import train_test_split
from itertools import combinations

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Arguments other than a weight enum or `None` for 'weights' are deprecated")
warnings.filterwarnings("ignore", category=UserWarning, message="torch.utils.checkpoint: the use_reentrant parameter should be passed explicitly")

# Additional Augmentation Classes
class RandomRotate90:
    def __init__(self, p=0.5):
        self.p = p

    def __call__(self, img):
        if random.random() < self.p:
            return F.rotate(img, angle=random.choice([0, 90, 180, 270]))
        return img

class RandomRotate:
    def __init__(self, limit=30, p=0.5):
        self.limit = limit
        self.p = p

    def __call__(self, img):
        if random.random() < self.p:
            angle = random.uniform(-self.limit, self.limit)
            return F.rotate(img, angle=angle)
        return img

class AddGaussianNoise:
    def __init__(self, var_limit=0.1, p=0.5):
        self.var_limit = var_limit
        self.p = p

    def __call__(self, img):
        if random.random() < self.p:
            np_img = np.array(img)
            noise = np.random.randn(*np_img.shape) * self.var_limit * 255
            noisy_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
            return Image.fromarray(noisy_img)
        return img

class MedianBlur:
    def __init__(self, kernel_size=3, p=0.5):
        self.kernel_size = kernel_size
        self.p = p

    def __call__(self, img):
        if random.random() < self.p:
            np_img = np.array(img)
            blurred_img = cv2.medianBlur(np_img, self.kernel_size)
            return Image.fromarray(blurred_img)
        return img

class RandomErasingPIL:
    def __init__(self, p=0.5, scale=(0.02, 0.2), ratio=(0.3, 3.3), value=0):
        self.p = p
        self.scale = scale
        self.ratio = ratio
        self.value = value

    def __call__(self, img):
        if random.uniform(0, 1) > self.p:
            return img

        img_w, img_h = img.size
        area = img_w * img_h

        for _ in range(10):
            target_area = random.uniform(*self.scale) * area
            aspect_ratio = random.uniform(*self.ratio)

            h = int(round((target_area * aspect_ratio) ** 0.5))
            w = int(round((target_area / aspect_ratio) ** 0.5))

            if w < img_w and h < img_h:
                x1 = random.randint(0, img_w - w)
                y1 = random.randint(0, img_h - h)

                img_np = np.array(img)
                img_np[y1:y1 + h, x1:x1 + w] = self.value
                return Image.fromarray(img_np)

        return img

def extract_fov(image):
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

# Dataset Class
class RetinalDataset(Dataset):
    def __init__(self, csv_file, image_dir, transform=None, augment_counts=None):
        self.data = pd.read_csv(csv_file)
        self.image_dir = image_dir
        self.transform = transform
        self.augment_counts = augment_counts or {}
        self.data.iloc[:, 1:20] = self.data.iloc[:, 1:20].apply(pd.to_numeric, errors='coerce', axis=1)
        self.data = self.data.iloc[:, :20]
        self.augmented_data = self._augment_data()
        self.normalize = transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))

    def _augment_data(self):
        augmented_data = []
        for idx in range(len(self.data)):
            row = self.data.iloc[idx]
            img_name = row[0]
            label = row[1:].values.astype(np.float32)
            label_str = ' '.join([self.data.columns[i+1] for i, val in enumerate(label) if val == 1])
            count = self.augment_counts.get(label_str, 0)
            augmented_data.append((img_name, label))
            if count > 0:
                for _ in range(count):
                    augmented_data.append((img_name, label))
        return augmented_data

    def __len__(self):
        return len(self.augmented_data)

    def __getitem__(self, idx):
        img_name, label = self.augmented_data[idx]  # Use augmented_data instead of self.data

        # Check if img_name already has an extension
        if img_name.lower().endswith(('.tif', '.png', '.jpg', '.jpeg')):
            # If yes, use as-is
            img_path = os.path.join(self.image_dir, img_name)
        else:
            # Otherwise, try different extensions
            extensions = ['.tif', '.png', '.jpg', '.jpeg']
            for ext in extensions:
                potential_path = os.path.join(self.image_dir, img_name + ext)
                if os.path.exists(potential_path):
                    img_path = potential_path
                    break
            else:  # This runs if no break occurred
                raise FileNotFoundError(f"Image not found: {img_name} (tried extensions: {extensions} in {self.image_dir})")

        # Load image and extract FOV
        image = Image.open(img_path).convert("RGB")
        fov_image, mask = extract_fov(image)

        # Apply transformations without normalization
        if self.transform:
            # Split transform into pre-normalization and normalization parts
            if isinstance(self.transform, transforms.Compose):
                # Apply all transforms except normalization
                pre_norm_transforms = [t for t in self.transform.transforms
                                      if not isinstance(t, transforms.Normalize)]
                pre_norm_transform = transforms.Compose(pre_norm_transforms)
                transformed_image = pre_norm_transform(fov_image)
            else:
                transformed_image = self.transform(fov_image)

            # If transformed_image is a tensor, convert back to PIL for masking
            if isinstance(transformed_image, torch.Tensor):
                transformed_image = transforms.ToPILImage()(transformed_image)

            # Convert to numpy for masking
            np_image = np.array(transformed_image)

            # Resize mask to match transformed image dimensions
            mask_resized = cv2.resize(mask, (np_image.shape[1], np_image.shape[0]))

            # Apply mask
            if len(np_image.shape) == 3 and np_image.shape[2] == 3:  # RGB image
                # Make sure mask is 3-channel for RGB image
                if len(mask_resized.shape) == 2:  # If mask is single channel
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
        else:
            # If no transform, just convert to tensor and normalize
            masked_tensor = transforms.ToTensor()(np.array(fov_image))
            normalized_tensor = self.normalize(masked_tensor)

        return normalized_tensor, label, img_path

# Load augmentation counts from disease_counts.csv
def load_augmentation_counts(file_path, target_count=20):
    augment_counts = {}
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            disease_combo = row['Disease Combination']
            count = int(row['Count'])
            if count < target_count:
                augment_counts[disease_combo] = target_count - count
    return augment_counts

# Replace the current dataset split code with this stratified split implementation
def create_stratified_split(dataset, train_ratio=0.8, random_state=42):
    """
    Creates a stratified split for multi-label data, preserving the distribution
    of each class and their combinations in both training and validation sets.

    Args:
        dataset: RetinalDataset object
        train_ratio: Fraction of data to use for training
        random_state: Random seed for reproducibility

    Returns:
        train_indices, val_indices: Indices for train and validation splits
    """
    # Extract all labels from the dataset
    all_labels = []
    for idx in range(len(dataset.data)):
        label = dataset.data.iloc[idx, 1:20].values.astype(np.float32)
        all_labels.append(label)

    all_labels = np.array(all_labels)
    n_samples = len(all_labels)

    # Create a stratification key based on label combinations
    # We'll create a string representation of each sample's label combination
    stratify_keys = []
    for label_vec in all_labels:
        # Get indices of positive labels
        pos_indices = np.where(label_vec == 1)[0]
        # Create a string key like "0_5_9" for a sample with labels 0, 5, and 9 positive
        key = "_".join([str(idx) for idx in pos_indices])
        if not key:  # Handle case with no positive labels
            key = "none"
        stratify_keys.append(key)

    # Count occurrences of each key
    from collections import Counter
    key_counts = Counter(stratify_keys)
    print(f"Label combination distribution: {key_counts}")

    # For combinations with very few samples, we need to handle them separately
    # to avoid stratification errors when some classes have very few samples
    rare_keys = {k for k, v in key_counts.items() if v < 5}
    if rare_keys:
        print(f"Found {len(rare_keys)} rare label combinations that will be handled separately")

    # Get indices for each key type
    common_indices = [i for i, k in enumerate(stratify_keys) if k not in rare_keys]
    rare_indices = [i for i, k in enumerate(stratify_keys) if k in rare_keys]

    # Split common keys with stratification
    if common_indices:
        common_keys = [stratify_keys[i] for i in common_indices]
        common_train_idx, common_val_idx = train_test_split(
            common_indices,
            train_size=train_ratio,
            random_state=random_state,
            stratify=common_keys
        )
    else:
        common_train_idx, common_val_idx = [], []

    # Split rare keys randomly (can't stratify effectively)
    if rare_indices:
        rare_train_idx, rare_val_idx = train_test_split(
            rare_indices,
            train_size=train_ratio,
            random_state=random_state
        )
    else:
        rare_train_idx, rare_val_idx = [], []

    # Combine indices
    train_indices = common_train_idx + rare_train_idx
    val_indices = common_val_idx + rare_val_idx

    # Verify class distribution in splits
    train_labels = all_labels[train_indices].sum(axis=0)
    val_labels = all_labels[val_indices].sum(axis=0)

    print("Class distribution in splits:")
    for i in range(all_labels.shape[1]):
        total = train_labels[i] + val_labels[i]
        train_pct = (train_labels[i] / total * 100) if total > 0 else 0
        val_pct = (val_labels[i] / total * 100) if total > 0 else 0
        print(f"Class {i}: Total={int(total)}, Train={int(train_labels[i])} ({train_pct:.1f}%), Val={int(val_labels[i])} ({val_pct:.1f}%)")

    return train_indices, val_indices

# Image Transformations
train_transforms = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.5),
    RandomRotate90(p=0.5),
    RandomRotate(limit=30, p=0.5),
    transforms.RandomApply([transforms.Lambda(lambda img: MedianBlur(kernel_size=1)(img))], p=0.3),
    AddGaussianNoise(var_limit=0.05, p=0.5),
    transforms.ColorJitter(hue=0.1, saturation=0.1, brightness=0.1, contrast=0.1),
    # transforms.RandomApply([transforms.ColorJitter(brightness=0.05, contrast=0.05)], p=0.2),
    RandomErasingPIL(p=0.3, scale=(0.01, 0.01), ratio=(1.0, 1.0), value=0),
    transforms.Resize((448, 448)),
    transforms.ToTensor()
    # transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
])

val_transforms = transforms.Compose([
    transforms.Resize((448, 448)),
    transforms.ToTensor()
    # transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
])

# File paths for training and validation datasets
train_csv_file = "/content/drive/MyDrive/Colab Notebooks/images/NO_train_data.csv"
val_csv_file = "/content/drive/MyDrive/Colab Notebooks/images/NO_val_data.csv"
full_csv_file = "/content/drive/MyDrive/Colab Notebooks/images/NO_combined.csv"
image_dir = "/content/drive/MyDrive/Colab Notebooks/images/final_images"
disease_counts_file = "/content/drive/MyDrive/Colab Notebooks/images/combined_disease_count.csv"

# Load augmentation counts (only apply to training data)
augment_counts = load_augmentation_counts(disease_counts_file)

# # Create separate datasets for training and validation
# train_dataset = RetinalDataset(train_csv_file, image_dir, transform=train_transforms, augment_counts=augment_counts)
# val_dataset = RetinalDataset(val_csv_file, image_dir, transform=val_transforms)

# # Print dataset information
# print(f"Augmentation counts: {augment_counts}")
# print(f"Training dataset size: {len(train_dataset)}")
# print(f"Validation dataset size: {len(val_dataset)}")

# Replace your dataset creation code with this:
print("Creating stratified datasets for multi-label classification")
seed = 42
torch.manual_seed(seed)

# First create the full dataset without augmentations
full_dataset = RetinalDataset(full_csv_file, image_dir, transform=val_transforms, augment_counts=augment_counts)

# Get stratified split indices
train_indices, val_indices = create_stratified_split(full_dataset, train_ratio=0.8, random_state=seed)

# Now create the training dataset with augmentations
train_full = RetinalDataset(full_csv_file, image_dir, transform=train_transforms)
# And the validation dataset without augmentations
val_full = RetinalDataset(full_csv_file, image_dir, transform=val_transforms)

# Create subset datasets for training and validation
train_dataset = torch.utils.data.Subset(train_full, train_indices)
val_dataset = torch.utils.data.Subset(val_full, val_indices)

# Create subset datasets using the indices
train_dataset = torch.utils.data.Subset(train_full, train_indices)
val_dataset = torch.utils.data.Subset(val_full, val_indices)

print(f"Training dataset size: {len(train_dataset)}")
print(f"Validation dataset size: {len(val_dataset)}")

# Create data loaders
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=1, shuffle=False)  # No need to shuffle validation data

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

# Load Models
device = torch.device("cuda" if torch.cuda.is_available() else
          "xpu" if hasattr(torch, "xpu") and torch.xpu.is_available() else "cpu")
print(f"Using device: {device}")
densenet_model = models.densenet161(weights=False)
feature_extractor = nn.Sequential(*list(densenet_model.children())[:-1])  # Remove final layer

config = ViTConfig()
config.num_labels = 19
vit_model = ViTForImageClassification(config)
vit_model.head = nn.Identity()

# Create Combined Model
model = CombinedModel(feature_extractor, vit_model, num_classes=19)
model.to(device)

# Loss and Optimizer
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

# Initialize variables for training
start_epoch = 0
checkpoint_path = "/content/drive/MyDrive/Colab Notebooks/NO_retinal_model.pth"
best_model_path = "/content/drive/MyDrive/Colab Notebooks/NO_retinal_model_best.pth"

# Early stopping parameters
patience = 5
best_val_loss = float('inf')
best_train_loss = float('inf')
best_val_f1 = float('-inf')
best_train_f1 = float('-inf')
early_stop_counter = 0

# History tracking
history = {
    'train_loss': [], 'train_accuracy': [], 'train_precision': [], 'train_recall': [], 'train_f1': [],
    'val_loss': [], 'val_accuracy': [], 'val_precision': [], 'val_recall': [], 'val_f1': []
}

# Initial checkpoint loading
if os.path.exists(checkpoint_path):
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    start_epoch = checkpoint['epoch'] + 1
    if 'best_val_f1' in checkpoint:
        best_val_f1 = checkpoint['best_val_f1']
    if 'best_train_f1' in checkpoint:
        best_train_f1 = checkpoint['best_train_f1']
    if 'history' in checkpoint:
        history = checkpoint['history']
    print(f"Checkpoint loaded. Resuming training from epoch {start_epoch} best val f1: {best_val_f1:.4f}")

# Training Loop
num_epochs = 200

for epoch in range(start_epoch, num_epochs):
    # Training phase
    model.train()
    running_loss = 0.0
    all_labels = []
    all_preds = []

    print(f"Epoch {epoch+1}/{num_epochs}")
    for images, labels, _ in tqdm(train_loader, desc="Training", unit="batch"):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs, _ = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        preds = torch.sigmoid(outputs).detach().cpu().numpy()
        all_labels.extend(labels.cpu().numpy())
        all_preds.extend(preds)

    train_loss = running_loss / len(train_loader)
    all_labels = np.array(all_labels)
    all_preds = np.array(all_preds) > 0.5

    train_accuracy = accuracy_score(all_labels, all_preds)
    train_precision = precision_score(all_labels, all_preds, average='macro', zero_division=0)
    train_recall = recall_score(all_labels, all_preds, average='macro', zero_division=0)
    train_f1 = f1_score(all_labels, all_preds, average='macro', zero_division=0)

    # Track training metrics
    history['train_loss'].append(train_loss)
    history['train_accuracy'].append(train_accuracy)
    history['train_precision'].append(train_precision)
    history['train_recall'].append(train_recall)
    history['train_f1'].append(train_f1)

    print(f"Epoch [{epoch+1}], Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}, Train Precision Score: {train_precision:.4f}, Train Recall Score: {train_recall:.4f}, Train F1 Score: {train_f1:.4f}")

    # Evaluation phase
    model.eval()
    val_running_loss = 0.0
    val_all_labels = []
    val_all_preds = []

    with torch.no_grad():
        for images, labels, _ in tqdm(val_loader, desc="Validation", unit="batch"):
            images, labels = images.to(device), labels.to(device)

            outputs, _ = model(images)
            loss = criterion(outputs, labels)

            val_running_loss += loss.item()
            preds = torch.sigmoid(outputs).cpu().numpy()
            val_all_labels.extend(labels.cpu().numpy())
            val_all_preds.extend(preds)

    val_loss = val_running_loss / len(val_loader)
    val_all_labels = np.array(val_all_labels)
    val_all_preds = np.array(val_all_preds) > 0.5

    val_accuracy = accuracy_score(val_all_labels, val_all_preds)
    val_precision = precision_score(val_all_labels, val_all_preds, average='macro', zero_division=0)
    val_recall = recall_score(val_all_labels, val_all_preds, average='macro', zero_division=0)
    val_f1 = f1_score(val_all_labels, val_all_preds, average='macro', zero_division=0)

    # Track validation metrics
    history['val_loss'].append(val_loss)
    history['val_accuracy'].append(val_accuracy)
    history['val_precision'].append(val_precision)
    history['val_recall'].append(val_recall)
    history['val_f1'].append(val_f1)

    print(f"Epoch [{epoch+1}], Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.4f}, Val Precision Score: {val_precision:.4f}, Val Recall Score: {val_recall:.4f}, Val F1 Score: {val_f1:.4f}")

    # Early stopping and checkpoint logic
    if best_val_f1 < val_f1:
        # New best model found
        best_val_f1 = val_f1
        best_train_f1 = train_f1
        print(f"New best model saved with Validation F1 Score: {best_val_f1:.4f}  Training F1 Score: {best_train_f1:.4f}")

        # Save best model
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'best_train_f1': best_train_f1,
            'best_val_f1': best_val_f1,
            'history': history
        }, best_model_path)

        early_stop_counter = 0
    # else:
    #     early_stop_counter += 1
    #     print("Validation F1 didn't improve.")
    #     if early_stop_counter >= patience:
    #         print(f"Early stopping triggered after {patience} epochs without improvement")
    #         break  # Exit the training loop

    # Save regular checkpoint
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'best_train_f1': best_train_f1,
        'best_val_f1': best_val_f1,
        'history': history
    }, checkpoint_path)
    print("Checkpoint saved successfully!")