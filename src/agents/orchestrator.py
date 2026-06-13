"""Minimal agentic tool-routing pattern for sanitized demos."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    run: Callable[[str], str]


class SimpleOrchestrator:
    def __init__(self, tools: list[Tool]) -> None:
        self.tools = {tool.name: tool for tool in tools}

    def route(self, intent: str) -> Tool:
        normalized = intent.lower()
        if "search" in normalized or "knowledge" in normalized:
            return self.tools["knowledge_search"]
        if "ticket" in normalized or "case" in normalized:
            return self.tools["case_creation"]
        return self.tools["human_review"]

    def run(self, intent: str, payload: str) -> str:
        tool = self.route(intent)
        return tool.run(payload)
