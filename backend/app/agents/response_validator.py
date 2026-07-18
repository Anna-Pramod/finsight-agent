"""Response safety/grounding validator.

Post-processes agent output before it reaches the user:

- blocks prompt-injection attempts (both in the question and echoed in output);
- blocks regulated-advice phrasing (guarantees, buy/sell instructions);
- requires that answers which quote figures actually ran tools (grounding);
- the disclaimer travels on every ChatResponse via its schema default.

This is a deterministic guardrail layered on top of the instruction-level
rules — defence in depth, and independently testable. Implemented in Issue #7.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.agents.root_agent import AgentTurnResult
from app.schemas.chat import GroundedAnswer

# Patterns that indicate the *question* is trying to subvert the agent.
# Checked against a normalised form of the text (see _canonical) so that
# leetspeak ("1gn0r3") and homoglyph tricks don't slip past.
INJECTION_PATTERNS = [
    r"ignore (all |any |your |previous |prior |the )*(instructions|rules|guidelines|prompt)",
    r"disregard (all |any |your |previous |prior |the )*(instructions|rules|safety|guidelines)",
    r"(reveal|show|print|repeat|translate|output|tell me) (me )?(your|the) (system |initial )?(prompt|instructions)",
    r"you are (now |)(no longer|a |an )",
    r"you are now\b",
    r"pretend (you are|to be|that)",
    r"act as (if|though|a different|an? )",
    r"roleplay as|role-play as",
    r"jailbreak",
    r"(developer|dev|god|admin|sudo) mode",
    r"(disable|turn off|bypass|switch off|remove) (your |the |all )?(safety|guardrails?|checks?|filters?|restrictions?|rules)",
    r"(no|without|zero) (restrictions?|rules|limits|filters|guardrails?)",
    r"fabricate|make up (the |some )?(data|numbers|figures)",
    r"guarantee (me )?(a |the )?(loan|approval|return)",
    r"as (the |a )?(developer|admin|owner)( of)?.{0,20}(authoris|authoriz|disable|enable|override)",
]

# Checked against a "despaced" form (all non-letters removed) to defeat
# character-spacing evasion like "i g n o r e   a l l   r u l e s".
DESPACED_PATTERNS = [
    r"ignore.{0,12}(instruction|rule|guideline|prompt)",
    r"disregard.{0,12}(instruction|rule|safety)",
    r"ignoreyour(rules|instructions)",
    r"(disable|bypass|turnoff|remove).{0,4}(safety|guardrail|check|filter|restriction|rule)",
    r"(developer|dev|god|admin|sudo)mode",
    r"you(are)?now(no|a|an)",
    r"no(restriction|rule|limit|filter|guardrail)",
    r"jailbreak",
    r"revealyour(prompt|instruction)",
    r"(repeat|reveal|show|print|output|translate).{0,20}(systemprompt|yourprompt|yourinstruction)",
]

# Leetspeak / common homoglyph substitutions folded back to letters.
_LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s", "|": "i"})

# Output phrasing that would cross the not-an-advisor line.
FORBIDDEN_OUTPUT_PATTERNS = [
    r"\bguaranteed? (approval|returns?|profit)",
    r"\byou (will|are certain to) (be approved|get the loan|profit)",
    r"\b(buy|sell|dump|short) (this|that|the|your) (stock|fund|share)",
    r"\byou should (buy|sell) \b",
    r"\bI (guarantee|promise)\b",
]

REFUSAL = GroundedAnswer(
    observation=(
        "I can't help with that request. It appears to ask me to ignore my "
        "safety and grounding rules (e.g. fabricate data, reveal instructions, "
        "or give guaranteed/regulated advice), which I won't do. I'm happy to "
        "answer questions grounded in your connected financial data."
    ),
    risk=None,
    suggested_next_step="Ask a question about your net worth, loans, SIPs, EPF, or transactions.",
)


@dataclass
class ValidationResult:
    answer: GroundedAnswer
    blocked: bool
    reason: str | None = None


def _canonical(question: str) -> str:
    """Lowercase and fold leetspeak/homoglyphs so evasions read as plain text."""
    return question.lower().translate(_LEET)


def _despace(question: str) -> str:
    """Strip everything but letters, defeating character-spacing evasion."""
    return re.sub(r"[^a-z]", "", _canonical(question))


def is_injection(question: str) -> bool:
    canonical = _canonical(question)
    if any(re.search(p, canonical) for p in INJECTION_PATTERNS):
        return True
    despaced = _despace(question)
    return any(re.search(p, despaced) for p in DESPACED_PATTERNS)


def validate_question(question: str) -> ValidationResult | None:
    """Pre-flight check. Returns a blocking result for injection attempts."""
    if is_injection(question):
        return ValidationResult(answer=REFUSAL, blocked=True, reason="prompt_injection")
    return None


def validate_response(result: AgentTurnResult) -> ValidationResult:
    """Post-hoc check of the agent's structured answer."""
    text = " ".join(
        filter(
            None,
            [
                result.answer.observation,
                result.answer.risk or "",
                result.answer.suggested_next_step or "",
            ],
        )
    ).lower()

    for pattern in FORBIDDEN_OUTPUT_PATTERNS:
        if re.search(pattern, text):
            return ValidationResult(
                answer=REFUSAL, blocked=True, reason=f"forbidden_output:{pattern}"
            )

    # Grounding: an answer quoting rupee figures must have called at least one tool.
    quotes_figures = bool(re.search(r"(₹|\binr\b|\brs\.?\s?\d)", text))
    if quotes_figures and not result.tools_called:
        return ValidationResult(
            answer=GroundedAnswer(
                observation=(
                    "I couldn't ground an answer in your connected data for this "
                    "question (no data tools were used), so I won't quote figures."
                ),
                suggested_next_step="Try rephrasing the question about your connected accounts.",
            ),
            blocked=True,
            reason="ungrounded_figures",
        )

    return ValidationResult(answer=result.answer, blocked=False)


__all__ = [
    "ValidationResult",
    "validate_question",
    "validate_response",
    "is_injection",
    "REFUSAL",
]
