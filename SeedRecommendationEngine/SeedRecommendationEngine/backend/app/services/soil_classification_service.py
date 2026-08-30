import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import joblib
import numpy as np
import pandas as pd

from ..utils.logger import get_logger

logger = get_logger("soil_classification_service")


class SoilClassificationService:
    """
    Integrates the research project's core Soil Classification Model
    located in R26-IT-159-Soil-Classification-Region-Identification/models.
    Predicts the 14 Sri Lankan Soil Series and integrates with Agro-Ecological Zones.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoilClassificationService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.models_dir = Path(__file__).resolve().parents[4] / "models"
        if not self.models_dir.exists():
            # Fallback relative to project root
            self.models_dir = Path(__file__).resolve().parents[3] / "models"

        self.soil_model = None
        self.scaler = None
        self.le_soil = None
        self.le_zone = None
        self._is_loaded = False
        self._load_models()
        self._initialized = True

    def _load_models(self):
        try:
            soil_model_path = self.models_dir / "soil_model.pkl"
            scaler_path = self.models_dir / "scaler.pkl"
            le_soil_path = self.models_dir / "label_encoder_soil.pkl"
            le_zone_path = self.models_dir / "label_encoder_zone.pkl"

            if all(p.exists() for p in [soil_model_path, scaler_path, le_soil_path, le_zone_path]):
                self.soil_model = joblib.load(soil_model_path)
                self.scaler = joblib.load(scaler_path)
                self.le_soil = joblib.load(le_soil_path)
                self.le_zone = joblib.load(le_zone_path)
                self._is_loaded = True
                logger.info(f"Loaded Core Soil Classification Model from {self.models_dir}")
            else:
                logger.warning(f"Soil model files not all found in {self.models_dir}")
        except Exception as e:
            logger.error(f"Failed to load soil classification model: {e}")

    def is_available(self) -> bool:
        return self._is_loaded and self.soil_model is not None

    def classify_soil(
        self,
        soil_ph: float = 6.5,
        nitrogen_N: float = 70.0,
        phosphorus_P: float = 40.0,
        potassium_K: float = 40.0,
        soil_moisture: float = 50.0,
        soil_temp: float = 27.0,
        ambient_temp: float = 28.0,
        humidity: float = 75.0,
        rainfall: float = 150.0,
        altitude: float = 50.0,
        zone: str = "Dry"
    ) -> Optional[Dict[str, Any]]:
        if not self.is_available():
            return None

        try:
            # Map zone string to encoder classes: ['Dry', 'Dry/Wet', 'Intermediate', 'Wet']
            valid_zones = list(self.le_zone.classes_)
            zone_matched = "Dry"
            z_lower = zone.lower()
            if "wet" in z_lower and "dry" in z_lower:
                zone_matched = "Dry/Wet"
            elif "wet" in z_lower:
                zone_matched = "Wet"
            elif "inter" in z_lower:
                zone_matched = "Intermediate"
            elif "dry" in z_lower:
                zone_matched = "Dry"
            elif zone in valid_zones:
                zone_matched = zone

            zone_enc = self.le_zone.transform([zone_matched])[0]

            scaler_features = [
                "soil_ph", "nitrogen_N", "phosphorus_P", "potassium_K", "soil_moisture",
                "soil_temp", "ambient_temp", "humidity", "rainfall", "altitude"
            ]
            raw_dict = {
                "soil_ph": [soil_ph],
                "nitrogen_N": [nitrogen_N],
                "phosphorus_P": [phosphorus_P],
                "potassium_K": [potassium_K],
                "soil_moisture": [soil_moisture],
                "soil_temp": [soil_temp],
                "ambient_temp": [ambient_temp],
                "humidity": [humidity],
                "rainfall": [rainfall],
                "altitude": [altitude]
            }
            raw_df = pd.DataFrame(raw_dict, columns=scaler_features)
            scaled_vals = self.scaler.transform(raw_df)

            model_features = scaler_features + ["agro_ecological_zone_encoded"]
            model_input_df = pd.DataFrame(
                np.hstack([scaled_vals, [[zone_enc]]]),
                columns=model_features
            )

            pred_idx = self.soil_model.predict(model_input_df)[0]
            probs = self.soil_model.predict_proba(model_input_df)[0]

            predicted_soil = self.le_soil.inverse_transform([pred_idx])[0]
            confidence = float(probs[pred_idx])

            # Top 3 alternative soils
            ranked_indices = np.argsort(probs)[::-1][:3]
            alternatives = []
            for idx in ranked_indices:
                alternatives.append({
                    "soil": self.le_soil.inverse_transform([idx])[0],
                    "confidence": round(float(probs[idx]), 4)
                })

            return {
                "predicted_soil_series": predicted_soil,
                "confidence": round(confidence, 4),
                "agro_zone": zone_matched,
                "top_alternatives": alternatives
            }
        except Exception as err:
            logger.error(f"Soil classification inference error: {err}")
            return None
