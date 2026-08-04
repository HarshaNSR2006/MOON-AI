from datetime import datetime, timezone


def rank_memory(score: float, importance: float, timestamp: str) -> float:
    try:
        created = datetime.fromisoformat(timestamp)
    except Exception:
        created = datetime.now(timezone.utc)
    age_seconds = max(0.0, (datetime.now(timezone.utc) - created).total_seconds())
    recency_score = max(0.0, 1.0 - age_seconds / 86400.0)
    return score * 0.6 + importance * 0.3 + recency_score * 0.1
