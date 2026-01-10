from ultralytics import YOLO
import glob

def main():
    model = YOLO("runs/detect/train/weights/best.pt")

    test_images = glob.glob("images/test/*.jpg")

    for img_path in test_images:
        results = model(img_path)
        results[0].save(filename=f"results_{img_path.split('/')[-1]}")

if __name__ == "__main__":
    main()
