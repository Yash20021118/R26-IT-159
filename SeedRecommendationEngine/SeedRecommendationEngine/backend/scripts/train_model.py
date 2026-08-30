import json
import sys
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BACKEND_DIR))

from app.utils.paths import DEFAULT_DATASET, MODEL_METADATA_PATH, MODEL_PATH, PROCESSED_DATASET
from scripts.preprocess_data import NUMERIC_COLUMNS, preprocess_dataset


def load_dataset() -> pd.DataFrame:
    if PROCESSED_DATASET.exists():
        return pd.read_csv(PROCESSED_DATASET)
    if DEFAULT_DATASET.exists():
        return preprocess_dataset(DEFAULT_DATASET)
    raise FileNotFoundError(
        f"Dataset not found at {DEFAULT_DATASET}. Place Crop_recommendation.csv there."
    )


def evaluate_model(model, x_test, y_test) -> dict:
    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, predictions, average="macro", zero_division=0
    )
    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
    }


def main() -> None:
    data = load_dataset()
    x = data[NUMERIC_COLUMNS]
    y = data["label"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "RandomForest": RandomForestClassifier(
            n_estimators=250, random_state=42, n_jobs=-1
        ),
    }

    results = {}
    best_model_name = None
    best_score = (-1.0, -1.0)

    for name, model in models.items():
        model.fit(x_train, y_train)
        metrics = evaluate_model(model, x_test, y_test)
        results[name] = metrics

        score = (metrics["accuracy"], metrics["f1"])
        if score > best_score:
            best_score = score
            best_model_name = name

    best_model = models[best_model_name]
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)

    metadata = {
        "model_name": best_model_name,
        "accuracy": results[best_model_name]["accuracy"],
        "precision": results[best_model_name]["precision"],
        "recall": results[best_model_name]["recall"],
        "f1": results[best_model_name]["f1"],
        "feature_columns": NUMERIC_COLUMNS,
        "trained_on": datetime.utcnow().isoformat() + "Z",
        "dataset_rows": int(data.shape[0]),
        "comparison": results,
    }
    MODEL_METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved metadata to {MODEL_METADATA_PATH}")


if __name__ == "__main__":
    main()
