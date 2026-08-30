from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
MODELS_DIR = ROOT_DIR / "models"
SEED_BACKEND_DIR = ROOT_DIR / "SeedRecommendationEngine" / "backend"

MODEL_PATH = MODELS_DIR / "crop_model.pkl"
if not MODEL_PATH.exists():
    MODEL_PATH = SEED_BACKEND_DIR / "trained_models" / "crop_model.pkl"

MODEL_METADATA_PATH = SEED_BACKEND_DIR / "trained_models" / "model_metadata.json"
