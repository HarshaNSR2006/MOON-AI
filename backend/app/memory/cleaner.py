from datetime import datetime, timezone
from typing import List

from app.memory.storage import MemoryStorage


class MemoryCleaner:
    def __init__(self, storage: MemoryStorage) -> None:
        self.storage = storage

    def prune_old_memories(self, days: int = 30) -> List[str]:
        cutoff = datetime.now(timezone.utc).timestamp() - days * 86400
        removed = []
        memories = self.storage.list_memories(limit=1000)
        for memory in memories:
            if memory.timestamp.timestamp() < cutoff:
                self.storage.delete_memory(memory.id)
                removed.append(memory.id)
        return removed
