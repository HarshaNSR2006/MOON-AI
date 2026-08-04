from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, constr


class MemoryCreate(BaseModel):
    content: str = Field(..., min_length=1)
    category: constr(strip_whitespace=True, min_length=1) = Field(default="general")
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    conversation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MemoryUpdate(BaseModel):
    content: Optional[str] = None
    category: Optional[str] = None
    importance: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None


class MemoryResponse(BaseModel):
    id: str
    content: str
    category: str
    importance: float
    timestamp: datetime
    conversation_id: Optional[str]
    metadata: Optional[Dict[str, Any]]


class MemorySearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None
    category: Optional[str] = None
    top_k: Optional[int] = Field(default=5, ge=1)


class MemorySearchResult(BaseModel):
    id: str
    content: str
    category: str
    importance: float
    timestamp: datetime
    conversation_id: Optional[str]
    metadata: Optional[Dict[str, Any]]
    similarity: Optional[float] = None


class ConversationMessageResponse(BaseModel):
    role: str
    content: str
    timestamp: datetime


class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    messages: List[ConversationMessageResponse]
