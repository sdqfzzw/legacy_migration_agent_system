from __future__ import annotations

from dataclasses import dataclass, field


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    ascii_chars = sum(1 for char in text if ord(char) < 128)
    non_ascii_chars = len(text) - ascii_chars
    return max(1, ascii_chars // 4 + non_ascii_chars)


@dataclass
class ContextBudget:
    scale_factor: int = 160
    events: list[dict] = field(default_factory=list)

    def record(self, stage: str, text: str) -> int:
        estimated = estimate_tokens(text) * self.scale_factor
        self.events.append({"stage": stage, "estimated_tokens": estimated})
        return estimated

    @property
    def total_estimated_tokens(self) -> int:
        return sum(event["estimated_tokens"] for event in self.events)

    def as_dict(self) -> dict:
        return {
            "total_estimated_tokens": self.total_estimated_tokens,
            "events": self.events,
            "note": "This estimates the context processed by full-repository scans, agent memory, logs, and review loops.",
        }

