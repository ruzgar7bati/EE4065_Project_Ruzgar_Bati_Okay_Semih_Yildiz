# Question 2: Handwritten Digit Detection with YOLO - Step-by-Step Guide

## Overview
Implement handwritten digit detection (0-9) using YOLO. Train on PC, deploy inference on ESP32 CAM.

## Step-by-Step Implementation Plan

### Phase 1: Dataset Preparation

#### Step 1.1: Create Handwritten Digit Images
- [ ] Write digits 0-9 multiple times on white paper
- [ ] Use different pens/markers for variety
- [ ] Write digits in different sizes and styles
- [ ] Take photos with good lighting (use phone camera or webcam)
- [ ] Capture at least 50-100 images per digit (total 500-1000 images)
- [ ] Ensure digits are clearly visible and not overlapping

#### Step 1.2: Organize Images
- [ ] Create folder structure:
  ```
  images/
    train/    (70% of images)
    val/      (20% of images)
    test/     (10% of images)
  ```

#### Step 1.3: Annotate Images (Create Labels)
- [ ] Use labeling tool (LabelImg, Roboflow, or CVAT)
- [ ] Draw bounding boxes around each digit in images
- [ ] Label each box with digit class (0, 1, 2, ..., 9)
- [ ] Export annotations in YOLO format:
  - One `.txt` file per image
  - Format: `class_id center_x center_y width height` (normalized 0-1)
  - Example: `5 0.5 0.5 0.2 0.3` means digit "5" at center with 20% width, 30% height

#### Step 1.4: Create Dataset Configuration File
- [ ] Create `data.yaml` with:
  - Paths to train/val/test folders
  - Number of classes (10 for digits 0-9)
  - Class names: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

### Phase 2: Model Training (PC)

#### Step 2.1: Setup Training Environment
- [ ] Install Ultralytics YOLO: `pip install ultralytics`
- [ ] Verify dataset structure is correct
- [ ] Check that images and labels are properly paired

#### Step 2.2: Choose Model Architecture
- [ ] Select lightweight model for ESP32:
  - `yolov8n.pt` (nano - smallest, fastest)
  - `yolov8s.pt` (small - better accuracy)
  - Consider ESP32 memory constraints

#### Step 2.3: Configure Training Parameters
- [ ] Set image size (320x320 or 416x416 for ESP32)
- [ ] Set batch size (8-16 depending on GPU/CPU)
- [ ] Set number of epochs (50-100)
- [ ] Configure data augmentation (optional)

#### Step 2.4: Train Model
- [ ] Run training script
- [ ] Monitor training loss and validation metrics
- [ ] Save best model weights (`best.pt`)

#### Step 2.5: Evaluate Model
- [ ] Test on test set
- [ ] Calculate precision, recall, mAP
- [ ] Visualize predictions on test images
- [ ] Verify model detects digits correctly

### Phase 3: Model Optimization for ESP32

#### Step 3.1: Model Conversion
- [ ] Convert PyTorch model to ONNX format
- [ ] Or use TensorFlow Lite for ESP32
- [ ] Quantize model (INT8) to reduce size

#### Step 3.2: Model Size Optimization
- [ ] Check model size (should fit in ESP32 memory)
- [ ] Consider pruning if too large
- [ ] Test inference speed on PC first

#### Step 3.3: Research ESP32 AI Libraries
- [ ] Check STMicroelectronics resources:
  - `https://github.com/STMicroelectronics/stm32ai-modelzoo-services`
  - `https://github.com/STMicroelectronics/stm32ai-modelzoo`
- [ ] Look for ESP32-compatible inference libraries
- [ ] Consider TensorFlow Lite Micro or similar

### Phase 4: ESP32 CAM Implementation

#### Step 4.1: Setup ESP32 Development Environment
- [ ] Install Arduino IDE or PlatformIO
- [ ] Install ESP32 board support
- [ ] Install required libraries (camera, TensorFlow Lite, etc.)

#### Step 4.2: Camera Configuration
- [ ] Configure ESP32 CAM for appropriate resolution
- [ ] Test camera capture and image format
- [ ] Ensure image format matches model input (RGB, grayscale, etc.)

#### Step 4.3: Image Preprocessing
- [ ] Implement image resize to model input size (320x320)
- [ ] Convert image format if needed (RGB to grayscale, etc.)
- [ ] Normalize pixel values (0-255 to 0-1 or -1 to 1)

#### Step 4.4: Model Inference
- [ ] Load model weights into ESP32 memory
- [ ] Implement inference function
- [ ] Process model output (bounding boxes, confidence scores)
- [ ] Apply non-maximum suppression (NMS) to remove duplicate detections

#### Step 4.5: Post-processing
- [ ] Extract bounding box coordinates
- [ ] Map class IDs to digit labels (0-9)
- [ ] Filter detections by confidence threshold
- [ ] Draw bounding boxes on image (optional, for visualization)

#### Step 4.6: Communication with PC
- [ ] Send detection results via Serial
- [ ] Or send annotated image with bounding boxes
- [ ] Format: digit class, coordinates, confidence score

### Phase 5: Testing and Validation

#### Step 5.1: Test on PC First
- [ ] Run inference on PC with same model
- [ ] Test with actual handwritten digit images
- [ ] Verify accuracy matches training results

#### Step 5.2: Test on ESP32
- [ ] Upload code to ESP32 CAM
- [ ] Test with real-time camera feed
- [ ] Compare results with PC implementation
- [ ] Measure inference time and memory usage

#### Step 5.3: Performance Optimization
- [ ] Optimize inference speed if too slow
- [ ] Reduce memory usage if needed
- [ ] Adjust confidence threshold for better results

### Phase 6: Documentation

#### Step 6.1: Document Implementation
- [ ] Document dataset creation process
- [ ] Document training parameters and results
- [ ] Document ESP32 implementation details
- [ ] Include code comments

#### Step 6.2: Prepare Results
- [ ] Capture example detection images
- [ ] Record performance metrics (accuracy, speed, memory)
- [ ] Create comparison between PC and ESP32 results

## Alternative Approaches (Based on Question Requirements)

### Option B: Python-only Implementation (10 points)
- Skip ESP32 implementation
- Run inference on PC only
- Use webcam or image files as input
- Simpler but worth fewer points

### Option C: Pre-trained YOLO Model (10 points)
- Use existing YOLO model that runs on ESP32
- Skip custom training
- Focus on integration and testing
- Worth fewer points but faster to implement

## Key Considerations

1. **Memory Constraints**: ESP32 has limited RAM (~520KB), model must fit
2. **Processing Speed**: Inference should complete in reasonable time (<1 second)
3. **Image Quality**: Camera resolution and lighting affect detection accuracy
4. **Model Size**: Smaller models (YOLOv8n) are better for embedded systems
5. **Quantization**: INT8 quantization reduces model size significantly

## Recommended Tools

- **Labeling**: LabelImg, Roboflow, CVAT
- **Training**: Ultralytics YOLO, PyTorch
- **ESP32**: Arduino IDE, PlatformIO, TensorFlow Lite Micro
- **Testing**: Serial monitor, image capture tools

