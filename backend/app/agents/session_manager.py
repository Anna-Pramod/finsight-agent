"""Shared MCP session manager.

Owns ONE ``mcp-session-...`` id per demo session and reuses it across every
specialist agent and tool call, per the upstream requirement that a session is a
single client<->server connection logged in once (never one session per agent).

Session ids are derived deterministically from a seed (so they can be recreated
without a random source) and always carry the required ``mcp-session-`` prefix.

Implemented in Issue #5.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from app.config import Settings, get_settings


def make_session_id(prefix: str, seed: str) -> str:
    """Return a prefixed, stable session id for a given seed (e.g. phone+persona)."""
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]
    return f"{prefix}{digest}"


@dataclass
class DemoSession:
    """A single demo session: one persona, one shared MCP session id."""

    session_id: str
    persona: str
    phone: str
    logged_in: bool = False
    login_url: str | None = None


@dataclass
class SessionManager:
    """Creates and tracks demo sessions, one shared MCP session id each."""

    settings: Settings = field(default_factory=get_settings)
    _sessions: dict[str, DemoSession] = field(default_factory=dict)

    def get_or_create(self, persona: str, phone: str, session_id: str | None = None) -> DemoSession:
        if session_id and session_id in self._sessions:
            return self._sessions[session_id]
        sid = session_id or make_session_id(self.settings.mcp_session_prefix, f"{phone}:{persona}")
        session = self._sessions.get(sid) or DemoSession(session_id=sid, persona=persona, phone=phone)
        self._sessions[sid] = session
        return session

    def get(self, session_id: str) -> DemoSession | None:
        return self._sessions.get(session_id)


__all__ = ["make_session_id", "DemoSession", "SessionManager"]
