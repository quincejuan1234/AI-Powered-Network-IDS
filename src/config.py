from pathlib import Path

# Project root = parent of src/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SAMPLE_DIR = DATA_DIR / "sample"

MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
METRICS_DIR = OUTPUTS_DIR / "metrics"
REPORTS_DIR = OUTPUTS_DIR / "reports"

APP_DIR = PROJECT_ROOT / "app"

DEFAULT_RAW_FILENAME = None  # Set this if you want a fixed file name, e.g. "cicids2017_ddos.csv"
PROCESSED_FILENAME = "cicids2017_processed.csv"
MODEL_FILENAME = "random_forest_artifact.joblib"

RANDOM_STATE = 42
TEST_SIZE = 0.2
N_ESTIMATORS = 200

TARGET_COLUMN = "Label"
BENIGN_LABEL = "BENIGN"


def get_raw_data_path() -> Path:
    """
    Return the configured raw CSV path, or auto-detect the first CSV in data/raw.
    """
    if DEFAULT_RAW_FILENAME:
        path = RAW_DIR / DEFAULT_RAW_FILENAME
        if not path.exists():
            raise FileNotFoundError(f"Configured raw data file not found: {path}")
        return path

    csv_files = sorted(RAW_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DIR}. Put your CIC-IDS2017 subset there."
        )
    return csv_files[0]


def ensure_directories() -> None:
    for folder in [
        RAW_DIR,
        PROCESSED_DIR,
        SAMPLE_DIR,
        MODELS_DIR,
        FIGURES_DIR,
        METRICS_DIR,
        REPORTS_DIR,
    ]:
        folder.mkdir(parents=True, exist_ok=True)
