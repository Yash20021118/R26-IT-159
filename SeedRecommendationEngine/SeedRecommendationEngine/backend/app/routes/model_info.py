from fastapi import APIRouter, HTTPException

from ..schemas import ModelInfoResponse
from ..services.model_service import ModelService

router = APIRouter(tags=["model"])
service = ModelService()


@router.get("/model-info", response_model=ModelInfoResponse)
def model_info() -> ModelInfoResponse:
    try:
        return service.model_info()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
