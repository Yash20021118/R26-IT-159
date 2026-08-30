from typing import List

from pydantic import BaseModel, Field


class InputFeatures(BaseModel):
    N: float = Field(..., ge=0, description="Nitrogen content")
    P: float = Field(..., ge=0, description="Phosphorus content")
    K: float = Field(..., ge=0, description="Potassium content")
    temperature: float = Field(..., ge=-10, le=60, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Relative humidity percentage")
    ph: float = Field(..., ge=0, le=14, description="Soil pH")
    rainfall: float = Field(..., ge=0, description="Rainfall in mm")


class PredictionResponse(BaseModel):
    crop: str
    confidence: float


class RecommendationItem(BaseModel):
    crop: str
    confidence: float


class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]


class ModelInfoResponse(BaseModel):
    model_name: str
    accuracy: float
    feature_columns: List[str]
    trained_on: str
    dataset_rows: int
