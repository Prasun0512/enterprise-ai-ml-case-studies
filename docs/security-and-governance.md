# Security and Governance

This repository uses sanitized examples only. Do not place client data, private source code, credentials, tokens, connection strings, resumes, medical records, or production exports in this repo.

## Data Controls

- Redact PII before prompt construction, logging, indexing, or evaluation.
- Keep only the fields required for the demo workflow.
- Use `.env.example` for configuration shape and never commit `.env`.
- Treat generated outputs as review candidates when confidence is low.

## AI Governance

- Version prompts, schemas, and evaluation datasets together.
- Track model/provider, prompt version, retrieval parameters, and confidence scores.
- Route uncertain or high-risk outputs to human review.
- Keep case-study language clear that examples are sanitized and portfolio-safe.

## Security Review Checklist

- No real emails, resumes, medical documents, or customer records.
- No API keys, tokens, private endpoints, or internal hostnames.
- No fake production metrics or exaggerated business claims.
- No automated destructive actions in demo workflows.
- Tests cover redaction, confidence thresholds, and fallback behavior.

## Production Considerations

- Apply RBAC to case-study services and storage accounts.
- Use managed identity or a secret manager in real deployments.
- Add audit trails for all AI-assisted decisions.
- Use rate limits, budget controls, and abuse monitoring for LLM calls.
