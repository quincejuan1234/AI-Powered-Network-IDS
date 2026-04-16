import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_PATH = PROJECT_ROOT / "app" / "app.py"

subprocess.run(["streamlit", "run", str(APP_PATH)], check=True)
