# Question 2: Handwritten Digit Detection with YOLO

This directory contains scripts for training, inference, and evaluation of a YOLO model for handwritten digit detection.

**Note:** Currently configured for 3 digits (0, 4, 7) to reduce dataset size and model complexity for testing purposes.

## Directory Structure

```
question2/
├── data.yaml          # Dataset configuration
├── train.py          # Training script
├── infer.py          # Inference script
├── evaluate.py       # Evaluation script
├── images/
│   ├── train/        # Training images
│   ├── val/          # Validation images
│   └── test/         # Test images
└── labels/
    ├── train/        # Training labels (YOLO format)
    ├── val/          # Validation labels
    └── test/         # Test labels
```

## Prerequisites

Install required packages:
```bash
pip install ultralytics opencv-python matplotlib
```

**For better augmentations (recommended):**
```bash
pip install albumentations
```

The `prepare_dataset.py` script works with or without `albumentations`, but it's recommended for:
- Better rotation handling (whole image rotation with multiple angles)
- Automatic bounding box updates during augmentation
- More robust augmentation pipeline

## Dataset Preparation

### Step 1: Prepare Raw Images

1. **Create images**: Write digits **0, 4, and 7** on paper and take photos
2. **Place in source folder**: Put all raw images in `images/to processed/`
3. **Naming convention**: Name files as `{digit} {number}.png` (e.g., `0 1.png`, `4 2.png`, `7 6.png`)
   - Images ending with `6.png` will be used as test set (no augmentation)
   - Images 1-5 will be split into train/val with augmentations

### Step 2: Run Dataset Preparation Script

```bash
python prepare_dataset.py
```

This script will:
- ✅ Separate test images (6.png files) - **augmented, but only in test folder**
- ✅ Split remaining images (1-5) into train (80%) and val (20%)
- ✅ Apply augmentations to all images (train/val/test):
  - Noise
  - Brightness adjustment
  - Contrast adjustment
  - Rotation (±10°)
  - Gaussian blur
  - Horizontal flip
- ✅ Create empty label files (`.txt`) for annotation
- ✅ Organize into proper folder structure

**Output structure:**
```
images/
  train/     (original + augmented images)
  val/       (original + augmented images)
  test/      (original + augmented images, never used in train/val)
labels/
  train/     (empty .txt files, ready for annotation)
  val/       (empty .txt files, ready for annotation)
  test/      (empty .txt files, ready for annotation)
```

**Note:** Test images (6.png files) are augmented but kept separate - they are never used in training or validation.

### Step 3: Annotate Images

1. **Use LabelImg**: Download from https://github.com/tzutalin/labelImg
2. **Set format to YOLO**: View → Auto Save mode, format = YOLO
3. **Annotate each image**:
   - Draw bounding box around each digit
   - Select class: 0="0", 1="4", 2="7"
   - Save (creates/updates `.txt` file)

See `ANNOTATION_GUIDE.md` for detailed instructions.

### YOLO Label Format

Each label file should contain one line per detection:
```
class_id center_x center_y width height
```

All coordinates are normalized (0-1). 

**Class IDs for this project:**
- `0` = digit "0"
- `1` = digit "4"
- `2` = digit "7"

Example:
```
1 0.5 0.5 0.2 0.3
```
This means digit "4" (class_id=1) at center (0.5, 0.5) with 20% width and 30% height.

## Usage

### 1. Training

Train the model with default settings:
```bash
python train.py
```

With custom parameters:
```bash
python train.py --model yolov8n.pt --epochs 100 --imgsz 416 --batch 16 --device cuda
```

Options:
- `--model`: YOLO model to use (yolov8n.pt, yolov8s.pt, etc.)
- `--epochs`: Number of training epochs (default: 50)
- `--imgsz`: Image size for training (default: 320)
- `--batch`: Batch size (default: 8)
- `--device`: Device to use - cpu, cuda, or GPU number (default: cpu)

The trained model will be saved to `runs/detect/digit_detection/weights/best.pt`

### 2. Inference

Run inference on a single image:
```bash
python infer.py --source test_digit.jpg
```

Run on multiple images:
```bash
python infer.py --source images/test/*.jpg --save
```

Run on a directory:
```bash
python infer.py --source images/test/ --save --output results
```

Options:
- `--model`: Path to model weights (default: runs/detect/digit_detection/weights/best.pt)
- `--source`: Image path, folder, or pattern
- `--conf`: Confidence threshold 0-1 (default: 0.25)
- `--save`: Save annotated images
- `--output`: Output directory (default: results)
- `--no-show`: Don't display images (for batch processing)

### 3. Evaluation

Evaluate model on test set:
```bash
python evaluate.py
```

With options:
```bash
python evaluate.py --conf 0.3 --save --output evaluation_results
```

Options:
- `--model`: Path to model weights
- `--data`: Path to data.yaml (default: data.yaml)
- `--test-dir`: Test images directory (default: images/test)
- `--conf`: Confidence threshold (default: 0.25)
- `--save`: Save annotated test images
- `--output`: Output directory (default: evaluation_results)

## Example Workflow

1. **Prepare dataset** (images and labels in correct folders)

2. **Train model**:
   ```bash
   python train.py --epochs 50 --device cuda
   ```

3. **Test on single image**:
   ```bash
   python infer.py --source my_digit_image.jpg
   ```

4. **Evaluate on test set**:
   ```bash
   python evaluate.py --save
   ```

## Model Selection

- **yolov8n.pt** (nano): Smallest, fastest, best for ESP32
- **yolov8s.pt** (small): Better accuracy, still relatively fast
- **yolov8m.pt** (medium): Better accuracy, slower
- **yolov8l.pt** (large): High accuracy, slow
- **yolov8x.pt** (xlarge): Highest accuracy, very slow

For ESP32 deployment, use **yolov8n.pt** (nano model).

## Troubleshooting

**Error: data.yaml not found**
- Make sure `data.yaml` exists in the current directory
- Check that paths in data.yaml are correct

**Error: No images found**
- Verify images are in `images/train/`, `images/val/`, `images/test/`
- Check image file extensions (.jpg, .png, etc.)

**Error: Model not found**
- Train the model first using `train.py`
- Or specify correct model path with `--model` option

**Low accuracy**
- Increase number of training epochs
- Add more training images
- Check annotation quality
- Try larger model (yolov8s instead of yolov8n)

