from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
@router.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "seed-recommendation-engine"}

