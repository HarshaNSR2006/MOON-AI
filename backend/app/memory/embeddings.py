import httpx

from app.ai.exceptions import AIProviderUnavailable
from app.core.config import settings


OPENAI_EMBEDDING_URL = "https://api.openai.com/v1/embeddings"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


class EmbeddingGenerator:
    def __init__(self) -> None:
        self.provider = settings.embedding_provider

    async def embed_text(self, text: str) -> list[float]:
        if self.provider != "openai":
            raise AIProviderUnavailable(
                f"Embedding provider '{self.provider}' is not supported." 
            )
        return await self._embed_openai(text)

    async def _embed_openai(self, text: str) -> list[float]:
        if not settings.openai_api_key:
            raise AIProviderUnavailable("OpenAI API key is not configured for embeddings.")

        payload = {
            "model": DEFAULT_EMBEDDING_MODEL,
            "input": text,
        }
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(OPENAI_EMBEDDING_URL, json=payload, headers=headers)
            if response.status_code >= 400:
                raise AIProviderUnavailable(
                    f"OpenAI embedding error {response.status_code}: {response.text}"
                )
            body = response.json()
            data = body.get("data")
            if not data or not isinstance(data, list):
                raise AIProviderUnavailable("OpenAI embedding response was empty.")
            return data[0].get("embedding", [])
