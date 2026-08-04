from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

HISTORY_PATH = Path(__file__).resolve().parents[2] / "logs" / "agent_history.json"
HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)


def read_history() -> List[Dict[str, Any]]:
    if not HISTORY_PATH.exists():
        return []
    try:
        with HISTORY_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return []


def write_history(entries: List[Dict[str, Any]]) -> None:
    try:
        with HISTORY_PATH.open("w", encoding="utf-8") as handle:
            json.dump(entries, handle, indent=2)
    except Exception:
        pass
