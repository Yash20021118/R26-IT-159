import os
from dataclasses import dataclass
from typing import List

from .paths import MODEL_METADATA_PATH, MODEL_PATH


def _get_allowed_origins() -> List[str]:
    origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5000")
    return [origin.strip() for origin in origins.split(",") if origin.strip()]


@dataclass(frozen=True)
class Settings:
    api_title: str
    api_version: str
    model_path: str
    model_metadata_path: str
    log_level: str
    allowed_origins: List[str]


settings = Settings(
    api_title=os.getenv("API_TITLE", "Seed Recommendation Engine API"),
    api_version=os.getenv("API_VERSION", "0.1.0"),
    model_path=os.getenv("MODEL_PATH", str(MODEL_PATH)),
    model_metadata_path=os.getenv("MODEL_METADATA_PATH", str(MODEL_METADATA_PATH)),
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    allowed_origins=_get_allowed_origins(),
)
