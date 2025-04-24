import json
from datetime import datetime
from pathlib import Path

HISTORY_FILE = "summary_history.json"

def save_history(text: str, summary: str, summary_type: str):
    history = []
    if Path(HISTORY_FILE).exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    
    history.append({
        "timestamp": datetime.now().isoformat(),
        "original": text[:200] + "..." if len(text) > 200 else text,
        "summary": summary,
        "type": summary_type
    })
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2) 