import cv2
import argparse
from ultralytics import YOLO

WEIGHTS = "runs/drone_v1/weights/best.pt"
CLASSES = ["pool", "tire"]
COLORS  = {"pool": (0, 200, 255), "tire": (0, 255, 80)}
CONF    = 0.4

def draw(frame, results):
    for box in results[0].boxes:
        cls_id = int(box.cls)
        label  = CLASSES[cls_id] if cls_id < len(CLASSES) else str(cls_id)
        conf   = float(box.conf)
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        color = COLORS.get(label, (255, 255, 255))

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        text = f"{label} {conf:.2f}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(frame, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)
        cv2.putText(frame, text, (x1 + 2, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    return frame

def run(source):
    model = YOLO(WEIGHTS)
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Erro ao abrir fonte: {source}")
        return

    print("Iniciando demo — pressione 'q' para sair")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=CONF, verbose=False)
        frame = draw(frame, results)

        detections = len(results[0].boxes)
        cv2.putText(frame, f"Deteccoes: {detections}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("FETIN — Pool & Tire Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=0,
                        help="Fonte de vídeo: 0=webcam, 1=câmera externa, ou caminho de arquivo/URL")
    parser.add_argument("--conf", type=float, default=CONF,
                        help="Limiar de confiança (padrão: 0.4)")
    args = parser.parse_args()

    CONF = args.conf
    source = int(args.source) if str(args.source).isdigit() else args.source
    run(source)
