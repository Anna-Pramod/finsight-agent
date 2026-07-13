"""Personas endpoint (GET /personas).

Lists selectable demo personas (name + scenario) so the frontend can offer a
persona picker without knowing upstream phone numbers.

Implemented in Issue #8.
"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.mcp.persona_mapping import list_personas

router = APIRouter(tags=["personas"])


class PersonaOut(BaseModel):
    name: str
    scenario: str


@router.get("/personas", response_model=list[PersonaOut])
def personas() -> list[PersonaOut]:
    """All selectable personas, in display order. Phone numbers stay server-side."""
    return [PersonaOut(name=p.name, scenario=p.scenario) for p in list_personas()]


__all__ = ["router"]
