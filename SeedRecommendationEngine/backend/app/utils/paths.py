from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent

DATASET_DIR = BACKEND_DIR / "dataset"
TRAINED_MODELS_DIR = BACKEND_DIR / "trained_models"
REPORTS_DIR = BACKEND_DIR / "reports"
NOTEBOOKS_DIR = BACKEND_DIR / "notebooks"

DEFAULT_DATASET = DATASET_DIR / "Crop_recommendation.csv"
PROCESSED_DATASET = DATASET_DIR / "processed_crop_data.csv"
MODEL_PATH = TRAINED_MODELS_DIR / "crop_model.pkl"
MODEL_METADATA_PATH = TRAINED_MODELS_DIR / "model_metadata.json"
