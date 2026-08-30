from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the sender (user/assistant)")
    content: str = Field(..., description="Message text content")


class ChatRequest(BaseModel):
    message: str = Field(..., description="User question in Sinhala, English, or Tamil")
    language: Optional[str] = Field("auto", description="Language preference: 'si', 'en', 'ta', or 'auto'")
    session_id: Optional[str] = Field(None, description="Optional chat session identifier for persistent tracking")


class CropRecommendationInsight(BaseModel):
    crop: str
    confidence: float
    sinhala_name: Optional[str] = None
    tamil_name: Optional[str] = None
    crop_si: Optional[str] = None
    crop_ta: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    detected_language: str
    model_source: str
    session_id: Optional[str] = None
    agro_zone: Optional[str] = None
    soil_type: Optional[str] = None
    soil_series_prediction: Optional[Dict[str, Any]] = None
    extracted_features: Optional[Dict[str, Any]] = None
    recommended_crops: Optional[List[CropRecommendationInsight]] = None
    soil_remediation: Optional[str] = None
    latency_ms: Optional[float] = None


class ChatStatusResponse(BaseModel):
    status: str
    engine_name: str
    device: str
    cuda_available: bool
    ml_model_accuracy: float
    supported_languages: List[str]
    cloud_api_dependency: bool
    description: str

