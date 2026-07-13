"""Persona <-> phone mapping.

Maps human-readable persona names (e.g. 'SIP Samurai') to Fi MCP Dev test phone
numbers (e.g. 8888888888). The frontend selects a persona by name; the backend
resolves it to the phone number the upstream server keys its ``test_data_dir``
on. Source table: docs/fi-mcp-integration.md (verified upstream 2026-06-24).

Implemented in Issue #8.
"""

from __future__ import annotations

from pydantic import BaseModel


class Persona(BaseModel):
    """A selectable demo persona backed by an upstream test data directory."""

    name: str
    phone: str
    scenario: str


# Order here is the display order in the frontend persona selector.
PERSONAS: list[Persona] = [
    Persona(name="No Assets", phone="1111111111", scenario="Savings balance only; no assets connected"),
    Persona(name="Portfolio Heavyweight", phone="2222222222", scenario="All assets connected; large MF portfolio (9 funds)"),
    Persona(name="Lean Investor", phone="3333333333", scenario="All assets connected; small MF portfolio (1 fund)"),
    Persona(name="Multi-Account Juggler", phone="4444444444", scenario="All assets; 2 UANs, 3 banks, txns for 2 accounts"),
    Persona(name="No Credit Score", phone="5555555555", scenario="All assets except credit score"),
    Persona(name="No Bank Account", phone="6666666666", scenario="All assets except bank account; large MF portfolio"),
    Persona(name="Debt-Heavy Low Performer", phone="7777777777", scenario="High liabilities, underperforming"),
    Persona(name="SIP Samurai", phone="8888888888", scenario="Disciplined SIP investor"),
    Persona(name="Fixed Income Fanatic", phone="9999999999", scenario="Conservative, fixed-income heavy"),
    Persona(name="Precious Metal Believer", phone="1010101010", scenario="Gold-heavy allocation"),
    Persona(name="Dormant EPF Earner", phone="1212121212", scenario="Idle EPF, little activity"),
    Persona(name="Balanced Growth Tracker", phone="1313131313", scenario="Diversified, balanced growth"),
    Persona(name="Salary Sinkhole", phone="1414141414", scenario="Salary in, little retained"),
    Persona(name="Starter Saver", phone="2020202020", scenario="Early-stage saver"),
    Persona(name="Dual Income Dynamo", phone="2121212121", scenario="Two incomes, strong savings"),
    Persona(name="Live-for-Today Spender", phone="2525252525", scenario="High spend, low savings"),
]

_BY_NAME = {p.name.lower(): p for p in PERSONAS}
_BY_PHONE = {p.phone: p for p in PERSONAS}


def resolve_phone(persona_name: str) -> str:
    """Return the Fi MCP phone number for a persona name (case-insensitive)."""
    persona = _BY_NAME.get(persona_name.strip().lower())
    if persona is None:
        raise KeyError(f"Unknown persona: {persona_name!r}")
    return persona.phone


def get_persona(persona_name: str) -> Persona:
    persona = _BY_NAME.get(persona_name.strip().lower())
    if persona is None:
        raise KeyError(f"Unknown persona: {persona_name!r}")
    return persona


def list_personas() -> list[Persona]:
    return list(PERSONAS)


__all__ = ["Persona", "PERSONAS", "resolve_phone", "get_persona", "list_personas"]
