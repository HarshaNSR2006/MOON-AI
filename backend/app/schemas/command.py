from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


class CommandStep(BaseModel):
    command: str = Field(..., min_length=1)
    args: Dict[str, Any] = Field(default_factory=dict)


class CommandPlan(BaseModel):
    steps: List[CommandStep] = Field(default_factory=list)


class CommandPlanRequest(BaseModel):
    query: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None


class CommandExecutionRequest(BaseModel):
    plan: Optional[CommandPlan] = None
    command: Optional[str] = None
    args: Dict[str, Any] = Field(default_factory=dict)
    conversation_id: Optional[str] = None
    allow_dangerous: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_request(self) -> "CommandExecutionRequest":
        if self.plan is None and self.command is None:
            raise ValueError("Either 'plan' or 'command' must be provided.")
        if self.plan is not None and self.command is not None:
            raise ValueError("Provide either 'plan' or 'command', not both.")
        return self


class CommandInfo(BaseModel):
    name: str
    description: str
    args: Optional[Dict[str, str]] = None


class CommandResult(BaseModel):
    success: bool
    command: str
    message: str
    data: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


class BatchCommandResult(BaseModel):
    success: bool
    results: List[CommandResult]
