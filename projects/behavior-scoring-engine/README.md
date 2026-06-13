# Behavior Scoring Engine

## Goal

Predict multiple behavior labels from emails or text records with calibrated
thresholds, weak-label handling, and explainable review signals.

## Architecture Pattern

- Text normalization and feature extraction
- SentenceTransformer embeddings
- Per-behavior classifiers
- Approximate-nearest-neighbor retrieval for examples
- Class weighting for imbalanced behavior labels
- Confidence-based LLM fallback

## Evaluation

- Per-label precision, recall, and F1
- Threshold calibration by behavior
- Low-confidence routing
- Evidence snippets for reviewer trust
