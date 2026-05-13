import sys
from pathlib import Path

import pandas as pd

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BACKEND_DIR))

from app.utils.paths import DEFAULT_DATASET, PROCESSED_DATASET


NUMERIC_COLUMNS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
EXPECTED_COLUMNS = set(NUMERIC_COLUMNS + ["label"])


def validate_columns(dataframe: pd.DataFrame) -> None:
    missing = EXPECTED_COLUMNS - set(dataframe.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"Dataset missing required columns: {missing_list}")


def preprocess_dataset(dataset_path: Path) -> pd.DataFrame:
    dataframe = pd.read_csv(dataset_path)
    validate_columns(dataframe)

    dataframe[NUMERIC_COLUMNS] = dataframe[NUMERIC_COLUMNS].apply(
        pd.to_numeric, errors="coerce"
    )
    dataframe[NUMERIC_COLUMNS] = dataframe[NUMERIC_COLUMNS].fillna(
        dataframe[NUMERIC_COLUMNS].median()
    )

    if dataframe["label"].isna().any():
        dataframe["label"] = dataframe["label"].fillna(
            dataframe["label"].mode().iloc[0]
        )

    return dataframe


def main() -> None:
    dataset_path = Path(DEFAULT_DATASET)
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {dataset_path}. Place Crop_recommendation.csv there."
        )

    processed = preprocess_dataset(dataset_path)
    PROCESSED_DATASET.parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(PROCESSED_DATASET, index=False)
    print(f"Saved processed dataset to {PROCESSED_DATASET}")


if __name__ == "__main__":
    main()
