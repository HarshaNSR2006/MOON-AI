import asyncio

from app.ai.manager import AIManager
from app.ai.models import AIRequest, AIResponse
from app.providers.base import BaseProvider


class DummyProvider(BaseProvider):
    name = "dummy"

    async def generate(self, messages: list[dict], model: str, temperature: float) -> str:
        return "dummy response"

    async def stream(self, messages: list[dict], model: str, temperature: float):
        yield "dummy"
        yield " response"

    async def available_models(self) -> list[str]:
        return ["dummy-model"]


def test_ai_manager_generate_returns_response() -> None:
    manager = AIManager(providers=[DummyProvider()])
    manager.default_provider = "dummy"
    manager.default_model = "dummy-model"

    request = AIRequest(
        conversation_id="test-convo",
        message="hello world",
        provider="dummy",
    )

    response = asyncio.run(manager.generate(request))
    assert isinstance(response, AIResponse)
    assert response.response == "dummy response"
    assert response.provider == "dummy"
    assert response.model == "dummy-model"


def test_ai_manager_stream_yields_chunks() -> None:
    manager = AIManager(providers=[DummyProvider()])
    manager.default_provider = "dummy"
    manager.default_model = "dummy-model"

    request = AIRequest(
        conversation_id="test-stream",
        message="stream please",
        provider="dummy",
    )

    async def _collect() -> list[str]:
        chunks = []
        async for part in await manager.stream(request):
            chunks.append(part)
        return chunks

    chunks = asyncio.run(_collect())
    assert chunks == ["dummy", " response"]
