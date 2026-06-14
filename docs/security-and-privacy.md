# Security and Privacy

This document complements `docs/security-and-governance.md`.

## Public Portfolio Boundaries

- Use sanitized demo data only.
- Do not commit client source code, customer records, real emails, resumes, documents, credentials, tokens, internal URLs, or proprietary prompts.
- Do not invent fake production metrics.
- Mark private/internal implementations as sanitized architecture summaries.

## Privacy Controls

- Redact PII before prompt construction, logging, indexing, or sample output.
- Keep examples intentionally synthetic.
- Avoid storing unnecessary identifiers in examples and tests.
- Route uncertain or sensitive outputs to human review.

## Interview-Safe Positioning

Explain design patterns, tradeoffs, validation, and governance. Do not imply this repository contains production client implementations.
