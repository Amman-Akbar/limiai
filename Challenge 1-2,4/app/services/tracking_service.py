import mlflow
import time
import os
import logging

logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("Image-Analysis-Service")

def track_inference(query: str, nlp_results: dict, detected_objects: list, latency_ms: float):
    """
    Logs inference metadata, parameters, and results to MLflow for experiment tracking.
    
    MLOps Best Practices:
    - Track input query parameters (text).
    - Track output summary metrics (number of detections, sentiment).
    - Track system performance (latency).
    - Track model metadata (versions).
    """
    try:
        with mlflow.start_run(nested=True):
            # 1. Log Parameters (Inputs)
            mlflow.log_param("query_text", query)
            mlflow.log_param("num_keywords", len(nlp_results.get("keywords", [])))
            
            # 2. Log Metrics (Latency & Result counts)
            mlflow.log_metric("latency_ms", latency_ms)
            mlflow.log_metric("num_detections", len(detected_objects))
            
            # 3. Log Tags (Metadata)
            mlflow.set_tag("sentiment", nlp_results.get("sentiment", "N/A"))
            mlflow.set_tag("model_yolo", "YOLOE-26n-seg")
            mlflow.set_tag("model_nlp", "DistilBERT-SST2")
            
            # Log results as a simplified artifact if needed
            logger.info(f"MLflow logged inference metrics: latency={latency_ms:.2f}ms, detections={len(detected_objects)}")
            
    except Exception as e:
        logger.warning(f"Failed to log to MLflow: {str(e)}")
