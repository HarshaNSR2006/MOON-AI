import json
from typing import AsyncGenerator, List

import httpx

from app.ai.exceptions import AIProviderUnavailable
from app.core.config import settings
from app.providers.base import BaseProvider


class OllamaProvider(BaseProvider):
    name = "ollama"

    def _host(self) -> str:
        if not settings.ollama_host:
            raise AIProviderUnavailable("OLLAMA_HOST is not configured.")
        return settings.ollama_host.rstrip("/")

    async def generate(self, messages: list[dict], model: str, temperature: float) -> str:
        url = f"{self._host()}/v1/chat/{model}"
        payload = {
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code >= 400:
                raise AIProviderUnavailable(
                    f"Ollama error {response.status_code}: {response.text}"
                )
            body = response.json()
            if "response" in body:
                return str(body["response"]).strip()
            if "choices" in body and body["choices"]:
                return str(body["choices"][0].get("message", {}).get("content", "")).strip()
            raise AIProviderUnavailable("Ollama returned an empty response.")

    async def stream(
        self, messages: list[dict], model: str, temperature: float
    ) -> AsyncGenerator[str, None]:
        url = f"{self._host()}/v1/chat/{model}"
        payload = {
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload) as response:
                if response.status_code >= 400:
                    text = await response.aread()
                    raise AIProviderUnavailable(
                        f"Ollama stream error {response.status_code}: {text.decode(errors='ignore')}"
                    )
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    if line.startswith("data:"):
                        raw = line[len("data:") :].strip()
                        if raw == "[DONE]":
                            break
                        try:
                            event = json.loads(raw)
                        except json.JSONDecodeError:
                            continue
                        if isinstance(event, dict):
                            text = event.get("response") or event.get("content")
                            if not text and "choices" in event:
                                choice = event["choices"][0]
                                text = choice.get("delta", {}).get("content")
                            if text:
                                yield str(text)

    async def available_models(self) -> List[str]:
        url = f"{self._host()}/v1/models"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            if response.status_code >= 400:
                raise AIProviderUnavailable(
                    f"Ollama models error {response.status_code}: {response.text}"
                )
            body = response.json()
            if isinstance(body, dict) and "models" in body:
                return [item.get("name") for item in body["models"] if isinstance(item, dict)]
            if isinstance(body, list):
                return [item.get("name") for item in body if isinstance(item, dict)]
            return []
