# Virtual HR Assistant and Candidate Screening

## Goal

Automate routine HR inquiries and assist candidate screening through controlled
LLM workflows integrated with enterprise HR systems.

## Architecture Pattern

- Intent classification for HR requests
- Retrieval over policy and FAQ documents
- Tool calls for approved HRIS data access
- Resume and assessment parsing for screening
- Escalation to HR staff for sensitive requests

## Governance

- Role-aware data access
- PII-aware prompts and logging
- Human review for hiring-sensitive decisions
- Policy citation requirements
