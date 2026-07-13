"""Tests for the MCP client, session manager, and persona mapping (Issues #5, #8)."""

from typing import Any

import pytest

from app.agents.session_manager import SessionManager, make_session_id
from app.config import Settings
from app.mcp.fi_client import FiMcpClient, LoginRequired
from app.mcp.persona_mapping import list_personas, resolve_phone


class FakeTransport:
    """In-memory transport returning canned tool payloads (no Go server needed)."""

    def __init__(self, responses: dict[str, dict[str, Any]]) -> None:
        self.responses = responses
        self.calls: list[str] = []

    def call_tool(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(tool)
        return self.responses.get(tool, {})


def test_persona_resolution() -> None:
    assert resolve_phone("SIP Samurai") == "8888888888"
    assert resolve_phone("sip samurai") == "8888888888"  # case-insensitive
    assert len(list_personas()) == 16
    with pytest.raises(KeyError):
        resolve_phone("Nonexistent Persona")


def test_client_returns_tool_data() -> None:
    transport = FakeTransport({"fetch_net_worth": {"total_net_worth": 4200000}})
    client = FiMcpClient(transport)
    assert client.fetch_net_worth() == {"total_net_worth": 4200000}
    assert transport.calls == ["fetch_net_worth"]


def test_client_surfaces_login_required() -> None:
    transport = FakeTransport(
        {"fetch_credit_report": {"status": "login_required", "login_url": "http://x/login"}}
    )
    client = FiMcpClient(transport)
    with pytest.raises(LoginRequired) as exc:
        client.fetch_credit_report()
    assert exc.value.login_url == "http://x/login"


def test_session_id_is_prefixed_and_stable() -> None:
    sid = make_session_id("mcp-session-", "8888888888:SIP Samurai")
    assert sid.startswith("mcp-session-")
    assert sid == make_session_id("mcp-session-", "8888888888:SIP Samurai")


def test_session_manager_reuses_one_session() -> None:
    mgr = SessionManager(settings=Settings())
    a = mgr.get_or_create("SIP Samurai", "8888888888")
    b = mgr.get_or_create("SIP Samurai", "8888888888", session_id=a.session_id)
    assert a.session_id == b.session_id
    assert mgr.get(a.session_id) is a
