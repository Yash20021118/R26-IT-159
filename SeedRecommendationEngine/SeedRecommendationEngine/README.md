# Seed Recommendation Engine

## Project Overview
Seed Recommendation Engine is a Smart Agriculture Decision Support component that predicts the most suitable crops based on soil and environmental parameters. This phase delivers a complete data pipeline, machine learning model training, API backend, and a responsive frontend prototype for research progress presentations.

## Research Objectives (Phase 1)
- Clean and preprocess the Kaggle Crop Recommendation dataset.
- Train and compare baseline ML models (Decision Tree, KNN, Random Forest).
- Provide a recommendation engine with confidence-based ranking.
- Expose production-ready APIs with validation and documentation.
- Provide a modern frontend prototype for demo and validation.

## Architecture
- **Data Layer**: Dataset ingestion, validation, preprocessing scripts.
- **Model Layer**: Training, evaluation, model persistence.
- **Service Layer**: Prediction and recommendation logic.
- **API Layer**: FastAPI endpoints with Pydantic schemas.
- **UI Layer**: React client with a clean agricultural theme.

## Dataset
- **Source**: Kaggle Crop Recommendation Dataset
- **Columns**: N, P, K, temperature, humidity, ph, rainfall, label
- **Label**: `label` is the crop name

Place the dataset at:
```
SeedRecommendationEngine/backend/dataset/Crop_recommendation.csv
```

## Preprocessing
Scripts validate required columns and handle missing values:
- Numeric columns are coerced and filled with median values.
- Labels are filled with the mode if any are missing.

Run preprocessing:
```bash
python backend/scripts/preprocess_data.py
```

## Models
- Decision Tree
- K-Nearest Neighbors
- Random Forest (primary model for recommendations)

Model training compares accuracy, precision, recall, and F1-score (macro). The best model is saved as:
```
backend/trained_models/crop_model.pkl
```

## Evaluation and Visualization
Generated in `backend/reports/`:
- Confusion matrix
- Model accuracy comparison chart
- Model comparison JSON

Run evaluation:
```bash
python backend/scripts/evaluate_model.py
```

## Backend API
**Base URL**: `http://localhost:8000`

### Endpoints
- `GET /` Health check
- `POST /predict` Best crop prediction
- `POST /recommend` Top 3 recommendations
- `GET /model-info` Model metadata and accuracy

### Sample Request
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

### Sample Response
```json
{
  "recommendations": [
    { "crop": "rice", "confidence": 92.4 },
    { "crop": "maize", "confidence": 4.1 },
    { "crop": "cotton", "confidence": 1.7 }
  ]
}
```

## Frontend Prototype
The React UI provides:
- Parameter input form
- Best crop prediction card
- Top 3 recommendations with confidence bars
- Loading and error states

## Installation
### Backend
```bash
cd SeedRecommendationEngine/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/preprocess_data.py
python scripts/train_model.py
uvicorn app.main:app --reload
```

### Frontend
```bash
cd SeedRecommendationEngine/frontend
npm install
npm start
```

## Folder Structure
```
SeedRecommendationEngine/
│
├── backend/
│   ├── app/
│   ├── dataset/
│   ├── trained_models/
│   ├── notebooks/
│   ├── reports/
│   ├── scripts/
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

## Research Contribution
- Establishes a reliable ML baseline for crop suitability prediction.
- Implements confidence-based ranking for interpretability.
- Provides a demo-ready UI and API for stakeholder feedback.

## Limitations (Phase 1)
- No region-based filtering
- No agro-ecological zoning
- No IoT sensor integration
- No hybrid AI logic

## Next Phase Plans
- Region and agro-ecological zone personalization
- IoT-based dynamic parameter capture
- Hybrid AI recommendations with expert rules
- Advanced explainability and multi-modal insights

## Screenshots
- `docs/screenshots/ui-overview.png` (placeholder)
- `docs/screenshots/recommendation-output.png` (placeholder)
