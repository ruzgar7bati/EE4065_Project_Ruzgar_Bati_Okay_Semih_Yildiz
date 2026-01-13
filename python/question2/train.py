"""
YOLO Training Script for Handwritten Digit Detection
Trains a YOLO model to detect handwritten digits (0-9)
"""
from ultralytics import YOLO
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description='Train YOLO model for digit detection')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                        help='YOLO model to use (yolov8n.pt, yolov8s.pt, etc.)')
    parser.add_argument('--epochs', type=int, default=50,
                        help='Number of training epochs')
    parser.add_argument('--imgsz', type=int, default=320,
                        help='Image size for training')
    parser.add_argument('--batch', type=int, default=8,
                        help='Batch size')
    parser.add_argument('--device', type=str, default='cpu',
                        help='Device to use (cpu, cuda, 0, 1, etc.)')
    parser.add_argument('--data', type=str, default='data.yaml',
                        help='Path to data.yaml file')
    
    args = parser.parse_args()
    
    # Check if data.yaml exists
    if not os.path.exists(args.data):
        print(f"Error: {args.data} not found!")
        print("Please create data.yaml with dataset configuration.")
        return
    
    print("=" * 60)
    print("YOLO Handwritten Digit Detection - Training")
    print("=" * 60)
    print("Classes: 0, 4, 7 (3 digits)")
    print(f"Model: {args.model}")
    print(f"Epochs: {args.epochs}")
    print(f"Image size: {args.imgsz}")
    print(f"Batch size: {args.batch}")
    print(f"Device: {args.device}")
    print("=" * 60)
    
    # Load YOLO model
    print(f"\nLoading model: {args.model}")
    model = YOLO(args.model)
    
    # Train the model
    print(f"\nStarting training...")
    print("This may take a while. Please be patient.\n")
    
    try:
        results = model.train(
            data=args.data,
            epochs=args.epochs,
            imgsz=args.imgsz,
            batch=args.batch,
            device=args.device,
            project='runs/detect',
            name='digit_detection',
            save=True,
            plots=True
        )
        
        print("\n" + "=" * 60)
        print("Training completed successfully!")
        print("=" * 60)
        print(f"Best model saved to: runs/detect/digit_detection/weights/best.pt")
        print(f"Last model saved to: runs/detect/digit_detection/weights/last.pt")
        print("\nYou can now use the model for inference with infer.py")
        
    except Exception as e:
        print(f"\nError during training: {e}")
        print("\nCommon issues:")
        print("1. Check that images/ and labels/ folders exist")
        print("2. Verify data.yaml paths are correct")
        print("3. Ensure images and labels are properly paired")
        print("4. Check that you have enough disk space")


if __name__ == "__main__":
    main()
