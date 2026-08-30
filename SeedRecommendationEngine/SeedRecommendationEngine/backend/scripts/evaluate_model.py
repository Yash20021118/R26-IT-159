import json
import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BACKEND_DIR))

from app.utils.paths import DEFAULT_DATASET, MODEL_PATH, PROCESSED_DATASET, REPORTS_DIR
from scripts.preprocess_data import NUMERIC_COLUMNS, preprocess_dataset


def load_dataset() -> pd.DataFrame:
    if PROCESSED_DATASET.exists():
        return pd.read_csv(PROCESSED_DATASET)
    if DEFAULT_DATASET.exists():
        return preprocess_dataset(DEFAULT_DATASET)
    raise FileNotFoundError(
        f"Dataset not found at {DEFAULT_DATASET}. Place Crop_recommendation.csv there."
    )


def evaluate_saved_model(x_test, y_test, labels) -> None:
    model = joblib.load(MODEL_PATH)
    predictions = model.predict(x_test)
    matrix = confusion_matrix(y_test, predictions, labels=labels)

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        matrix,
        cmap="YlGnBu",
        xticklabels=labels,
        yticklabels=labels,
        annot=False,
    )
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORTS_DIR / "confusion_matrix.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def compare_models(x_train, x_test, y_train, y_test) -> dict:
    models = {
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "RandomForest": RandomForestClassifier(
            n_estimators=250, random_state=42, n_jobs=-1
        ),
    }

    results = {}
    for name, model in models.items():
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        results[name] = float(accuracy_score(y_test, predictions))

    labels = list(results.keys())
    scores = [results[label] for label in labels]

    plt.figure(figsize=(8, 5))
    sns.barplot(x=labels, y=scores, palette="Greens")
    plt.ylim(0, 1)
    plt.title("Model Accuracy Comparison")
    plt.ylabel("Accuracy")

    output_path = REPORTS_DIR / "model_accuracy_comparison.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    return results


def main() -> None:
    data = load_dataset()
    x = data[NUMERIC_COLUMNS]
    y = data["label"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    labels = sorted(y.unique())
    if MODEL_PATH.exists():
        evaluate_saved_model(x_test, y_test, labels)

    results = compare_models(x_train, x_test, y_train, y_test)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    metadata_path = REPORTS_DIR / "model_comparison.json"
    metadata_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Saved evaluation reports to {REPORTS_DIR}")


if __name__ == "__main__":
    main()
