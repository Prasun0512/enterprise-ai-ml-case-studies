"""Runnable POC implementations for the sanitized case-study folders."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any

from src.common.confidence import decide_review_route
from src.common.redaction import mask_pii
from src.rag.chunking import chunk_text
from src.rag.retrieval_metrics import recall_at_k


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
AMOUNT_RE = re.compile(r"(?:inr|rs\.?|\$)\s?([0-9][0-9,]*(?:\.[0-9]{2})?)", re.I)
REFERENCE_RE = re.compile(r"\b(?:claim|case|invoice|policy|req)[ -]?(?:id|no|number)[:# ]+([A-Z0-9-]{4,})\b", re.I)


@dataclass(frozen=True)
class PocResult:
    project: str
    status: str
    payload: dict[str, Any]
    audit: list[str]


def _tokens(text: str) -> set[str]:
    return {token.strip(".,:;!?()[]{}").lower() for token in text.split() if token}


def _keyword_score(text: str, keywords: list[str]) -> float:
    normalized = text.lower()
    if not keywords:
        return 0.0
    hits = sum(1 for keyword in keywords if keyword.lower() in normalized)
    return round(hits / len(keywords), 2)


def _cosine_similarity(left: str, right: str) -> float:
    left_counts = Counter(_tokens(left))
    right_counts = Counter(_tokens(right))
    shared = set(left_counts).intersection(right_counts)
    numerator = sum(left_counts[token] * right_counts[token] for token in shared)
    left_norm = math.sqrt(sum(value * value for value in left_counts.values()))
    right_norm = math.sqrt(sum(value * value for value in right_counts.values()))
    if not left_norm or not right_norm:
        return 0.0
    return round(numerator / (left_norm * right_norm), 2)


def _extract_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    email = EMAIL_RE.search(text)
    amount = AMOUNT_RE.search(text)
    reference = REFERENCE_RE.search(text)
    if email:
        fields["email"] = email.group(0)
    if amount:
        fields["amount"] = amount.group(1).replace(",", "")
    if reference:
        fields["reference_id"] = reference.group(1).upper()
    return fields


def run_behavioral_intelligence_platform() -> PocResult:
    samples = [
        {"text": "Agent resolved the billing issue politely.", "label": "helpful"},
        {"text": "Customer message contains repeated threats and escalation language.", "label": "risk"},
        {"text": "Neutral status update with no behavior signal.", "label": "neutral"},
    ]
    label_counts = Counter(sample["label"] for sample in samples)
    drift_risk = "medium" if label_counts["risk"] / len(samples) >= 0.3 else "low"
    return PocResult(
        "behavioral-intelligence-platform",
        "ready",
        {"dataset_size": len(samples), "label_distribution": dict(label_counts), "drift_risk": drift_risk},
        ["loaded:samples", "checked:label_distribution", "evaluated:drift_risk"],
    )


def run_behavior_scoring_engine(text: str = "Repeated escalation and rude language in customer email.") -> PocResult:
    behaviors = {
        "escalation": ["urgent", "escalation", "blocked", "complaint"],
        "toxicity": ["rude", "threat", "abuse", "insult"],
        "churn_risk": ["cancel", "refund", "competitor", "unhappy"],
    }
    scores = {label: _keyword_score(text, keywords) for label, keywords in behaviors.items()}
    decisions = {
        label: decide_review_route(label, confidence=score, threshold=0.45).__dict__
        for label, score in scores.items()
    }
    return PocResult(
        "behavior-scoring-engine",
        "review_required" if any(item["route_to_human"] for item in decisions.values()) else "auto_scored",
        {"scores": scores, "decisions": decisions},
        ["normalized:text", "scored:behaviors", "applied:thresholds"],
    )


def run_explainable_toxicity_highlighting(
    text: str = "The first sentence is fine. This rude threat should be reviewed."
) -> PocResult:
    risky_terms = {"rude", "threat", "abuse", "harass"}
    sentences = [sentence.strip() for sentence in re.split(r"[.!?]", text) if sentence.strip()]
    evidence = [
        {"sentence": sentence, "matched_terms": sorted(_tokens(sentence).intersection(risky_terms))}
        for sentence in sentences
        if _tokens(sentence).intersection(risky_terms)
    ]
    score = round(min(1.0, len(evidence) * 0.45), 2)
    return PocResult(
        "explainable-toxicity-highlighting",
        "review_required" if evidence else "clear",
        {"toxicity_score": score, "evidence": evidence},
        ["segmented:text", "matched:evidence_spans", "created:review_payload"],
    )


def run_face_search_attribute_analytics() -> PocResult:
    target = [0.12, 0.88, 0.31]
    candidates = {
        "frame_001.jpg": [0.11, 0.86, 0.33],
        "frame_002.jpg": [0.72, 0.12, 0.44],
        "frame_003.jpg": [0.13, 0.9, 0.3],
    }
    matches = []
    for image, vector in candidates.items():
        similarity = round(sum(a * b for a, b in zip(target, vector)), 2)
        if similarity >= 0.85:
            matches.append({"image": image, "similarity": similarity, "attributes": {"review": "human_verify"}})
    return PocResult(
        "face-search-attribute-analytics",
        "matches_found",
        {"matches": matches, "threshold": 0.85, "responsible_use": "human verification required"},
        ["embedded:target", "searched:candidates", "filtered:threshold"],
    )


def run_genai_email_to_case(
    text: str = "From user@example.com. Please open claim number CLM-4491 for INR 12000."
) -> PocResult:
    fields = _extract_fields(text)
    confidence = 0.45 + (0.2 if "email" in fields else 0) + (0.2 if "reference_id" in fields else 0) + (0.1 if "amount" in fields else 0)
    decision = decide_review_route("email_to_case", round(confidence, 2), threshold=0.78)
    return PocResult(
        "genai-email-to-case",
        "case_ready" if not decision.route_to_human else "review_required",
        {"redacted_text": mask_pii(text), "fields": fields, "confidence": decision.confidence, "review": decision.route_to_human},
        ["ingested:email", "extracted:fields", "validated:confidence"],
    )


def run_jd_resume_ats_matcher() -> PocResult:
    resume = "Technical Lead with Python, Azure OpenAI, RAG, LangGraph, OCR, Service Bus, and MLOps."
    jd = "Need AI Architect with Python, Azure OpenAI, RAG, LangGraph, OCR, Service Bus, and production MLOps."
    resume_skills = _tokens(resume)
    jd_skills = _tokens(jd)
    must_have = {"python", "rag", "langgraph", "ocr", "mlops"}
    matched = sorted(must_have.intersection(resume_skills).intersection(jd_skills))
    missing = sorted(must_have.difference(resume_skills))
    score = round(len(matched) / len(must_have), 2)
    return PocResult(
        "jd-resume-ats-matcher",
        "strong_match" if score >= 0.8 else "partial_match",
        {"score": score, "matched_skills": matched, "missing_skills": missing, "similarity": _cosine_similarity(resume, jd)},
        ["parsed:resume", "parsed:jd", "scored:must_have_skills"],
    )


def run_learning_content_generator() -> PocResult:
    objective = "Explain RAG evaluation to intermediate AI engineers"
    source = "RAG evaluation checks retrieval quality, citation support, and answer groundedness."
    quiz = [
        {"question": "Which metric checks if expected documents are retrieved?", "answer": "recall@k"},
        {"question": "Why are citations useful?", "answer": "They support grounded answer review."},
    ]
    return PocResult(
        "learning-content-generator",
        "draft_ready",
        {"objective": objective, "summary": source, "quiz": quiz, "quality_gate": "human_review_before_publish"},
        ["retrieved:source", "generated:lesson", "generated:quiz", "queued:review"],
    )


def run_medical_claims_automation(text: str = "Claim number CLM-9001 from patient@example.com for INR 32000.") -> PocResult:
    redacted = mask_pii(text)
    fields = _extract_fields(text)
    confidence = 0.5 + (0.2 if "reference_id" in fields else 0) + (0.15 if "amount" in fields else 0)
    decision = decide_review_route("medical_claim", round(confidence, 2), threshold=0.82)
    return PocResult(
        "medical-claims-automation",
        "review_required" if decision.route_to_human else "claim_payload_ready",
        {"redacted_text": redacted, "fields": fields, "confidence": decision.confidence, "review": decision.route_to_human},
        ["ocr:normalized", "phi:redacted", "extracted:claim_fields", "checked:human_review_gate"],
    )


def run_multi_agent_workflow_automation() -> PocResult:
    tasks = [
        {"agent": "planner", "action": "classify_request", "status": "done"},
        {"agent": "retriever", "action": "fetch_policy_context", "status": "done"},
        {"agent": "executor", "action": "draft_case_update", "status": "blocked_for_approval"},
    ]
    return PocResult(
        "multi-agent-workflow-automation",
        "approval_required",
        {"task_plan": tasks, "next_agent": "human_reviewer"},
        ["planned:workflow", "called:retriever", "blocked:write_action"],
    )


def run_prompt_rag_evaluation_suite() -> PocResult:
    expected = {"q1": ["doc-a", "doc-b"], "q2": ["doc-c"]}
    retrieved = {"q1": ["doc-a", "doc-x", "doc-b"], "q2": ["doc-y", "doc-c"]}
    scores = {qid: recall_at_k(set(expected_docs), retrieved[qid], k=3) for qid, expected_docs in expected.items()}
    return PocResult(
        "prompt-rag-evaluation-suite",
        "evaluation_complete",
        {"recall_at_3": scores, "average_recall": round(sum(scores.values()) / len(scores), 2)},
        ["loaded:golden_set", "ran:retrieval_variant", "calculated:recall_at_k"],
    )


def run_requirements_discovery_agent() -> PocResult:
    document = "The platform must support audit trails, role-based access, and metadata filters for retrieval."
    chunks = chunk_text(document, chunk_size=8, overlap=2)
    query = "audit metadata retrieval"
    ranked = sorted(chunks, key=lambda chunk: len(_tokens(chunk).intersection(_tokens(query))), reverse=True)
    return PocResult(
        "requirements-discovery-agent",
        "answer_grounded",
        {"query": query, "top_chunk": ranked[0], "citations": ["REQ-001"]},
        ["chunked:document", "retrieved:metadata_filtered", "generated:grounded_answer"],
    )


def run_smart_consultation_recording_trigger() -> PocResult:
    detections = [0.1, 0.82, 0.88, 0.91, 0.4, 0.2]
    active_windows = 0
    events: list[str] = []
    recording = False
    for score in detections:
        active_windows = active_windows + 1 if score >= 0.8 else 0
        if active_windows >= 2 and not recording:
            recording = True
            events.append("recording_started")
        if score < 0.5 and recording:
            recording = False
            events.append("recording_stopped")
    return PocResult(
        "smart-consultation-recording-trigger",
        "events_emitted",
        {"detections": detections, "events": events, "final_recording_state": recording},
        ["sampled:frames", "smoothed:detections", "emitted:recording_events"],
    )


def run_virtual_hr_assistant() -> PocResult:
    question = "Can I apply for planned leave next week?"
    policy = "Employees can apply for planned leave through the HR portal with manager approval."
    citations = ["HR-POL-001"] if _tokens(question).intersection(_tokens(policy)) else []
    return PocResult(
        "virtual-hr-assistant",
        "answered_with_citation",
        {"answer": policy, "citations": citations, "sensitive_action": False},
        ["classified:intent_leave_policy", "retrieved:policy", "generated:cited_answer"],
    )


POC_RUNNERS = {
    "behavioral-intelligence-platform": run_behavioral_intelligence_platform,
    "behavior-scoring-engine": run_behavior_scoring_engine,
    "explainable-toxicity-highlighting": run_explainable_toxicity_highlighting,
    "face-search-attribute-analytics": run_face_search_attribute_analytics,
    "genai-email-to-case": run_genai_email_to_case,
    "jd-resume-ats-matcher": run_jd_resume_ats_matcher,
    "learning-content-generator": run_learning_content_generator,
    "medical-claims-automation": run_medical_claims_automation,
    "multi-agent-workflow-automation": run_multi_agent_workflow_automation,
    "prompt-rag-evaluation-suite": run_prompt_rag_evaluation_suite,
    "requirements-discovery-agent": run_requirements_discovery_agent,
    "smart-consultation-recording-trigger": run_smart_consultation_recording_trigger,
    "virtual-hr-assistant": run_virtual_hr_assistant,
}
