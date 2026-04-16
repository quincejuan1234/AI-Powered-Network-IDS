from pathlib import Path

import pandas as pd

from config import (
    PROCESSED_DIR,
    PROCESSED_FILENAME,
    TARGET_COLUMN,
    BENIGN_LABEL,
    ensure_directories,
    get_raw_data_path,
)
from features import (
    clean_column_names,
    replace_infinite_and_drop_missing,
    encode_binary_label,
    keep_numeric_features,
)


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)

    if TARGET_COLUMN not in df.columns:
        raise KeyError(
            f"Target column '{TARGET_COLUMN}' not found after cleaning columns. "
            f"Available columns: {df.columns.tolist()}"
        )

    df = replace_infinite_and_drop_missing(df)
    df = encode_binary_label(df, TARGET_COLUMN, BENIGN_LABEL)
    df = keep_numeric_features(df, TARGET_COLUMN)

    if df.empty:
        raise ValueError("Processed dataframe is empty after cleaning. Check your raw dataset.")

    return df


def run_preprocessing(raw_path: Path, processed_path: Path) -> Path:
    print(f"[INFO] Loading raw data from: {raw_path}")
    df = pd.read_csv(raw_path)

    print(f"[INFO] Raw shape: {df.shape}")
    processed_df = preprocess_dataframe(df)
    print(f"[INFO] Processed shape: {processed_df.shape}")

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(processed_path, index=False)

    print(f"[INFO] Saved processed data to: {processed_path}")
    print(f"[INFO] Label distribution:\n{processed_df[TARGET_COLUMN].value_counts()}")

    return processed_path


def main() -> None:
    ensure_directories()
    raw_path = get_raw_data_path()
    processed_path = PROCESSED_DIR / PROCESSED_FILENAME
    run_preprocessing(raw_path, processed_path)


if __name__ == "__main__":
    main()
