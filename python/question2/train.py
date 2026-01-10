from ultralytics import YOLO

def main():
    # Load lightweight YOLO model
    model = YOLO("yolov8n.pt")

    # Train on handwritten digit dataset
    model.train(
        data="data.yaml",
        epochs=50,
        imgsz=320,
        batch=8,
        device="cpu"
    )

if __name__ == "__main__":
    main()
