from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # API Metadata
    PROJECT_NAME: str = "AI Image Analysis Service"
    PROJECT_DESCRIPTION: str = "Image analysis API combining YOLOE object detection with NLP pipelines."
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"

    # Model Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    MODEL_DIR: Path = BASE_DIR / "models"
    YOLO_MODEL_PATH: str = str(MODEL_DIR / "yoloe-26n-seg.pt")
    
    # MLflow Configuration
    MLFLOW_TRACKING_URI: str = "file:./mlruns"
    MLFLOW_EXPERIMENT_NAME: str = "Image-Analysis-Service"

    # Cache Configuration
    CACHE_CAPACITY: int = 100

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
