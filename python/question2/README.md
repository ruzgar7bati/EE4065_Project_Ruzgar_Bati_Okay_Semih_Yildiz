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

## Dataset Preparation

1. **Create images**: Write digits **0, 4, and 7** on paper and take photos
2. **Organize images**: Place images in `images/train/`, `images/val/`, and `images/test/`
3. **Annotate images**: Use LabelImg or similar tool to create bounding box annotations
4. **Create labels**: Save annotations in YOLO format (one `.txt` file per image) in `labels/` folders

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

