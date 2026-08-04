import json
from typing import AsyncGenerator, List

import httpx

from app.ai.exceptions import AIProviderUnavailable
from app.core.config import settings
from app.providers.base import BaseProvider


OPENAI_COMPLETION_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODELS_URL = "https://api.openai.com/v1/models"


class OpenAIProvider(BaseProvider):
    name = "openai"

    def _headers(self) -> dict[str, str]:
        if not settings.openai_api_key:
            raise AIProviderUnavailable("OpenAI API key is not configured.")
        return {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }

    async def generate(self, messages: list[dict], model: str, temperature: float) -> str:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1024,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                OPENAI_COMPLETION_URL,
                headers=self._headers(),
                json=payload,
            )
            if response.status_code >= 400:
                raise AIProviderUnavailable(
                    f"OpenAI error {response.status_code}: {response.text}"
                )
            body = response.json()
            choices = body.get("choices", [])
            if not choices:
                raise AIProviderUnavailable("OpenAI returned an empty response.")
            return choices[0].get("message", {}).get("content", "").strip()

    async def stream(
        self, messages: list[dict], model: str, temperature: float
    ) -> AsyncGenerator[str, None]:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                OPENAI_COMPLETION_URL,
                headers=self._headers(),
                json=payload,
            ) as response:
                if response.status_code >= 400:
                    text = await response.aread()
                    raise AIProviderUnavailable(
                        f"OpenAI stream error {response.status_code}: {text.decode(errors='ignore')}"
                    )
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    if line.startswith("data:"):
                        raw = line[len("data:") :].strip()
                        if raw == "[DONE]":
                            break
                        try:
                            chunk = json.loads(raw)
                            delta = chunk["choices"][0].get("delta", {}).get("content", "")
                            if delta:
                                yield delta
                        except json.JSONDecodeError:
                            continue

    async def available_models(self) -> List[str]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                OPENAI_MODELS_URL,
                headers=self._headers(),
            )
            if response.status_code >= 400:
                raise AIProviderUnavailable(
                    f"OpenAI models error {response.status_code}: {response.text}"
                )
            body = response.json()
            return [item["id"] for item in body.get("data", []) if isinstance(item, dict)]
