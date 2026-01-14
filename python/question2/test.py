"""
Test Script - Final Evaluation on TEST dataset
Compatible with:
- Python 3.10
- ultralytics 8.0.196
"""

from ultralytics import YOLO
import os
import pandas as pd
from pathlib import Path
import glob

# ============================================================================
# CONFIGURATION
# ============================================================================
MODEL_PATH = None  # Set manually if skipping hyperparameter search
DATA_YAML = "data.yaml"
RESULTS_DIR = Path("hyperparameter_results")

TEST_DIR = "images/test"
CONF_THRESHOLD = 0.4

SAVE_IMAGES = False
OUTPUT_DIR = "test_results"

# ============================================================================
# HELPERS
# ============================================================================
def load_best_model_info():
    csv_path = RESULTS_DIR / "validation_metrics.csv"
    if not csv_path.exists():
        return None

    df = pd.read_csv(csv_path)
    best = df.loc[df["mAP50"].idxmax()]

    print("Best model from hyperparameter search:")
    print(
        f"  {best['experiment']} | "
        f"LR={best['learning_rate']} | "
        f"Batch={best['batch_size']}"
    )
    print(f"  Validation mAP50: {best['mAP50']:.4f}")

    return {
        "model_path": best["model_path"],
        "name": best["experiment"],          # <- map experiment → name
        "lr0": best["learning_rate"],
        "batch": best["batch_size"],
        "imgsz": 320,                         # fixed, not stored in CSV
        "val_mAP50": best["mAP50"],
        "val_precision": best["precision"],
        "val_recall": best["recall"],
    }

def extract_metrics(results):
    """
    Correct metric extraction for ultralytics 8.0.196
    model.val() returns DetMetrics
    """
    m = results.box
    return (
        float(m.map50),
        float(m.map),
        float(m.mp),
        float(m.mr),
    )


# ============================================================================
# TESTING
# ============================================================================
def test_model(model_path):
    print(f"\nLoading model: {model_path}")
    if not os.path.exists(model_path):
        print("Model not found.")
        return None

    model = YOLO(model_path)

    # Create temporary data.yaml pointing val to test set
    temp_yaml = "data_test.yaml"
    with open(DATA_YAML, "r") as f:
        lines = f.readlines()

    with open(temp_yaml, "w") as f:
        for line in lines:
            if line.strip().startswith("val:"):
                f.write("val: images/test\n")
            else:
                f.write(line)

    try:
        results = model.val(
            data=temp_yaml,
            conf=CONF_THRESHOLD,
            verbose=True,
        )

        map50, map5095, precision, recall = extract_metrics(results)

        print("\nTest Set Results:")
        print(f"  mAP50:     {map50:.4f}")
        print(f"  mAP50-95:  {map5095:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")

        return {
            "mAP50": map50,
            "mAP50_95": map5095,
            "precision": precision,
            "recall": recall,
        }

    finally:
        if os.path.exists(temp_yaml):
            os.remove(temp_yaml)

# ============================================================================
# VISUALIZATION (OPTIONAL)
# ============================================================================
def visualize_test_images(model_path):
    if not SAVE_IMAGES:
        return

    model = YOLO(model_path)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    image_paths = []
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        image_paths.extend(glob.glob(os.path.join(TEST_DIR, ext)))

    for img in image_paths:
        results = model(img, conf=CONF_THRESHOLD)
        save_path = os.path.join(OUTPUT_DIR, f"result_{os.path.basename(img)}")
        results[0].save(filename=save_path)

# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 70)
    print("TEST - FINAL EVALUATION")
    print("=" * 70)

    if MODEL_PATH:
        best = {
            "model_path": MODEL_PATH,
            "name": "manual",
            "lr0": 0,
            "batch": 0,
            "imgsz": 320,
            "val_mAP50": 0,
            "val_precision": 0,
            "val_recall": 0,
        }
    else:
        best = load_best_model_info()
        if not best:
            print("No validation results found. Run train.py first.")
            return

    test_metrics = test_model(best["model_path"])
    if not test_metrics:
        print("Test failed.")
        return

    # Save final results
    out_csv = RESULTS_DIR / "test_results.csv"
    df = pd.DataFrame([{
        **best,
        "test_mAP50": test_metrics["mAP50"],
        "test_mAP50_95": test_metrics["mAP50_95"],
        "test_precision": test_metrics["precision"],
        "test_recall": test_metrics["recall"],
    }])
    df.to_csv(out_csv, index=False)

    print("\n" + "=" * 70)
    print("FINAL TEST RESULTS")
    print("=" * 70)
    print(df.to_string(index=False))
    print("=" * 70)
    print(f"\n✓ Results saved to: {out_csv}")

    if SAVE_IMAGES:
        visualize_test_images(best["model_path"])

    print("\n✓ Test set was used ONLY for final evaluation.")

if __name__ == "__main__":
    main()
