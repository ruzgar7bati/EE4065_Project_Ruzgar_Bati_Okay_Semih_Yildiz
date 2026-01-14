"""
Collect validation metrics from Ultralytics results.csv files

Compatible with:
- ultralytics 8.0.196
- Python 3.10+

Scans all experiment folders inside hyperparameter_results/
and produces:
- validation_metrics.csv
- best_model_info.txt
"""

import pandas as pd
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================
RESULTS_DIR = Path("hyperparameter_results")
OUTPUT_CSV = RESULTS_DIR / "validation_metrics.csv"
BEST_INFO_TXT = RESULTS_DIR / "best_model_info.txt"

# ============================================================================
# HELPERS
# ============================================================================
def parse_metrics_from_results_csv(exp_dir: Path):
    csv_path = exp_dir / "results.csv"
    if not csv_path.exists():
        return None

    df = pd.read_csv(csv_path)
    if df.empty:
        return None

    last = df.iloc[-1]

    def find_col(possible_keys):
        for col in df.columns:
            for key in possible_keys:
                if key in col:
                    return col
        return None

    col_map50 = find_col(["mAP50"])
    col_map5095 = find_col(["mAP50-95", "mAP_0.5:0.95"])
    col_prec = find_col(["precision"])
    col_rec = find_col(["recall"])

    def val(col):
        return float(last[col]) if col and col in df.columns else 0.0

    return {
        "mAP50": val(col_map50),
        "mAP50_95": val(col_map5095),
        "precision": val(col_prec),
        "recall": val(col_rec),
    }


# ============================================================================
# MAIN
# ============================================================================
def main():
    if not RESULTS_DIR.exists():
        print(f"Error: {RESULTS_DIR} does not exist")
        return

    all_rows = []

    exp_dirs = sorted(
        d for d in RESULTS_DIR.iterdir()
        if d.is_dir() and d.name.startswith("exp_")
    )

    if not exp_dirs:
        print("No experiment folders found.")
        return

    for exp_dir in exp_dirs:
        metrics = parse_metrics_from_results_csv(exp_dir)
        if metrics is None:
            print(f"Skipping {exp_dir.name}: no valid results.csv")
            continue

        weights_dir = exp_dir / "weights"
        best_pt = weights_dir / "best.pt"

        if not best_pt.exists():
            print(f"Skipping {exp_dir.name}: best.pt missing")
            continue

        # Try to infer LR and batch from folder name
        name = exp_dir.name
        lr = None
        batch = None

        if "lr" in name and "batch" in name:
            try:
                lr = float(name.split("lr")[1].split("_")[0])
                batch = int(name.split("batch")[1])
            except Exception:
                pass

        row = {
            "experiment": exp_dir.name,
            "learning_rate": lr,
            "batch_size": batch,
            "mAP50": metrics["mAP50"],
            "mAP50_95": metrics["mAP50_95"],
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "model_path": str(best_pt),
        }

        all_rows.append(row)

    if not all_rows:
        print("No valid experiments found.")
        return

    df = pd.DataFrame(all_rows)
    df.to_csv(OUTPUT_CSV, index=False)

    best = df.loc[df["mAP50"].idxmax()]

    with open(BEST_INFO_TXT, "w", encoding="utf-8") as f:
        f.write("BEST MODEL INFORMATION\n")
        f.write("=" * 50 + "\n")
        f.write(f"Experiment   : {best['experiment']}\n")
        f.write(f"Learning Rate: {best['learning_rate']}\n")
        f.write(f"Batch Size   : {best['batch_size']}\n")
        f.write(f"mAP50        : {best['mAP50']:.4f}\n")
        f.write(f"mAP50-95     : {best['mAP50_95']:.4f}\n")
        f.write(f"Precision    : {best['precision']:.4f}\n")
        f.write(f"Recall       : {best['recall']:.4f}\n")
        f.write(f"Model Path   : {best['model_path']}\n")

    print("\n✓ Validation metrics collected")
    print(f"✓ CSV saved to: {OUTPUT_CSV}")
    print(f"✓ Best model: {best['experiment']} (mAP50={best['mAP50']:.4f})")

if __name__ == "__main__":
    main()
