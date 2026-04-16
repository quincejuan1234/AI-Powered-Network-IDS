from pathlib import Path
from typing import Tuple

import pandas as pd

from config import MODELS_DIR, MODEL_FILENAME, TARGET_COLUMN
from features import clean_column_names
from utils import load_joblib


def align_features(df: pd.DataFrame, feature_names: list[str]) -> pd.DataFrame:
    df = clean_column_names(df)

    if TARGET_COLUMN in df.columns:
        df = df.drop(columns=[TARGET_COLUMN])

    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

    missing_cols = [col for col in feature_names if col not in df.columns]
    for col in missing_cols:
        df[col] = 0

    extra_cols = [col for col in df.columns if col not in feature_names]
    if extra_cols:
        df = df.drop(columns=extra_cols)

    return df[feature_names]


def predict_from_dataframe(df: pd.DataFrame, artifact_path: Path | None = None) -> Tuple[pd.DataFrame, pd.Series]:
    artifact_path = artifact_path or (MODELS_DIR / MODEL_FILENAME)
    artifact = load_joblib(artifact_path)

    model = artifact["model"]
    feature_names = artifact["feature_names"]

    x = align_features(df, feature_names)

    predictions = model.predict(x)
    probabilities = None

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(x)[:, 1]

    result_df = df.copy()
    result_df["prediction"] = predictions
    result_df["prediction_label"] = result_df["prediction"].map({0: "BENIGN", 1: "ATTACK"})

    if probabilities is not None:
        result_df["attack_probability"] = probabilities

    return result_df, predictions


def main() -> None:
    sample_path = Path("data/sample/sample_input.csv")
    if not sample_path.exists():
        raise FileNotFoundError(
            f"Sample input not found: {sample_path}. "
            "Create one or use the Streamlit app."
        )

    df = pd.read_csv(sample_path)
    result_df, _ = predict_from_dataframe(df)
    print(result_df.head())


if __name__ == "__main__":
    main()
