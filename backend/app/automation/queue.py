from __future__ import annotations

from collections import deque
from typing import Deque, Optional


class QueueManager:
    def __init__(self) -> None:
        self._queue: Deque[str] = deque()

    def enqueue(self, task_id: str) -> None:
        self._queue.append(task_id)

    def dequeue(self) -> Optional[str]:
        if not self._queue:
            return None
        return self._queue.popleft()

    def list(self) -> list[str]:
        return list(self._queue)


queue_manager = QueueManager()
