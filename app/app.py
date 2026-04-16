import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Allow importing from src/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from config import FIGURES_DIR, METRICS_DIR, MODELS_DIR, MODEL_FILENAME
from predict import predict_from_dataframe
from utils import load_joblib, load_json


st.set_page_config(page_title="AI-Powered Network IDS", layout="wide")
st.title("🛡️ AI-Powered Network Intrusion Detection System")
st.write("Upload a CSV file and classify network traffic as benign or attack.")

artifact_path = MODELS_DIR / MODEL_FILENAME

if not artifact_path.exists():
    st.error("No trained model found. Run preprocess.py, train.py, and evaluate.py first.")
    st.stop()

artifact = load_joblib(artifact_path)
st.sidebar.header("Model Information")
st.sidebar.write(artifact.get("metadata", {}))
st.sidebar.write(f"Feature count: {len(artifact.get('feature_names', []))}")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Prediction")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Input preview:", df.head())

        result_df, _ = predict_from_dataframe(df, artifact_path=artifact_path)
        st.success("Prediction complete.")
        st.write(result_df.head(20))

        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download predictions as CSV",
            data=csv,
            file_name="predictions.csv",
            mime="text/csv",
        )
    else:
        st.info("Upload a CSV file to begin.")

with col2:
    st.subheader("Evaluation Artifacts")

    metrics_path = METRICS_DIR / "metrics.json"
    if metrics_path.exists():
        metrics = load_json(metrics_path)
        st.write(
            {
                "accuracy": round(metrics["accuracy"], 4),
                "precision": round(metrics["precision"], 4),
                "recall": round(metrics["recall"], 4),
                "f1_score": round(metrics["f1_score"], 4),
            }
        )

    cm_path = FIGURES_DIR / "confusion_matrix.png"
    if cm_path.exists():
        st.image(str(cm_path), caption="Confusion Matrix")

    fi_path = FIGURES_DIR / "feature_importance.png"
    if fi_path.exists():
        st.image(str(fi_path), caption="Feature Importance")
