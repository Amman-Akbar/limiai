from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.yolo_service import detect_objects
from app.services.nlp_service import analyze_text
from app.services.cache_service import LRUCache
from app.services.tracking_service import track_inference
from app.schemas.analyze import AnalysisResponseSchema
from app.core.config import settings
import logging
import hashlib
import time

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize LRU Cache based on centralized settings
inference_cache = LRUCache(capacity=settings.CACHE_CAPACITY)

@router.post("/analyze", response_model=AnalysisResponseSchema)
async def analyze(
    image: UploadFile = File(...),
    text: str = Form(...)
):
    """
    Analyzes an image and a text query.
    1. Extracts sentiment and keywords from text.
    2. Performs object detection using YOLOWorld/YOLOE.
    3. Returns detected objects and sentiment analysis.
    Uses an LRU Cache to optimize latency for repeat requests.
    """
    start_time = time.time()
    
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded is not an image.")

    if not text.strip():
        raise HTTPException(status_code=400, detail="Text query cannot be empty.")

    try:
        # Generate hash for the LRU cache key
        contents = await image.read()
        image_hash = hashlib.md5(contents).hexdigest()
        cache_key = f"{image_hash}:{text}"

        # 1. Check LRU Cache
        cached_result = inference_cache.get(cache_key)
        if cached_result:
            latency = (time.time() - start_time) * 1000
            logger.info(f"CACHE HIT for query: {text} (Latency: {latency:.2f}ms)")
            return {
                "status": "success",
                "data": cached_result,
                "cached": True
            }

        logger.info(f"CACHE MISS for query: {text}. Processing...")

        # 2. NLP Pipeline
        nlp_results = analyze_text(text)
        
        # 3. Combine filters
        search_filters = list(set(nlp_results["keywords"] + nlp_results["semantic_classes"]))
        
        # 4. Computer Vision Pipeline
        detected_objects = await detect_objects(contents, keywords=search_filters)
        
        result_data = {
            "detected_objects": detected_objects,
            "text_analysis": {
                "query": text,
                "sentiment": nlp_results["sentiment"],
                "extracted_keywords": nlp_results["keywords"],
                "semantic_mapping": nlp_results["semantic_classes"]
            }
        }

        # 5. Store in Cache
        inference_cache.put(cache_key, result_data)

        latency = (time.time() - start_time) * 1000
        
        # 6. MLOps Tracking
        track_inference(text, nlp_results, detected_objects, latency)
        
        logger.info(f"Analysis complete. (Latency: {latency:.2f}ms)")

        return {
            "status": "success",
            "data": result_data,
            "cached": False
        }
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal processing error: {str(e)}")
