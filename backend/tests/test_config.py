"""Tests for settings and schema contracts (Issue #3)."""

from app.config import Settings
from app.schemas.chat import ChatResponse, GroundedAnswer


def test_mcp_stream_url_composed() -> None:
    s = Settings(FI_MCP_BASE_URL="http://localhost:8080/", FI_MCP_STREAM_PATH="/mcp/stream")
    assert s.mcp_stream_url == "http://localhost:8080/mcp/stream"


def test_cors_origins_parsed() -> None:
    s = Settings(CORS_ALLOW_ORIGINS="http://a.com, http://b.com ,")
    assert s.cors_origins == ["http://a.com", "http://b.com"]


def test_chat_response_carries_disclaimer() -> None:
    resp = ChatResponse(
        session_id="mcp-session-x",
        persona="SIP Samurai",
        answer=GroundedAnswer(observation="net worth is stable"),
    )
    assert "not a financial advisor" in resp.disclaimer
