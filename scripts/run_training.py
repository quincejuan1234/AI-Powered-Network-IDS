import sys
from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent

commands = [
    [sys.executable, str(PROJECT_ROOT / "src" / "preprocess.py")],
    [sys.executable, str(PROJECT_ROOT / "src" / "train.py")],
    [sys.executable, str(PROJECT_ROOT / "src" / "evaluate.py")],
]

for command in commands:
    print(f"[INFO] Running: {' '.join(command)}")
    subprocess.run(command, check=True)

print("[INFO] Full training pipeline completed successfully.")
