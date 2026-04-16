from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from config import (
    MODELS_DIR,
    MODEL_FILENAME,
    PROCESSED_DIR,
    PROCESSED_FILENAME,
    RANDOM_STATE,
    TEST_SIZE,
    N_ESTIMATORS,
    TARGET_COLUMN,
)
from features import split_features_target, get_feature_names
from utils import save_joblib


def train_model(processed_path: Path, model_path: Path) -> Path:
    print(f"[INFO] Loading processed data from: {processed_path}")
    df = pd.read_csv(processed_path)

    x, y = split_features_target(df, TARGET_COLUMN)
    feature_names = get_feature_names(x)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=N_ESTIMATORS,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight="balanced",
    )

    print("[INFO] Training RandomForestClassifier...")
    model.fit(x_train, y_train)

    artifact = {
        "model": model,
        "feature_names": feature_names,
        "x_test": x_test,
        "y_test": y_test,
        "target_column": TARGET_COLUMN,
        "metadata": {
            "model_type": "RandomForestClassifier",
            "n_estimators": N_ESTIMATORS,
            "random_state": RANDOM_STATE,
            "test_size": TEST_SIZE,
        },
    }

    save_joblib(artifact, model_path)
    print(f"[INFO] Saved model artifact to: {model_path}")
    return model_path


def main() -> None:
    processed_path = PROCESSED_DIR / PROCESSED_FILENAME
    if not processed_path.exists():
        raise FileNotFoundError(
            f"Processed file not found: {processed_path}. Run preprocess.py first."
        )

    model_path = MODELS_DIR / MODEL_FILENAME
    train_model(processed_path, model_path)


if __name__ == "__main__":
    main()
