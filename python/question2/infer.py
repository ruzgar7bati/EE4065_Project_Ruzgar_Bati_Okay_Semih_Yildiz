"""
Inference Script - Generate annotated images for report

Compatible with:
- Python 3.10
- ultralytics 8.0.196
"""

from ultralytics import YOLO
import os
import pandas as pd
from pathlib import Path
import cv2
import glob

# ============================================================================
# CONFIGURATION
# ============================================================================
MODEL_PATH = None  # Set manually if needed
RESULTS_DIR = Path("hyperparameter_results")
TEST_DIR = "images/test"
OUTPUT_DIR = "figures"
CONF_THRESHOLD = 0.25

# ============================================================================
# HELPERS
# ============================================================================
def load_best_model_path():
    csv_path = RESULTS_DIR / "validation_metrics.csv"
    if not csv_path.exists():
        return None

    df = pd.read_csv(csv_path)
    best = df.loc[df["mAP50"].idxmax()]

    print("Best model from hyperparameter search:")
    print(
        f"  {best['experiment']} | "
        f"mAP50={best['mAP50']:.4f}"
    )
    print(f"  Model path: {best['model_path']}")

    return best["model_path"]

# ============================================================================
# INFERENCE
# ============================================================================
def run_inference():
    # Select model
    if MODEL_PATH:
        model_path = MODEL_PATH
        print(f"Using specified model: {model_path}")
    else:
        model_path = load_best_model_path()
        if not model_path:
            print("Error: Could not determine best model.")
            print("Run train.py and collect_validation_metrics.py first,")
            print("or set MODEL_PATH manually.")
            return

    if not os.path.exists(model_path):
        print(f"Error: Model not found: {model_path}")
        return

    print(f"\nLoading model: {model_path}")
    model = YOLO(model_path)

    # Class names (fallback if model.names missing)
    class_names = (
        model.names
        if hasattr(model, "names") and model.names
        else {0: "0", 1: "4", 2: "7"}
    )

    # Collect test images
    image_paths = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"):
        image_paths.extend(glob.glob(os.path.join(TEST_DIR, ext)))

    if not image_paths:
        print(f"No images found in {TEST_DIR}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"\nRunning inference on {len(image_paths)} images")
    print(f"Saving annotated images to: {OUTPUT_DIR}")
    print("=" * 70)

    for idx, img_path in enumerate(sorted(image_paths), 1):
        img_name = os.path.basename(img_path)
        print(f"[{idx}/{len(image_paths)}] {img_name}")

        results = model(img_path, conf=CONF_THRESHOLD)
        result = results[0]

        # Save annotated image
        out_path = os.path.join(OUTPUT_DIR, f"result_{img_name}")
        annotated = result.plot()
        cv2.imwrite(out_path, annotated)
        # Print detections
        if result.boxes is not None and len(result.boxes) > 0:
            detections = []
            for box in result.boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                label = class_names.get(cls_id, f"class_{cls_id}")
                detections.append(f"{label} ({conf:.2%})")
            print(f"  Detections: {', '.join(detections)}")
        else:
            print("  No detections")

    print("=" * 70)
    print("\n✓ Inference complete")
    print(f"✓ Annotated images saved to: {OUTPUT_DIR}")
    print("You can now select figures for your report.")

# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 70)
    print("INFERENCE - REPORT IMAGE GENERATION")
    print("=" * 70)
    run_inference()

if __name__ == "__main__":
    main()
