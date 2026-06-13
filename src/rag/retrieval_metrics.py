"""Retrieval quality metrics for RAG experiments."""

from __future__ import annotations


def recall_at_k(expected_ids: set[str], retrieved_ids: list[str], k: int) -> float:
    if not expected_ids:
        return 0.0
    hits = expected_ids.intersection(retrieved_ids[:k])
    return len(hits) / len(expected_ids)


def precision_at_k(expected_ids: set[str], retrieved_ids: list[str], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be positive")
    if not retrieved_ids:
        return 0.0
    hits = expected_ids.intersection(retrieved_ids[:k])
    return len(hits) / min(k, len(retrieved_ids))


def reciprocal_rank(expected_ids: set[str], retrieved_ids: list[str]) -> float:
    for index, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in expected_ids:
            return 1 / index
    return 0.0
