import sys
from pathlib import Path

# Add src folder to Python path
SRC_PATH = Path(__file__).resolve().parent.parent / "src"

sys.path.insert(0, str(SRC_PATH))