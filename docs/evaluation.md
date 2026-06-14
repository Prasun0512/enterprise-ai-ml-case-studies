# Evaluation Strategy

Evaluation in this repository is intentionally lightweight, deterministic, and safe for a public portfolio. The goal is to show how enterprise AI systems should be measured without publishing private datasets or client benchmarks.

## What To Evaluate

- Extraction accuracy on sanitized examples.
- Classification threshold behavior.
- Retrieval recall, precision, and citation support.
- Confidence scoring and human-review routing.
- Redaction quality before logging, indexing, or LLM calls.
- Failure-mode handling for incomplete inputs.

## Local Checks

```bash
python -m unittest discover -s tests
python projects/genai-email-to-case/poc.py
python projects/prompt-rag-evaluation-suite/poc.py
```

## Release Gate Thinking

- Do not ship a prompt or extraction schema without regression examples.
- Track false positives, false negatives, missing fields, and review-rate changes.
- Treat low confidence as a workflow state, not a silent failure.
- Keep business metrics separate from public demo claims unless they are documented and safe to share.

## Future Improvements

- Add generated benchmark reports from sanitized examples.
- Add richer expected-output fixtures per case study.
- Add prompt/version metadata to every POC output.
