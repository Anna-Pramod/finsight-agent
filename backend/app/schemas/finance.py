"""Finance schemas.

Pydantic models for financial data (net worth, liabilities, mutual-fund / SIP,
credit) normalised from Fi MCP responses. These are the typed shape the agent
and workflow services reason over, independent of the raw MCP JSON.

Implemented incrementally in Issues #11-#14.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Money(BaseModel):
    """A currency amount. Fi MCP returns INR values; currency is explicit."""

    amount: float
    currency: str = "INR"


class NetWorth(BaseModel):
    """Normalised net-worth snapshot from ``fetch_net_worth``."""

    total: Money
    total_assets: Money
    total_liabilities: Money
    assets: dict[str, float] = Field(default_factory=dict)
    liabilities: dict[str, float] = Field(default_factory=dict)


class CreditReport(BaseModel):
    """Subset of ``fetch_credit_report`` used for risk scoring."""

    credit_score: int | None = None
    active_loans: int = 0
    total_outstanding: Money | None = None


class MutualFund(BaseModel):
    """A single mutual-fund / SIP holding derived from MF transactions."""

    name: str
    invested: Money
    current_value: Money
    xirr: float | None = None


__all__ = ["Money", "NetWorth", "CreditReport", "MutualFund"]
