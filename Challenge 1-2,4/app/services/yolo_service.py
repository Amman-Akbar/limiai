from ultralytics import YOLO
from app.core.config import settings
import numpy as np
import cv2

# Initialize YOLOE using configurable model path
model = YOLO(settings.YOLO_MODEL_PATH)

def get_model_classes():
    """Returns a list of all class names the YOLO model currently knows."""
    return list(model.names.values())

async def detect_objects(image_bytes: bytes, keywords=None):
    """
    Performs object detection on an image using YOLOE (open-vocabulary).
    If keywords are provided, they are set as the target classes for detection.
    """
    # OpenCV pipeline for image decoding
    img = cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8),
        cv2.IMREAD_COLOR
    )

    # YOLOE open-vocabulary: tell the model what classes to detect
    if keywords:
        model.set_classes(keywords)

    # Perform inference
    results = model(img)

    detections = []
    
    # Process results (PyTorch-based detection output)
    for r in results:
        if hasattr(r, 'boxes') and r.boxes:
            for box in r.boxes:
                coords = box.xyxy[0].tolist()
                label = model.names[int(box.cls[0])]
                confidence = float(box.conf[0])

                detections.append({
                    "label": label,
                    "confidence": round(confidence, 4),
                    "box": [round(c, 2) for c in coords]
                })

    return detections