"""Numeric provenance.

Verifies that every *monetary* figure an answer quotes actually traces back to a
number in the retrieved tool payloads — turning "the model probably read the data"
into "each figure is checked against the data".

Design choices that keep the false-positive rate low:

- Only figures with a currency marker (₹ / Rs / INR) or a lakh/crore/k suffix are
  checked. Bare numbers, percentages, XIRRs and counts are ignored — they are
  derived or non-monetary, not claims about an amount on file.
- The "supported set" is built from the payloads' leaf numbers, their pairwise
  sums, and per-payload grand totals — because answers legitimately quote
  aggregates (total assets, total invested) that are sums of leaves.
- Matching uses a relative tolerance (default 1.5%) so a model rounding
  ₹11,35,627 to "₹11.36L" still verifies.

Unsupported figures are always recorded; the caller decides whether a *majority*
of unsupported monetary figures should block the answer (strong fabrication
signal) versus merely being surfaced in the audit trail.
"""

from __future__ import annotations

import re
from itertools import combinations
from typing import Any

# A monetary figure: optional currency marker, a number, optional scale suffix.
_MONEY_RE = re.compile(
    r"(?P<cur>₹|\brs\.?\s?|\binr\s?)?\s*"
    r"(?P<num>\d[\d,]*(?:\.\d+)?)"
    r"\s*(?P<suf>cr(?:ores?)?|lakhs?|l|k)?\b",
    re.IGNORECASE,
)

_SCALE = {"cr": 1e7, "crore": 1e7, "crores": 1e7, "l": 1e5, "lakh": 1e5, "lakhs": 1e5, "k": 1e3}


def _scale_of(suffix: str) -> float:
    return _SCALE.get(suffix.lower(), 1.0) if suffix else 1.0


def extract_monetary_figures(text: str) -> list[float]:
    """Return the numeric values of figures that are explicitly monetary."""
    figures: list[float] = []
    for m in _MONEY_RE.finditer(text):
        cur, num, suf = m.group("cur"), m.group("num"), m.group("suf")
        if not cur and not suf:
            continue  # bare number / percentage / count — not a monetary claim
        try:
            figures.append(float(num.replace(",", "")) * _scale_of(suf or ""))
        except ValueError:
            continue
    return figures


def _leaf_numbers(obj: Any, out: set[float]) -> None:
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        out.add(float(obj))
    elif isinstance(obj, str):
        s = obj.replace(",", "").strip()
        if re.fullmatch(r"-?\d+(?:\.\d+)?", s):
            out.add(float(s))
    elif isinstance(obj, dict):
        for v in obj.values():
            _leaf_numbers(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _leaf_numbers(v, out)


def supported_universe(payloads: list[dict[str, Any]], max_leaves_for_sums: int = 40) -> set[float]:
    """Numbers an answer may legitimately quote: leaves, pairwise sums, grand total."""
    leaves: set[float] = set()
    for p in payloads:
        _leaf_numbers(p, leaves)
    universe = set(leaves)
    # Monetary leaves only (>= 100) for aggregation, capped so this stays cheap.
    money_leaves = sorted({x for x in leaves if abs(x) >= 100})[:max_leaves_for_sums]
    for a, b in combinations(money_leaves, 2):
        universe.add(a + b)
    if money_leaves:
        universe.add(sum(money_leaves))
    return universe


def unverified_figures(
    answer_text: str, payloads: list[dict[str, Any]], tol: float = 0.015
) -> list[float]:
    """Monetary figures in the answer with no support in the payloads."""
    universe = supported_universe(payloads)
    unverified: list[float] = []
    for fig in extract_monetary_figures(answer_text):
        if fig == 0:
            continue
        ok = any(abs(fig - u) <= max(tol * max(abs(fig), abs(u)), 1.0) for u in universe)
        if not ok:
            unverified.append(fig)
    return unverified


__all__ = ["extract_monetary_figures", "supported_universe", "unverified_figures"]
