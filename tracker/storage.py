import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "progress.json"

def load_data():
    """Load habit data from JSON file."""
    if not DATA_FILE.exists():
        return {}
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """Save habit data to JSON file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)