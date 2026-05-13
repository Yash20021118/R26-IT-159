import json
from pathlib import Path
from typing import Dict, List

import joblib
import numpy as np

from ..schemas import InputFeatures, ModelInfoResponse, PredictionResponse, RecommendationItem, RecommendationResponse
from ..utils.config import settings
from ..utils.paths import MODEL_METADATA_PATH


class ModelService:
    def __init__(self) -> None:
        self._model = None
        self._metadata: Dict[str, object] = {}

    def _load_model(self) -> None:
        if self._model is not None:
            return
        model_path = Path(settings.model_path)
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {model_path}. Train the model first."
            )
        self._model = joblib.load(model_path)
        metadata_path = Path(settings.model_metadata_path)
        if metadata_path.exists():
            self._metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    def _to_feature_array(self, payload: InputFeatures) -> np.ndarray:
        feature_order: List[str] = [
            "N",
            "P",
            "K",
            "temperature",
            "humidity",
            "ph",
            "rainfall",
        ]
        return np.array([[getattr(payload, feature) for feature in feature_order]])

    def predict(self, payload: InputFeatures) -> PredictionResponse:
        self._load_model()
        features = self._to_feature_array(payload)
        probabilities = self._model.predict_proba(features)[0]
        best_index = int(np.argmax(probabilities))
        crop = str(self._model.classes_[best_index])
        confidence = round(float(probabilities[best_index]) * 100, 2)
        return PredictionResponse(crop=crop, confidence=confidence)

    def recommend(self, payload: InputFeatures) -> RecommendationResponse:
        self._load_model()
        features = self._to_feature_array(payload)
        probabilities = self._model.predict_proba(features)[0]
        classes = self._model.classes_
        ranked = sorted(
            zip(classes, probabilities), key=lambda item: item[1], reverse=True
        )
        top_three = [
            RecommendationItem(crop=str(label), confidence=round(float(score) * 100, 2))
            for label, score in ranked[:3]
        ]
        return RecommendationResponse(recommendations=top_three)

    def model_info(self) -> ModelInfoResponse:
        self._load_model()
        metadata = self._metadata or {}
        return ModelInfoResponse(
            model_name=str(metadata.get("model_name", "unknown")),
            accuracy=float(metadata.get("accuracy", 0.0)),
            feature_columns=list(metadata.get("feature_columns", [])),
            trained_on=str(metadata.get("trained_on", "")),
            dataset_rows=int(metadata.get("dataset_rows", 0)),
        )
