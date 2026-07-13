"""Tests for affordability / EMI maths (Issue #12)."""

import pytest

from app.services.affordability import affordability_ratio, compute_emi


def test_emi_50l_20y_at_8_5() -> None:
    # ₹50L, 20 years, 8.5% p.a. — known value ≈ ₹43,391/mo
    res = compute_emi(5_000_000, 8.5, 240)
    assert res.emi == pytest.approx(43_391, abs=1)
    assert res.total_interest > 0
    assert any("not a loan offer" in a for a in res.assumptions)


def test_zero_rate_is_simple_division() -> None:
    assert compute_emi(120_000, 0.0, 12).emi == 10_000


def test_invalid_inputs_raise() -> None:
    with pytest.raises(ValueError):
        compute_emi(0, 8.5, 240)
    with pytest.raises(ValueError):
        affordability_ratio(1000, 0)


def test_affordability_ratio() -> None:
    assert affordability_ratio(40_000, 100_000) == 0.4
