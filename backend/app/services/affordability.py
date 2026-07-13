"""Affordability / EMI maths.

Deterministic EMI and affordability arithmetic with explicit assumptions —
used to cross-check or enrich agent answers, never to promise approval.

Implemented in Issue #12.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EmiResult:
    principal: float
    annual_rate_pct: float
    tenure_months: int
    emi: float
    total_interest: float
    assumptions: list[str] = field(default_factory=list)


def compute_emi(principal: float, annual_rate_pct: float, tenure_months: int) -> EmiResult:
    """Standard reducing-balance EMI: P*r*(1+r)^n / ((1+r)^n - 1)."""
    if principal <= 0 or tenure_months <= 0:
        raise ValueError("principal and tenure must be positive")
    r = annual_rate_pct / 12 / 100
    if r == 0:
        emi = principal / tenure_months
    else:
        f = (1 + r) ** tenure_months
        emi = principal * r * f / (f - 1)
    return EmiResult(
        principal=principal,
        annual_rate_pct=annual_rate_pct,
        tenure_months=tenure_months,
        emi=round(emi, 2),
        total_interest=round(emi * tenure_months - principal, 2),
        assumptions=[
            f"Assumed interest rate: {annual_rate_pct}% p.a. (reducing balance)",
            f"Assumed tenure: {tenure_months} months",
            "This is an educational simulation, not a loan offer or approval.",
        ],
    )


def affordability_ratio(emi: float, monthly_inflow: float) -> float:
    """EMI as a fraction of monthly inflow (lenders commonly cap near 0.4-0.5)."""
    if monthly_inflow <= 0:
        raise ValueError("monthly inflow must be positive")
    return round(emi / monthly_inflow, 4)


__all__ = ["EmiResult", "compute_emi", "affordability_ratio"]
