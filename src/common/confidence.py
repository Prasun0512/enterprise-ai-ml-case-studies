"""Confidence scoring helpers for human-in-the-loop workflows."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewDecision:
    label: str
    confidence: float
    route_to_human: bool
    reason: str


def decide_review_route(label: str, confidence: float, threshold: float = 0.78) -> ReviewDecision:
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")

    if confidence < threshold:
        return ReviewDecision(
            label=label,
            confidence=confidence,
            route_to_human=True,
            reason="below confidence threshold",
        )

    return ReviewDecision(
        label=label,
        confidence=confidence,
        route_to_human=False,
        reason="meets confidence threshold",
    )
