from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path


def rgb_to_grayscale(image):
    """
    Convert RGB image to grayscale using integer arithmetic.
    Formula matches embedded-friendly luminance approximation.
    gray = (30*R + 59*G + 11*B) / 100
    """

    width, height = image.size
    gray = [[0 for _ in range(width)] for _ in range(height)]

    pixels = image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            gray[y][x] = (30 * r + 59 * g + 11 * b) // 100

    return gray


def extract_bright_pixels_histogram(gray, max_pixels=1000):
    """
    ESP32-friendly adaptive thresholding using histogram accumulation.
    Ensures output contains at most 'max_pixels' bright pixels.
    All other pixels are set to 0.
    """

    height = len(gray)
    width = len(gray[0])

    # 1. Build grayscale histogram
    hist = [0] * 256
    for y in range(height):
        for x in range(width):
            hist[gray[y][x]] += 1

    # 2. Find threshold from brightest to darkest
    cumulative = 0
    threshold = 255
    for intensity in range(255, -1, -1):
        cumulative += hist[intensity]
        if cumulative >= max_pixels:
            threshold = intensity
            break

    # 3. Create binary output image
    output = [[0 for _ in range(width)] for _ in range(height)]

    selected = 0
    for y in range(height):
        for x in range(width):
            if gray[y][x] >= threshold and selected < max_pixels:
                output[y][x] = 255
                selected += 1
            else:
                output[y][x] = 0

    return output, threshold


def visualize(gray, binary):
    """
    Visualization for PC validation only.
    Not part of embedded logic.
    """

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.title("Grayscale Image")
    plt.imshow(gray, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Binary Output (≤ 1000 pixels)")
    plt.imshow(binary, cmap="gray")
    plt.axis("off")

    plt.tight_layout()
    plt.show()


def main():
    # Load image (RGB) relative to this script's folder
    base_dir = Path(__file__).resolve().parent
    img_path = base_dir / "question1_images" / "reference_taken_from_phone.jpg"
    image = Image.open(img_path).convert("RGB")

    # For Python testing only: resize to match ESP32 resolution
    # This makes the behavior closer to the 96x96 images used on the board
    target_size = (96, 96)
    image = image.resize(target_size, Image.BILINEAR)

    # Convert to grayscale (ESP32-style)
    gray = rgb_to_grayscale(image)

    # Apply histogram-based thresholding
    binary, threshold = extract_bright_pixels_histogram(
        gray, max_pixels=1000
    )

    print("Selected threshold intensity:", threshold)

    # Visualization (PC only)
    visualize(gray, binary)


if __name__ == "__main__":
    main()
