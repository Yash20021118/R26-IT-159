# Seed Recommendation Engine - Backend

## Overview
The backend provides a FastAPI service for crop/seed recommendation. It loads a trained model, exposes prediction and recommendation endpoints, and ships scripts for data preprocessing, training, and evaluation.

## Folder Structure
- app/: FastAPI application (routes, services, schemas, utils)
- dataset/: Kaggle Crop Recommendation dataset
- trained_models/: Saved model and metadata
- scripts/: Preprocessing, training, and evaluation scripts
- reports/: Generated charts and metrics

## Setup
1. Create and activate a Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place the dataset at:
   backend/dataset/Crop_recommendation.csv

## Train the Model
```bash
python scripts/preprocess_data.py
python scripts/train_model.py
python scripts/evaluate_model.py
```

## Run the API
```bash
uvicorn app.main:app --reload
```

## API Endpoints
- GET / : Health check
- POST /predict : Best crop prediction
- POST /recommend : Top 3 ranked recommendations
- GET /model-info : Model metadata and accuracy

## Sample Request
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 21,
  "humidity": 82,
  "ph": 6.5,
  "rainfall": 202
}
```
