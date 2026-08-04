import os
from pathlib import Path
from typing import Optional

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env", env_file_encoding="utf-8")

    app_name: str = Field(default="MOON AI")
    app_version: str = Field(default="1.0.0")

    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)
    debug: bool = Field(default=False)

    secret_key: str = Field()
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)

    openai_api_key: Optional[str] = Field(default=None)
    embedding_provider: str = Field(default="openai")
    default_provider: str = Field(default="openai")
    default_model: str = Field(default="gpt-4o")
    ollama_host: Optional[str] = Field(default="http://localhost:11434")
    chroma_path: str = Field(default="./database/chroma")
    max_context_messages: int = Field(default=20)
    memory_top_k: int = Field(default=5)
    max_short_memory: int = Field(default=20)
    memory_importance_threshold: float = Field(default=0.75)
    streaming_enabled: bool = Field(default=True)
    temperature: float = Field(default=0.7)
    database_url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./moon.db"))
    log_level: str = Field(default="INFO")
    cors_origins: str = Field(default="*")
    cors_allow_credentials: bool = Field(default=False)

    voice_wake_word: str = Field(default="moon")
    voice_language: str = Field(default="en")
    voice_name: str = Field(default="default")
    voice_speed: float = Field(default=1.0)
    stt_engine: str = Field(default="placeholder")
    tts_engine: str = Field(default="placeholder")
    voice_streaming: bool = Field(default=True)


settings = Settings()
