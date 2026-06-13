"""Small redaction helpers for sanitized AI demos."""

from __future__ import annotations

import re

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)")


def mask_email(text: str, replacement: str = "[EMAIL]") -> str:
    return EMAIL_PATTERN.sub(replacement, text)


def mask_phone(text: str, replacement: str = "[PHONE]") -> str:
    return PHONE_PATTERN.sub(replacement, text)


def mask_pii(text: str) -> str:
    """Apply conservative email and phone masking for demo pipelines."""
    return mask_phone(mask_email(text))
