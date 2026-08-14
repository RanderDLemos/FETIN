import csv
import json
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "runs", "drone_v1", "results.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "runs", "drone_v1", "metrics.json")

with open(CSV_PATH) as f:
    rows = list(csv.DictReader(f))

epochs = []
best_map50 = 0
best_epoch = 0

for row in rows:
    epoch = int(row["epoch"])
    map50 = float(row["metrics/mAP50(B)"])
    epochs.append({
        "epoch": epoch,
        "train_box_loss": float(row["train/box_loss"]),
        "train_cls_loss": float(row["train/cls_loss"]),
        "train_dfl_loss": float(row["train/dfl_loss"]),
        "precision":      float(row["metrics/precision(B)"]),
        "recall":         float(row["metrics/recall(B)"]),
        "mAP50":          map50,
        "mAP50_95":       float(row["metrics/mAP50-95(B)"]),
        "val_box_loss":   float(row["val/box_loss"]),
        "val_cls_loss":   float(row["val/cls_loss"]),
    })
    if map50 > best_map50:
        best_map50 = map50
        best_epoch = epoch

last = epochs[-1]
metrics = {
    "model": "yolov8n",
    "dataset": "datasets/unified",
    "classes": ["pool", "tire"],
    "epochs_trained": len(epochs),
    "image_size": 640,
    "device": "mps",
    "augmentations": {
        "degrees": 180,
        "flipud": 0.5,
        "fliplr": 0.5,
        "scale": 0.6,
        "perspective": 0.0005,
        "mosaic": 1.0,
        "mixup": 0.1,
        "hsv_h": 0.015,
        "hsv_s": 0.5,
        "hsv_v": 0.4,
    },
    "best": {
        "epoch": best_epoch,
        "mAP50": round(best_map50, 4),
    },
    "final_epoch": {
        "precision": round(last["precision"], 4),
        "recall":    round(last["recall"], 4),
        "mAP50":     round(last["mAP50"], 4),
        "mAP50_95":  round(last["mAP50_95"], 4),
    },
    "per_epoch": epochs,
}

with open(OUT_PATH, "w") as f:
    json.dump(metrics, f, indent=2)

print(f"Salvo em {OUT_PATH}")
print(f"Melhor mAP50: {best_map50:.4f} (época {best_epoch})")
