from PIL import Image
import matplotlib.pyplot as plt


def resize_nearest_neighbor(gray, scale_num, scale_den):
    """
    ESP32-friendly nearest neighbor resize using integer arithmetic.

    scale = scale_num / scale_den
    Example:
        1.5  -> scale_num=3, scale_den=2
        2/3  -> scale_num=2, scale_den=3
    """

    input_h = len(gray)
    input_w = len(gray[0])

    # Compute output dimensions using integer math
    output_h = (input_h * scale_num) // scale_den
    output_w = (input_w * scale_num) // scale_den

    # Allocate output image
    output = [[0 for _ in range(output_w)] for _ in range(output_h)]

    # Inverse mapping (nearest neighbor)
    for y in range(output_h):
        for x in range(output_w):
            src_y = (y * scale_den) // scale_num
            src_x = (x * scale_den) // scale_num

            # Clamp to bounds
            if src_y >= input_h:
                src_y = input_h - 1
            if src_x >= input_w:
                src_x = input_w - 1

            output[y][x] = gray[src_y][src_x]

    return output


def image_to_gray_list(image):
    """
    Convert PIL image to grayscale 2D list using integer arithmetic.
    Same logic as ESP32 grayscale conversion.
    """
    width, height = image.size
    pixels = image.load()

    gray = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            gray[y][x] = (30 * r + 59 * g + 11 * b) // 100

    return gray


def visualize(original, upsampled, downsampled):
    """
    Visualization for PC validation only.
    Not part of embedded logic.
    """

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.title("Original")
