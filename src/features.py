from typing import List, Tuple

import numpy as np
import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip()
    return df


def replace_infinite_and_drop_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    return df


def encode_binary_label(df: pd.DataFrame, target_column: str, benign_label: str) -> pd.DataFrame:
    df = df.copy()
    df[target_column] = df[target_column].astype(str).str.strip()
    df[target_column] = df[target_column].apply(lambda x: 0 if x == benign_label else 1)
    return df


def keep_numeric_features(df: pd.DataFrame, target_column: str) -> pd.DataFrame:
    df = df.copy()

    feature_df = df.drop(columns=[target_column])
    numeric_df = feature_df.apply(pd.to_numeric, errors="coerce")
    numeric_df = numeric_df.dropna()

    aligned_target = df.loc[numeric_df.index, target_column]
    numeric_df[target_column] = aligned_target
    return numeric_df


def split_features_target(df: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
    x = df.drop(columns=[target_column])
    y = df[target_column]
    return x, y


def get_feature_names(x: pd.DataFrame) -> List[str]:
    return list(x.columns)
