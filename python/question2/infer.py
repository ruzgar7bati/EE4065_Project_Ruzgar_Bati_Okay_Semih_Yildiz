from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

def main():
    model = YOLO("runs/detect/train/weights/best.pt")

    image_path = "test_digit.jpg"
    results = model(image_path)

    annotated = results[0].plot()
    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    plt.imshow(annotated)
    plt.title("Detected Handwritten Digits")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
