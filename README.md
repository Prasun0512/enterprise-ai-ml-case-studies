# Enterprise AI/ML Case Studies

Sanitized portfolio repository for major AI/ML, Generative AI, RAG, document
intelligence, agentic workflow, NLP, and computer-vision projects led or
architected by Prasun Kumar.

This repository does not contain client source code, private data, credentials,
or proprietary implementation details. It provides architecture summaries,
delivery patterns, and small reusable starter-code modules that demonstrate the
engineering approach behind the projects.

## Business Impact Framing

These case studies are written to explain how AI systems are designed for real
business workflows: reducing manual document processing, improving extraction
consistency, enabling grounded knowledge discovery, and routing uncertain or
high-risk decisions to humans.

## Architecture Decisions and Tradeoffs

- **Decision:** Use sanitized POCs and reusable starter modules instead of
  private client code.
- **Tradeoff:** The repo cannot show proprietary implementations, but it can show
  architecture judgment, governance patterns, and interview-defensible design.
- **Expected scale:** Patterns are written for enterprise workflows where document
  volume, review backlogs, retrieval quality, and system-of-record writes must be
  planned explicitly.
- **Cost strategy:** Prefer deterministic baselines, targeted LLM calls, storage
  lifecycle cleanup, and benchmark-driven model selection.
- **Security strategy:** Use redaction helpers, review gates, and no private data.
- **Operational strategy:** Validate every POC through tests and document
  production readiness, monitoring, and roadmap considerations.
- **Lessons learned:** A strong AI architecture portfolio should explain
  constraints and tradeoffs, not only list tools.

## Project Index

- [GenAI Email-to-Case Automation](projects/genai-email-to-case/)
- [Requirements Discovery Agent](projects/requirements-discovery-agent/)
- [Behavioral Intelligence Platform](projects/behavioral-intelligence-platform/)
- [AI Learning Content Generator](projects/learning-content-generator/)
- [Virtual HR Assistant and Candidate Screening](projects/virtual-hr-assistant/)
- [Multi-Agent Workflow Automation](projects/multi-agent-workflow-automation/)
- [Behavior Scoring Engine](projects/behavior-scoring-engine/)
- [Medical Claims Automation](projects/medical-claims-automation/)
- [JD-Resume ATS Matcher](projects/jd-resume-ats-matcher/)
- [Explainable Toxicity and Behavior Highlighting](projects/explainable-toxicity-highlighting/)
- [Smart Consultation Recording Trigger](projects/smart-consultation-recording-trigger/)
- [Face Search and Attribute Analytics](projects/face-search-attribute-analytics/)
- [Prompt and RAG Evaluation Suite](projects/prompt-rag-evaluation-suite/)

## Starter Code

- `src/common/redaction.py` - basic PII masking helpers for demos
- `src/common/confidence.py` - confidence scoring and review routing helpers
- `src/rag/chunking.py` - deterministic text chunking helper
- `src/rag/retrieval_metrics.py` - retrieval evaluation metrics
- `src/agents/orchestrator.py` - minimal tool-routing orchestration pattern
- `src/classification/thresholds.py` - multi-label threshold calibration helper
- `src/case_study_pocs.py` - runnable local POC logic for every case-study folder

## Run a Case-Study POC

Every folder under `projects/` includes a runnable `poc.py` file with sanitized
sample logic and structured output.

```bash
python projects/jd-resume-ats-matcher/poc.py
python projects/genai-email-to-case/poc.py
python -m unittest discover -s tests
docker compose up --build
```

## Engineering Maturity

- Dockerfile and `docker-compose.yml` for local POC execution
- GitHub Actions workflow for validating all case-study POCs
- `.env.example` for safe configuration hygiene
- Production readiness notes in `docs/production-readiness.md`
- Security, testing, scalability, cost, and roadmap considerations documented

## Suggested Use

Use these materials to discuss system design, AI governance, retrieval quality,
human-in-the-loop validation, and production delivery patterns during interviews
or client-facing architecture conversations.
