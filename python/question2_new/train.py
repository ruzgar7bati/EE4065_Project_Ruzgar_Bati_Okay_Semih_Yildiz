"""
Training Script for Handwritten Digit Detection

Compatible with:
- Python 3.11
- ultralytics >= 8.3.0
- Latest torch versions

IMPORTANT:
- In newer ultralytics versions, model.train() returns metrics directly
- No need to call model.val() separately after training
"""

from ultralytics import YOLO
import os
import pandas as pd
from pathlib import Path
import time

# ============================================================================
# CONFIGURATION
# ============================================================================
HYPERPARAMETER_SEARCH = True

MODEL = "yolov8n.pt"
DATA_YAML = "data.yaml"

EPOCHS = 50
IMGSZ = 320
DEVICE = "cpu"  # Change to "cuda" if GPU available

HYPERPARAMETER_EXPERIMENTS = [
    {"lr0": 0.001, "batch": 2, "name": "lr0.001_batch2"},
    {"lr0": 0.001, "batch": 4, "name": "lr0.001_batch4"},
    {"lr0": 0.001, "batch": 8, "name": "lr0.001_batch8"},
    {"lr0": 0.01, "batch": 2, "name": "lr0.01_batch2"},
    {"lr0": 0.01, "batch": 4, "name": "lr0.01_batch4"},
    {"lr0": 0.01, "batch": 8, "name": "lr0.01_batch8"},
]

RESULTS_DIR = Path("hyperparameter_results")

# ============================================================================
# TRAINING + VALIDATION
# ============================================================================
def run_experiment(exp_config, exp_id):
    print("\n" + "=" * 70)
    print(f"Experiment {exp_id + 1}/{len(HYPERPARAMETER_EXPERIMENTS)}")
    print(f"Name : {exp_config['name']}")
    print(f"LR   : {exp_config['lr0']}")
    print(f"Batch: {exp_config['batch']}")
    print("=" * 70)

    model = YOLO(MODEL)
    project_name = f"exp_{exp_id + 1}_{exp_config['name']}"

    try:
        # -------------------------------
        # TRAIN (returns metrics in newer versions)
        # -------------------------------
        results = model.train(
            data=DATA_YAML,
            epochs=EPOCHS,
            imgsz=IMGSZ,
            batch=exp_config["batch"],
            lr0=exp_config["lr0"],
            device=DEVICE,
            project=str(RESULTS_DIR),
            name=project_name,
            save=True,
            plots=True,
            verbose=True,
        )

        # Get best model path from training results
        exp_dir = RESULTS_DIR / project_name
        best_model_path = exp_dir / "weights" / "best.pt"

        if not best_model_path.exists():
            raise FileNotFoundError("best.pt not found after training")

        # -------------------------------
        # EXTRACT METRICS (newer YOLO versions)
        # -------------------------------
        # In newer versions, results from model.train() contain validation metrics
        # Access via results.results_dict or results.metrics
        if hasattr(results, 'results_dict'):
            # Newer API: results.results_dict contains all metrics
            metrics = results.results_dict
            map50 = float(metrics.get('metrics/mAP50(B)', 0.0))
            map5095 = float(metrics.get('metrics/mAP50-95(B)', 0.0))
            precision = float(metrics.get('metrics/precision(B)', 0.0))
            recall = float(metrics.get('metrics/recall(B)', 0.0))
        elif hasattr(results, 'metrics') and hasattr(results.metrics, 'box'):
            # Alternative: direct metrics access
            m = results.metrics.box
            map50 = float(m.map50) if hasattr(m, 'map50') else 0.0
            map5095 = float(m.map) if hasattr(m, 'map') else 0.0
            precision = float(m.mp) if hasattr(m, 'mp') else 0.0
            recall = float(m.mr) if hasattr(m, 'mr') else 0.0
        else:
            # Fallback: run validation explicitly
            print("\nRunning explicit validation to collect metrics...")
            val_results = model.val(
                data=DATA_YAML,
                imgsz=IMGSZ,
                device=DEVICE
            )
            m = val_results.metrics.box
            map50 = float(m.map50)
            map5095 = float(m.map)
            precision = float(m.mp)
            recall = float(m.mr)

        print(
            f"✓ Validation results | "
            f"mAP50: {map50:.4f}, "
            f"mAP50-95: {map5095:.4f}, "
            f"P: {precision:.4f}, "
            f"R: {recall:.4f}"
        )

        return {
            "experiment_id": exp_id + 1,
            "name": exp_config["name"],
            "learning_rate": exp_config["lr0"],
            "batch_size": exp_config["batch"],
            "image_size": IMGSZ,
            "mAP50": map50,
            "mAP50_95": map5095,
            "precision": precision,
            "recall": recall,
            "model_path": str(best_model_path),
        }

    except Exception as e:
        print(f"✗ Experiment failed: {e}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================================
# HYPERPARAMETER SEARCH
# ============================================================================
def run_hyperparameter_search():
    print("=" * 70)
    print("HYPERPARAMETER SEARCH")
    print("=" * 70)

    RESULTS_DIR.mkdir(exist_ok=True)
    all_results = []

    start_time = time.time()

    for i, exp in enumerate(HYPERPARAMETER_EXPERIMENTS):
        result = run_experiment(exp, i)
        if result:
            all_results.append(result)

    elapsed_min = (time.time() - start_time) / 60
    print(f"\nAll experiments finished in {elapsed_min:.1f} minutes")

    if not all_results:
        print("No successful experiments.")
        return

    df = pd.DataFrame(all_results)
    csv_path = RESULTS_DIR / "validation_metrics.csv"
    df.to_csv(csv_path, index=False)

    best = df.loc[df["mAP50"].idxmax()]

    with open(RESULTS_DIR / "best_model_info.txt", "w", encoding="utf-8") as f:
        f.write("BEST MODEL INFORMATION\n")
        f.write("=" * 50 + "\n")
        f.write(f"Experiment   : {best['name']}\n")
        f.write(f"Learning Rate: {best['learning_rate']}\n")
        f.write(f"Batch Size   : {best['batch_size']}\n")
        f.write(f"mAP50        : {best['mAP50']:.4f}\n")
        f.write(f"Model Path   : {best['model_path']}\n")

    print(f"\n✓ Results saved to: {csv_path}")
    print(f"✓ Best model: {best['name']} (mAP50: {best['mAP50']:.4f})")

# ============================================================================
# MAIN
# ============================================================================
def main():
    if not os.path.exists(DATA_YAML):
        print(f"Error: {DATA_YAML} not found.")
        return

    if HYPERPARAMETER_SEARCH:
        run_hyperparameter_search()
    else:
        print("Single-run mode disabled in this configuration.")

if __name__ == "__main__":
    main()

