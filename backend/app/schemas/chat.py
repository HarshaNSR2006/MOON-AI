from typing import List, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    conversation_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    provider: Optional[str] = Field(default=None)
    model: Optional[str] = Field(default=None)
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    provider: str
    model: str


class ModelListResponse(BaseModel):
    provider: str
    models: List[str]


class ModelSelectionRequest(BaseModel):
    provider: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)


class ModelSelectionResponse(BaseModel):
    provider: str
    model: str
