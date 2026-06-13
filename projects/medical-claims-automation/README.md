# Medical Claims Automation

## Goal

Extract structured claim information from unstructured medical documents while
protecting PHI and enabling auditable case classification.

## Architecture Pattern

- PDF/image ingestion
- OCR and document layout extraction
- PHI/PII masking before model calls
- Entity extraction and normalization
- Case type classification
- Human review for low-confidence fields

## Safety Controls

- Redaction before logging
- Confidence scoring
- Audit trail from source span to extracted field
- Human approval for regulated decisions
