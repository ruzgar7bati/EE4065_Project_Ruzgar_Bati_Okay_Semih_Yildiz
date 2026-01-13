"""
YOLO Inference Script for Handwritten Digit Detection
Runs inference on images using trained YOLO model
"""
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os
import argparse
import glob


def visualize_results(results, image_path, save_path=None, show=True):
    """Visualize detection results"""
    annotated = results[0].plot()
    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    
    if save_path:
        cv2.imwrite(save_path, cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
        print(f"Saved result to: {save_path}")
    
    if show:
        plt.figure(figsize=(12, 8))
        plt.imshow(annotated)
        plt.title(f"Detected Handwritten Digits - {os.path.basename(image_path)}")
        plt.axis("off")
        plt.tight_layout()
        plt.show()


def print_detections(results):
    """Print detection results in text format"""
    # Class mapping: 0="0", 1="4", 2="7"
    class_names = {0: '0', 1: '4', 2: '7'}
    
    print("\n" + "=" * 60)
    print("Detection Results:")
    print("=" * 60)
    
    if len(results[0].boxes) == 0:
        print("No digits detected!")
        return
    
    for i, box in enumerate(results[0].boxes):
        # Get class ID and confidence
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        
        # Get digit name from class mapping
        digit_name = class_names.get(class_id, f"Unknown({class_id})")
        
        # Get bounding box coordinates
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        
        print(f"\nDetection {i+1}:")
        print(f"  Digit: {digit_name} (class {class_id})")
        print(f"  Confidence: {confidence:.2%}")
        print(f"  Bounding box: ({x1:.1f}, {y1:.1f}) to ({x2:.1f}, {y2:.1f})")
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Run YOLO inference on images')
    parser.add_argument('--model', type=str, 
                        default='runs/detect/digit_detection/weights/best.pt',
                        help='Path to trained model weights')
    parser.add_argument('--source', type=str, default='test_digit.jpg',
                        help='Image path, folder path, or pattern (e.g., images/test/*.jpg)')
    parser.add_argument('--conf', type=float, default=0.25,
                        help='Confidence threshold (0-1)')
    parser.add_argument('--save', action='store_true',
                        help='Save annotated images')
    parser.add_argument('--output', type=str, default='results',
                        help='Output directory for saved images')
    parser.add_argument('--no-show', action='store_true',
                        help='Do not display images (useful for batch processing)')
    
    args = parser.parse_args()
    
    # Check if model exists
    if not os.path.exists(args.model):
        print(f"Error: Model not found at {args.model}")
        print("\nPlease train the model first using train.py")
        print("Or specify the correct model path with --model")
        return
    
    # Load model
    print(f"Loading model: {args.model}")
    model = YOLO(args.model)
    
    # Create output directory if saving
    if args.save:
        os.makedirs(args.output, exist_ok=True)
    
    # Determine input type
    if os.path.isfile(args.source):
        # Single image
        image_paths = [args.source]
    elif os.path.isdir(args.source):
        # Directory - find all images
        image_paths = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
            image_paths.extend(glob.glob(os.path.join(args.source, ext)))
    else:
        # Pattern (e.g., images/test/*.jpg)
        image_paths = glob.glob(args.source)
    
    if not image_paths:
        print(f"Error: No images found at {args.source}")
        return
    
    print(f"\nFound {len(image_paths)} image(s) to process")
    print("=" * 60)
    
    # Process each image
    for image_path in image_paths:
        print(f"\nProcessing: {os.path.basename(image_path)}")
        
        # Run inference
        results = model(image_path, conf=args.conf)
        
        # Print detection results
        print_detections(results)
        
        # Save or show results
        if args.save:
            save_path = os.path.join(args.output, f"result_{os.path.basename(image_path)}")
            visualize_results(results, image_path, save_path=save_path, show=not args.no_show)
        elif not args.no_show:
            visualize_results(results, image_path, show=True)
    
    print(f"\n{'='*60}")
    print("Inference completed!")
    if args.save:
        print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
