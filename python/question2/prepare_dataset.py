"""
Dataset Preparation Script for Handwritten Digit Detection

USAGE:
    python prepare_dataset.py
    
    Processes images from 'images/to processed' folder:
    - Images 1-3 → train set
    - Images 4-5 → validation set  
    - Images 6 → test set
    - Applies augmentations (noise, blur, rotate, brightness, contrast)
    - Automatically generates YOLO format labels from filenames
"""

import os
import shutil
import cv2
import numpy as np
from pathlib import Path
import random

try:
    import albumentations as A
    ALBUMENTATIONS_AVAILABLE = True
except ImportError:
    ALBUMENTATIONS_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================
SOURCE_DIR = "images/to processed"
TRAIN_DIR = "images/train"
VAL_DIR = "images/val"
TEST_DIR = "images/test"
LABEL_TRAIN_DIR = "labels/train"
LABEL_VAL_DIR = "labels/val"
LABEL_TEST_DIR = "labels/test"

NUM_AUGMENTATIONS_PER_IMAGE = 2  # Augmentations per image
AUGMENTATION_TYPES = ['noise', 'blur', 'rotate', 'brightness', 'contrast']

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_class_id_from_filename(filename):
    """Extract class ID from filename: 0_1.png → class 0, 4_5.png → class 1, 7_6.png → class 2"""
    if filename.startswith('0_'):
        return 0  # Class 0 = digit "0"
    elif filename.startswith('4_'):
        return 1  # Class 1 = digit "4"
    elif filename.startswith('7_'):
        return 2  # Class 2 = digit "7"
    return None

def get_image_number(filename):
    """Extract image number from filename: 0_1.png → 1, 4_6.png → 6"""
    parts = filename.split('_')
    if len(parts) >= 2:
        try:
            return int(parts[1].split('.')[0])
        except:
            return None
    return None

def detect_digit_region(image):
    """Detect bounding box of digit in image using contour detection"""
    _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Add 10% padding
        h_img, w_img = image.shape
        padding_x = int(w * 0.1)
        padding_y = int(h * 0.1)
        x = max(0, x - padding_x)
        y = max(0, y - padding_y)
        w = min(w_img - x, w + 2 * padding_x)
        h = min(h_img - y, h + 2 * padding_y)
        return x, y, w, h
    
    # Fallback: centered box covering 80% of image
    h_img, w_img = image.shape
    margin = int(w_img * 0.1)
    return margin, margin, w_img - 2*margin, h_img - 2*margin

def create_label_file(image_path, label_dir, image):
    """Create YOLO format label file: class_id center_x center_y width height (all normalized)"""
    filename = os.path.basename(image_path)
    label_path = os.path.join(label_dir, os.path.splitext(filename)[0] + '.txt')
    
    class_id = get_class_id_from_filename(filename)
    if class_id is None:
        return
    
    x, y, w, h = detect_digit_region(image)
    img_h, img_w = image.shape
    
    # Convert to YOLO format (normalized)
    center_x = max(0, min(1, (x + w / 2) / img_w))
    center_y = max(0, min(1, (y + h / 2) / img_h))
    norm_width = max(0, min(1, w / img_w))
    norm_height = max(0, min(1, h / img_h))
    
    with open(label_path, 'w') as f:
        f.write(f"{class_id} {center_x:.6f} {center_y:.6f} {norm_width:.6f} {norm_height:.6f}\n")

def augment_image(image, aug_type):
    """Apply specific augmentation to image"""
    if aug_type == 'noise':
        noise = np.random.normal(0, 0.05 * 255, image.shape).astype(np.uint8)
        return np.clip(cv2.add(image, noise), 0, 255)
    elif aug_type == 'brightness':
        factor = random.uniform(-0.12, 0.12)
        return np.clip(cv2.convertScaleAbs(image, alpha=1, beta=factor * 255), 0, 255)
    elif aug_type == 'contrast':
        factor = random.uniform(-0.12, 0.12)
        return np.clip(cv2.convertScaleAbs(image, alpha=1 + factor, beta=0), 0, 255)
    elif aug_type == 'rotate':
        angle = random.uniform(-8, 8)
        h, w = image.shape[:2]
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        return cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
    elif aug_type == 'blur':
        return cv2.GaussianBlur(image, (3, 3), 0)
    return image

def process_image_set(image_files, output_dir, label_dir, set_name):
    """Process images: save originals and create augmented versions"""
    for img_file in image_files:
        img_path = os.path.join(SOURCE_DIR, img_file)
        img = cv2.imread(img_path)
        
        if img is None:
            continue
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        base_name = os.path.splitext(img_file)[0]
        ext = os.path.splitext(img_file)[1]
        
        # Save original
        output_path = os.path.join(output_dir, img_file)
        cv2.imwrite(output_path, img)
        create_label_file(output_path, label_dir, img)
        
        # Create augmented versions
        for aug_idx in range(NUM_AUGMENTATIONS_PER_IMAGE):
            aug_type = random.choice(AUGMENTATION_TYPES)
            aug_img = augment_image(img.copy(), aug_type)
            aug_filename = f"{base_name}_aug{aug_idx+1}_{aug_type}{ext}"
            aug_path = os.path.join(output_dir, aug_filename)
            cv2.imwrite(aug_path, aug_img)
            create_label_file(aug_path, label_dir, aug_img)

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def main():
    # Create directories
    for dir_path in [TRAIN_DIR, VAL_DIR, TEST_DIR, LABEL_TRAIN_DIR, LABEL_VAL_DIR, LABEL_TEST_DIR]:
        os.makedirs(dir_path, exist_ok=True)
    
    # Clear existing directories
    for dir_path in [TRAIN_DIR, VAL_DIR, TEST_DIR, LABEL_TRAIN_DIR, LABEL_VAL_DIR, LABEL_TEST_DIR]:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            os.makedirs(dir_path, exist_ok=True)
    
    # Get all images
    if not os.path.exists(SOURCE_DIR):
        print(f"Error: Source directory '{SOURCE_DIR}' not found!")
        return
    
    image_files = sorted([f for f in os.listdir(SOURCE_DIR) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    if not image_files:
        print(f"No images found in '{SOURCE_DIR}'")
        return
    
    # Split images: 1-3 train, 4-5 val, 6 test
    train_images = []
    val_images = []
    test_images = []
    
    for img_file in image_files:
        img_num = get_image_number(img_file)
        if img_num is None:
            continue
        if img_num == 6:
            test_images.append(img_file)
        elif img_num in [1, 2, 3]:
            train_images.append(img_file)
        elif img_num in [4, 5]:
            val_images.append(img_file)
    
    print(f"Processing: {len(train_images)} train, {len(val_images)} val, {len(test_images)} test")
    
    # Process each set
    process_image_set(train_images, TRAIN_DIR, LABEL_TRAIN_DIR, "train")
    process_image_set(val_images, VAL_DIR, LABEL_VAL_DIR, "val")
    process_image_set(test_images, TEST_DIR, LABEL_TEST_DIR, "test")
    
    # Summary
    train_count = len([f for f in os.listdir(TRAIN_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    val_count = len([f for f in os.listdir(VAL_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    test_count = len([f for f in os.listdir(TEST_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    print(f"\nDataset ready: {train_count} train, {val_count} val, {test_count} test images")
    print("Labels generated automatically. Class mapping: 0='0', 1='4', 2='7'")

if __name__ == "__main__":
    main()
