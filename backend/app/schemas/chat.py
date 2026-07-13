"""Chat schemas.

Request/response models for the chat API. A response deliberately separates an
*observation* from a *risk* from a *suggested next step*, and always carries the
tool trace and a disclaimer — the grounding/safety contract of FinSight Agent.

Implemented in Issue #9.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.audit import ToolCall

DISCLAIMER = (
    "FinSight Agent is not a financial advisor. This is an educational, "
    "data-grounded observation based only on the connected demo data."
)


class ChatRequest(BaseModel):
    """A user question against a selected persona."""

    persona: str = Field(..., description="Persona name, e.g. 'SIP Samurai'.")
    question: str = Field(..., min_length=1)
    session_id: str | None = Field(
        default=None, description="Reuse an existing demo session if provided."
    )


class GroundedAnswer(BaseModel):
    """The structured answer body: observation / risk / next step."""

    observation: str
    risk: str | None = None
    suggested_next_step: str | None = None
    assumptions: list[str] = Field(default_factory=list)


class ChatResponse(BaseModel):
    """Full chat response including trace and disclosure."""

    session_id: str
    persona: str
    answer: GroundedAnswer
    tools_called: list[ToolCall] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)
    blocked: bool = False
    disclaimer: str = DISCLAIMER


__all__ = ["ChatRequest", "ChatResponse", "GroundedAnswer", "DISCLAIMER"]
