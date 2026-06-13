"""Threshold helpers for multi-label classification demos."""

from __future__ import annotations


def predict_labels(scores: dict[str, float], thresholds: dict[str, float]) -> list[str]:
    labels: list[str] = []
    for label, score in scores.items():
        threshold = thresholds.get(label, 0.5)
        if score >= threshold:
            labels.append(label)
    return labels


def low_confidence_labels(scores: dict[str, float], margin: float = 0.08) -> list[str]:
    review: list[str] = []
    for label, score in scores.items():
        distance_from_default = abs(score - 0.5)
        if distance_from_default <= margin:
            review.append(label)
    return review
