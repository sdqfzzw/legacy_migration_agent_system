from __future__ import annotations

from dataclasses import dataclass, field

from .repository import RepositorySnapshot


@dataclass
class FileRisk:
    path: str
    level: str
    reasons: list[str] = field(default_factory=list)


def build_risk_map(snapshot: RepositorySnapshot) -> list[FileRisk]:
    risks: list[FileRisk] = []
    for source in snapshot.files:
        text = source.text.lower()
        reasons: list[str] = []
        if "failed" in text or "traceback" in text:
            reasons.append("contains failing regression evidence")
        if "legacy" in text or "todo" in text:
            reasons.append("contains legacy migration marker")
        if "customer_id" in text and "customer.id" in text:
            reasons.append("mentions old and new API shapes")
        if "calculate_invoice" in text:
            reasons.append("touches billing calculation boundary")

        if not reasons:
            continue
        level = "high" if len(reasons) >= 2 or "failed" in text else "medium"
        risks.append(FileRisk(path=source.path, level=level, reasons=reasons))
    return risks

