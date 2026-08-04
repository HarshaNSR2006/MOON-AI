from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List

HISTORY_PATH = Path(__file__).resolve().parents[2] / "logs" / "automation_history.json"


def read_history() -> List[Any]:
    if not HISTORY_PATH.exists():
        return []
    try:
        with HISTORY_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return []


def append_entry(entry: Any) -> None:
    data = read_history()
    data.append(entry)
    try:
        with HISTORY_PATH.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
    except Exception:
        pass
