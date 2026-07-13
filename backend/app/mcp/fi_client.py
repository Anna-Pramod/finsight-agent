"""Fi MCP Dev client wrapper.

A thin client over the upstream ``epiFi/fi-mcp-dev`` server. It speaks to the
``/mcp/stream`` endpoint using a shared ``Mcp-Session-Id`` and exposes the six
confirmed tools as methods.

The tool-calling transport is abstracted behind the ``Transport`` protocol so
the agent/service layers and tests can run without a live Go server (inject a
fake transport). ``HttpStreamTransport`` is the real implementation.

A ``login_required`` response is surfaced as ``LoginRequired`` rather than raised
as a generic error, so the API layer can hand the login URL to the frontend.

Implemented in Issue #5.
"""

from __future__ import annotations

import json
from typing import Any, Protocol, runtime_checkable

import httpx

TOOLS = (
    "fetch_net_worth",
    "fetch_credit_report",
    "fetch_epf_details",
    "fetch_mf_transactions",
    "fetch_bank_transactions",
    "fetch_stock_transactions",
)


class LoginRequired(Exception):
    """Raised/carried when the MCP server needs a (dummy) login first."""

    def __init__(self, login_url: str) -> None:
        super().__init__(f"login required: {login_url}")
        self.login_url = login_url


@runtime_checkable
class Transport(Protocol):
    """Abstracts one MCP tool call. Implementations own the wire protocol."""

    def call_tool(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]: ...


class HttpStreamTransport:
    """Real transport: JSON-RPC ``tools/call`` over the streamable HTTP endpoint.

    Uses a fixed session id (prefixed ``mcp-session-`` per upstream requirement)
    passed via the ``Mcp-Session-Id`` header so every call reuses one session.
    """

    def __init__(self, stream_url: str, session_id: str, client: httpx.Client | None = None) -> None:
        self._url = stream_url
        self._session_id = session_id
        self._client = client or httpx.Client(timeout=30.0)

    def call_tool(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": tool, "arguments": arguments},
        }
        resp = self._client.post(
            self._url,
            json=payload,
            headers={
                "Mcp-Session-Id": self._session_id,
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
        )
        resp.raise_for_status()
        return _parse_tool_result(resp.text)


def _parse_tool_result(raw: str) -> dict[str, Any]:
    """Parse an MCP tool result body (JSON or SSE ``data:`` frame) to a dict."""
    text = raw.strip()
    if text.startswith("event:") or text.startswith("data:"):
        for line in text.splitlines():
            if line.startswith("data:"):
                text = line[len("data:") :].strip()
                break
    envelope = json.loads(text)
    # MCP wraps tool output in result.content[].text (usually a JSON string).
    result = envelope.get("result", envelope)
    content = result.get("content")
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                inner = part.get("text", "")
                try:
                    return json.loads(inner)
                except (json.JSONDecodeError, TypeError):
                    return {"text": inner}
    return result if isinstance(result, dict) else {"result": result}


class FiMcpClient:
    """Typed facade over the six Fi MCP tools using a shared transport."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def _call(self, tool: str, **arguments: Any) -> dict[str, Any]:
        data = self._transport.call_tool(tool, arguments)
        if isinstance(data, dict) and data.get("status") == "login_required":
            raise LoginRequired(data.get("login_url", ""))
        return data

    def fetch_net_worth(self) -> dict[str, Any]:
        return self._call("fetch_net_worth")

    def fetch_credit_report(self) -> dict[str, Any]:
        return self._call("fetch_credit_report")

    def fetch_epf_details(self) -> dict[str, Any]:
        return self._call("fetch_epf_details")

    def fetch_mf_transactions(self) -> dict[str, Any]:
        return self._call("fetch_mf_transactions")

    def fetch_bank_transactions(self) -> dict[str, Any]:
        return self._call("fetch_bank_transactions")

    def fetch_stock_transactions(self) -> dict[str, Any]:
        return self._call("fetch_stock_transactions")


__all__ = [
    "TOOLS",
    "LoginRequired",
    "Transport",
    "HttpStreamTransport",
    "FiMcpClient",
]
