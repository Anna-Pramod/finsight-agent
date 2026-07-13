"""Audit schemas.

Pydantic models for the audit / tool-trace records that make every answer
inspectable: which MCP tools ran, what data came back, and what was missing.

Implemented in Issue #10.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """A single MCP tool invocation captured for the trace panel."""

    tool: str
    ok: bool = True
    duration_ms: int | None = None
    data_present: bool = True
    note: str | None = None


class AuditRecord(BaseModel):
    """The audit trail for one chat turn."""

    session_id: str
    persona: str
    question: str
    tools_called: list[ToolCall] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)
    blocked: bool = False


__all__ = ["ToolCall", "AuditRecord"]
