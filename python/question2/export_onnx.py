from ultralytics import YOLO
from pathlib import Path

# ============================================================================
# CONFIGURATION (HARDCODED FINAL MODEL)
# ============================================================================
BEST_MODEL_PATH = Path(
    "hyperparameter_results/exp_3_lr0.001_batch8/weights/best.pt"
)

OUTPUT_DIR = Path("../../esp32_cam_link/esp32_cam_q2")
MODEL_NAME = "digit_detection_model"
IMGSZ = 320

# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 70)
    print("YOLO → ONNX EXPORT (FINAL MODEL)")
    print("=" * 70)

    if not BEST_MODEL_PATH.exists():
        print(f"❌ Model not found: {BEST_MODEL_PATH}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\nUsing FINAL model:")
    print("--------------------------------------------------")
    print("Experiment   : exp_3_lr0.001_batch8")
    print("Learning Rate: 0.001")
    print("Batch Size   : 8")
    print("mAP50        : 0.9064")
    print("Model Path   :", BEST_MODEL_PATH)
    print("--------------------------------------------------\n")

    model = YOLO(str(BEST_MODEL_PATH))

    print("Exporting ONNX…")
    model.export(
        format="onnx",
        imgsz=IMGSZ,
        opset=12,
        simplify=False,
        dynamic=False
    )

    print("\n✓ ONNX export complete")
    print("✓ File created next to best.pt (best.onnx)")
    print("\nNEXT STEP:")
    print("→ Convert best.onnx to TFLite in a separate environment")

if __name__ == "__main__":
    main()
