# Embedded Image Processing and AI Project

## Overview
This repository contains Python implementations for an embedded vision project.
All algorithms were first validated on PC and designed to be portable to ESP32-CAM.

## Structure
- q1.py: Histogram-based thresholding with a strict pixel limit (ESP32-friendly)
- q3.py: Nearest-neighbor upsampling and downsampling using integer arithmetic
- question2/: Handwritten digit detection and training pipeline (Python-only)

## Notes
- Training is performed on PC. ESP32 deployment is inference-only.
- All image processing algorithms avoid external libraries and floating-point math
  to ensure compatibility with embedded systems.


This ensures unbiased performance assessment.
# Question 2 – Handwritten Digit Detection

## Description
This section implements handwritten digit detection using a YOLO-based model.
Training and inference are performed on PC using Python.

## Workflow
1. Digits are written manually on paper and photographed.
2. Images are annotated with bounding boxes.
3. A lightweight YOLO model is trained using transfer learning.
4. The trained model is evaluated on test images.

## Notes
- Training is not performed on ESP32 due to hardware limitations.
- The ESP32-CAM is intended for inference only.
- This implementation validates the detection pipeline.
## Dataset Split
The dataset was divided into three disjoint subsets:
- Training set: used for learning model parameters
- Validation set: used for model selection and monitoring
- Test set: used only for final evaluation