from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path

# ===== Configuration =====
# Input image settings
INPUT_IMAGE_PATH = "question1_images/reference_taken_from_phone.jpg"
TARGET_SIZE = (160, 120)  # Resize input to this size before processing
#Increased from 1.5x to 2.5x for upsampling and 2/3 to 2/5 for downsampling to show more difference
#will not keep this for esp32 implementation
# Resizing scale factors
UPSAMPLE_SCALE_NUM = 5  # For 2.5x upsampling: scale = 5/2
UPSAMPLE_SCALE_DEN = 2
DOWNSAMPLE_SCALE_NUM = 2  # For 2/5 downsampling: scale = 2/5
DOWNSAMPLE_SCALE_DEN = 5

# Output settings
OUTPUT_IMAGE_PATH = "question1_images/q3_comparison.png"
FIGURE_SIZE = (12, 4)  # Figure size in inches (width, height)
FIGURE_DPI = 150  # Resolution for saved figure

# ===== End Configuration =====


def resize_nearest_neighbor(image, scale_num, scale_den):
    """
    ESP32-friendly nearest neighbor resize using integer arithmetic.

    scale = scale_num / scale_den
    Works with RGB images (3 channels).
    """

    input_h = image.height
    input_w = image.width
    pixels = image.load()

    # Compute output dimensions using integer math
    output_h = (input_h * scale_num) // scale_den
    output_w = (input_w * scale_num) // scale_den

    # Create output image
    output = Image.new('RGB', (output_w, output_h))
    output_pixels = output.load()

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

            # Copy RGB pixel
            output_pixels[x, y] = pixels[src_x, src_y]

    return output


def visualize(original, upsampled, downsampled, save_path=None, figsize=(12, 4), dpi=150):
    """
    Visualization for PC validation only.
    Not part of embedded logic.
    """

    # Get dimensions for each image
    orig_w, orig_h = original.size
    up_w, up_h = upsampled.size
    down_w, down_h = downsampled.size

    plt.figure(figsize=figsize)

    plt.subplot(1, 3, 1)
    plt.title(f"Original\n{orig_w}×{orig_h} pixels")
    plt.imshow(original)
    plt.axis("off")

    upscale = UPSAMPLE_SCALE_NUM / UPSAMPLE_SCALE_DEN
    downscale = DOWNSAMPLE_SCALE_NUM / DOWNSAMPLE_SCALE_DEN
    
    plt.subplot(1, 3, 2)
    plt.title(f"Upsampled ({upscale}x)\n{up_w}×{up_h} pixels")
    plt.imshow(upsampled)
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.title(f"Downsampled ({downscale})\n{down_w}×{down_h} pixels")
    plt.imshow(downsampled)
    plt.axis("off")

    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        print(f"Saved comparison image to: {save_path}")
        print(f"  Original: {orig_w}×{orig_h} pixels")
        print(f"  Upsampled: {up_w}×{up_h} pixels")
        print(f"  Downsampled: {down_w}×{down_h} pixels")
    else:
        plt.show()


def main():
    # Load image relative to this script's folder
    base_dir = Path(__file__).resolve().parent
    img_path = base_dir / INPUT_IMAGE_PATH
    
    print(f"Loading image from: {img_path}")
    image = Image.open(img_path).convert("RGB")
    
    # Resize to target size (similar to ESP32 resolution)
    image = image.resize(TARGET_SIZE, Image.BILINEAR)
    print(f"Resized to: {TARGET_SIZE}")
    
    # Upsample
    upscale = UPSAMPLE_SCALE_NUM / UPSAMPLE_SCALE_DEN
    print(f"Upsampling ({upscale}x)...")
    upsampled = resize_nearest_neighbor(image, scale_num=UPSAMPLE_SCALE_NUM, scale_den=UPSAMPLE_SCALE_DEN)
    print(f"Upsampled size: {upsampled.size[0]}x{upsampled.size[1]}")
    
    # Downsample
    downscale = DOWNSAMPLE_SCALE_NUM / DOWNSAMPLE_SCALE_DEN
    print(f"Downsampling ({downscale})...")
    downsampled = resize_nearest_neighbor(image, scale_num=DOWNSAMPLE_SCALE_NUM, scale_den=DOWNSAMPLE_SCALE_DEN)
    print(f"Downsampled size: {downsampled.size[0]}x{downsampled.size[1]}")
    
    # Save comparison image
    output_path = base_dir / OUTPUT_IMAGE_PATH
    visualize(image, upsampled, downsampled, save_path=str(output_path), figsize=FIGURE_SIZE, dpi=FIGURE_DPI)


if __name__ == "__main__":
    main()
