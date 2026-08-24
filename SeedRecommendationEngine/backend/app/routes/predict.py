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


@router.get("/guidance/{crop_name}")
def get_guidance(crop_name: str):
    import sys
    from pathlib import Path
    ROOT = Path(__file__).resolve().parents[3]
    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))
    try:
        from app.utils.crop_guidance import get_crop_guidance
        return get_crop_guidance(crop_name)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

