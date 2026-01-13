"""
YOLO Evaluation Script for Handwritten Digit Detection
Evaluates trained model on test set and calculates metrics
"""
from ultralytics import YOLO
import os
import argparse
import glob


def main():
    parser = argparse.ArgumentParser(description='Evaluate YOLO model on test set')
    parser.add_argument('--model', type=str,
                        default='runs/detect/digit_detection/weights/best.pt',
                        help='Path to trained model weights')
    parser.add_argument('--data', type=str, default='data.yaml',
                        help='Path to data.yaml file')
    parser.add_argument('--test-dir', type=str, default='images/test',
                        help='Directory containing test images')
    parser.add_argument('--conf', type=float, default=0.25,
                        help='Confidence threshold')
    parser.add_argument('--save', action='store_true',
                        help='Save annotated test images')
    parser.add_argument('--output', type=str, default='evaluation_results',
                        help='Output directory for results')
    
    args = parser.parse_args()
    
    # Check if model exists
    if not os.path.exists(args.model):
        print(f"Error: Model not found at {args.model}")
        print("\nPlease train the model first using train.py")
        return
    
    # Check if test directory exists
    if not os.path.exists(args.test_dir):
        print(f"Error: Test directory not found: {args.test_dir}")
        return
    
    print("=" * 60)
    print("YOLO Model Evaluation")
    print("=" * 60)
    print(f"Model: {args.model}")
    print(f"Test directory: {args.test_dir}")
    print(f"Confidence threshold: {args.conf}")
    print("=" * 60)
    
    # Load model
    print(f"\nLoading model...")
    model = YOLO(args.model)
    
    # Find test images
    test_images = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
        test_images.extend(glob.glob(os.path.join(args.test_dir, ext)))
    
    if not test_images:
        print(f"\nNo test images found in {args.test_dir}")
        return
    
    print(f"\nFound {len(test_images)} test images")
    
    # Run validation (if data.yaml is available)
    if os.path.exists(args.data):
        print("\nRunning validation with data.yaml...")
        try:
            metrics = model.val(data=args.data, conf=args.conf)
            
            print("\n" + "=" * 60)
            print("Validation Metrics:")
            print("=" * 60)
            print(f"mAP50: {metrics.box.map50:.4f}")
            print(f"mAP50-95: {metrics.box.map:.4f}")
            print(f"Precision: {metrics.box.mp:.4f}")
            print(f"Recall: {metrics.box.mr:.4f}")
            print("=" * 60)
        except Exception as e:
            print(f"Warning: Could not run validation: {e}")
            print("Continuing with test image inference...")
    
    # Create output directory
    if args.save:
        os.makedirs(args.output, exist_ok=True)
    
    # Process test images
    print(f"\nProcessing test images...")
    total_detections = 0
    images_with_detections = 0
    
    for img_path in test_images:
        results = model(img_path, conf=args.conf)
        
        num_detections = len(results[0].boxes)
        total_detections += num_detections
        if num_detections > 0:
            images_with_detections += 1
        
        if args.save:
            save_path = os.path.join(args.output, f"result_{os.path.basename(img_path)}")
            results[0].save(filename=save_path)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Evaluation Summary:")
    print("=" * 60)
    print(f"Total test images: {len(test_images)}")
    print(f"Images with detections: {images_with_detections}")
    print(f"Total detections: {total_detections}")
    print(f"Average detections per image: {total_detections/len(test_images):.2f}")
    print("=" * 60)
    
    if args.save:
        print(f"\nAnnotated images saved to: {args.output}")


if __name__ == "__main__":
    main()
