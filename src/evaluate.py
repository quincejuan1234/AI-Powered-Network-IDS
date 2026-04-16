from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from config import FIGURES_DIR, METRICS_DIR, MODELS_DIR, MODEL_FILENAME
from utils import load_joblib, save_json


def evaluate_model(model_artifact_path: Path) -> None:
    artifact = load_joblib(model_artifact_path)

    model = artifact["model"]
    x_test = artifact["x_test"]
    y_test = artifact["y_test"]

    y_pred = model.predict(x_test)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0),
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
    }

    save_json(metrics, METRICS_DIR / "metrics.json")

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Benign", "Attack"], yticklabels=["Benign", "Attack"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "confusion_matrix.png", dpi=200)
    plt.close()

    # Feature importance
    if hasattr(model, "feature_importances_"):
        feature_names = artifact["feature_names"]
        importances = model.feature_importances_

        pairs = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:15]
        names = [p[0] for p in pairs][::-1]
        values = [p[1] for p in pairs][::-1]

        plt.figure(figsize=(8, 6))
        plt.barh(names, values)
        plt.xlabel("Importance")
        plt.title("Top 15 Feature Importances")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "feature_importance.png", dpi=200)
        plt.close()

    print("[INFO] Evaluation complete.")
    print(f"[INFO] Metrics saved to: {METRICS_DIR / 'metrics.json'}")
    print(f"[INFO] Confusion matrix saved to: {FIGURES_DIR / 'confusion_matrix.png'}")


def main() -> None:
    model_artifact_path = MODELS_DIR / MODEL_FILENAME
    if not model_artifact_path.exists():
        raise FileNotFoundError(
            f"Model artifact not found: {model_artifact_path}. Run train.py first."
        )

    evaluate_model(model_artifact_path)


if __name__ == "__main__":
    main()
