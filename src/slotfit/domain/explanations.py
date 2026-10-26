"""Plain-language explanations for eligibility reason codes.

The copy is written for a scheduling coordinator, not for an engineer. It must
never describe audit-only slices, bands or demographic attributes, because the
decision surface may not look slice-aware.
"""

from __future__ import annotations

from types import MappingProxyType

from slotfit.domain.model import CandidateEvaluation

ELIGIBLE_EXPLANATION = "This request can take this opening."

_EXPLANATIONS = MappingProxyType(
    {
        "NO_COMMUNICATION_CONSENT": "This request has not agreed to be contacted.",
        "PROVIDER_NOT_ELIGIBLE": "This opening is with a provider this request cannot see.",
        "REQUIRED_ROOM_UNAVAILABLE": "This request needs a room that is not available today.",
        "DURATION_EXCEEDS_INTERVAL": "This request needs more time than the opening offers.",
        "INSUFFICIENT_NOTICE": "This opening starts sooner than the notice this request needs.",
        "REQUEST_NOT_AVAILABLE": "This request is not available at this time.",
    }
)

REASON_CODES: tuple[str, ...] = tuple(_EXPLANATIONS)


def explain(reason_code: str) -> str:
    """Return the sentence for one reason code; unknown codes raise KeyError."""

    return _EXPLANATIONS[reason_code]


def explain_evaluation(evaluation: CandidateEvaluation) -> tuple[str, ...]:
    """Return one sentence per reason code, or the eligible sentence."""

    if evaluation.eligible:
        return (ELIGIBLE_EXPLANATION,)
    return tuple(explain(code) for code in evaluation.reason_codes)
