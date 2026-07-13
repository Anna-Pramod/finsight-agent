"""Tool-call trace capture.

Records which MCP tools were called, whether data came back, and how long each
call took — for the frontend trace panel and the audit log.

Implemented in Issue #10.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from app.schemas.audit import ToolCall


@dataclass
class ToolTraceRecorder:
    """Wraps a Transport, recording every call as a ToolCall."""

    inner: Any  # Transport
    calls: list[ToolCall] = field(default_factory=list)

    def call_tool(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        start = time.monotonic()
        try:
            data = self.inner.call_tool(tool, arguments)
        except Exception:
            self.calls.append(
                ToolCall(tool=tool, ok=False, duration_ms=_ms(start), data_present=False)
            )
            raise
        no_data = isinstance(data, dict) and data.get("status") == "no_data"
        self.calls.append(
            ToolCall(
                tool=tool,
                ok=True,
                duration_ms=_ms(start),
                data_present=not no_data,
                note=data.get("message") if no_data else None,
            )
        )
        return data


def _ms(start: float) -> int:
    return int((time.monotonic() - start) * 1000)


__all__ = ["ToolTraceRecorder"]
