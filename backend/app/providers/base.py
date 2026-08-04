from __future__ import annotations

from abc import ABC, abstractmethod
from typing import AsyncGenerator, List


class BaseProvider(ABC):
    name: str

    @abstractmethod
    async def generate(self, messages: list[dict], model: str, temperature: float) -> str:
        raise NotImplementedError

    @abstractmethod
    async def stream(self, messages: list[dict], model: str, temperature: float) -> AsyncGenerator[str, None]:
        raise NotImplementedError

    @abstractmethod
    async def available_models(self) -> List[str]:
        raise NotImplementedError
