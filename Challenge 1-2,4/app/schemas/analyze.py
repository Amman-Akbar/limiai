from pydantic import BaseModel, Field
from typing import List, Optional

class DetectedObjectSchema(BaseModel):
    label: str
    confidence: float
    box: List[float]

class NLPResultsSchema(BaseModel):
    query: str
    sentiment: str
    extracted_keywords: List[str]
    semantic_mapping: List[str]

class AnalysisResponseDataSchema(BaseModel):
    detected_objects: List[DetectedObjectSchema]
    text_analysis: NLPResultsSchema

class AnalysisResponseSchema(BaseModel):
    status: str = "success"
    data: AnalysisResponseDataSchema
    cached: bool = False

class ErrorResponseSchema(BaseModel):
    detail: str
