from pathlib import Path
from uuid import uuid4

from django.conf import settings
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def run_object_detection(image_path):
    results = model(str(image_path), conf=0.5)
    result = results[0]

    output_filename = f"detected_{Path(image_path).stem}_{uuid4().hex[:8]}.jpg"
    output_path = settings.MEDIA_ROOT / "results" / output_filename

    result.save(filename=str(output_path))

    detections = []
    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        detections.append({
            "label": result.names[class_id],
            "confidence": round(confidence * 100, 2),
        })

    return {
        "result_filename": output_filename,
        "detections": detections,
    }