from fastapi import APIRouter, HTTPException

from ..schemas import InputFeatures, PredictionResponse, RecommendationResponse
from ..services.model_service import ModelService

router = APIRouter(tags=["predictions"])
service = ModelService()


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: InputFeatures) -> PredictionResponse:
    try:
        return service.predict(payload)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/recommend", response_model=RecommendationResponse)
def recommend(payload: InputFeatures) -> RecommendationResponse:
    try:
        return service.recommend(payload)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
