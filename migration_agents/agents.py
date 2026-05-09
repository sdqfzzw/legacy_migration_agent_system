from __future__ import annotations

from dataclasses import dataclass

from .context_budget import ContextBudget
from .dependency_graph import DependencyGraph
from .repository import RepositorySnapshot
from .risk_map import FileRisk


@dataclass
class AgentResult:
    round: int
    agent: str
    finding: str
    actions: list[str]
    blockers: list[str]


class MigrationAgent:
    name = "MigrationAgent"

    def run(
        self,
        round_index: int,
        snapshot: RepositorySnapshot,
        graph: DependencyGraph,
        risks: list[FileRisk],
        memory: list[AgentResult],
        budget: ContextBudget,
    ) -> AgentResult:
        prompt_context = self._prompt_context(snapshot, graph, risks, memory)
        budget.record(f"round_{round_index}.{self.name}.context", prompt_context)
        result = self.analyze(round_index, snapshot, graph, risks, memory)
        budget.record(f"round_{round_index}.{self.name}.result", str(result))
        return result

    def _prompt_context(
        self,
        snapshot: RepositorySnapshot,
        graph: DependencyGraph,
        risks: list[FileRisk],
        memory: list[AgentResult],
    ) -> str:
        return "\n".join(
            [
                snapshot.full_context,
                str(graph.as_dict()),
                str([risk.__dict__ for risk in risks]),
                str([item.__dict__ for item in memory]),
            ]
        )

    def analyze(
        self,
        round_index: int,
        snapshot: RepositorySnapshot,
        graph: DependencyGraph,
        risks: list[FileRisk],
        memory: list[AgentResult],
    ) -> AgentResult:
        raise NotImplementedError


class ApiCompatibilityAgent(MigrationAgent):
    name = "ApiCompatibilityAgent"

    def analyze(self, round_index, snapshot, graph, risks, memory) -> AgentResult:
        return AgentResult(
            round=round_index,
            agent=self.name,
            finding="The public API must accept both root customer_id and nested customer.id during migration.",
            actions=[
                "Introduce a payload normalization adapter before billing is called.",
                "Keep create_invoice response fields stable for downstream clients.",
            ],
            blockers=["Missing characterization test for nested customer.id payload."],
        )


class RefactorPlanningAgent(MigrationAgent):
    name = "RefactorPlanningAgent"

    def analyze(self, round_index, snapshot, graph, risks, memory) -> AgentResult:
        high_risk = [risk.path for risk in risks if risk.level == "high"]
        return AgentResult(
            round=round_index,
            agent=self.name,
            finding=f"Refactor should be staged around high-risk files: {high_risk}.",
            actions=[
                "Add normalize_customer_payload(payload) as an adapter layer.",
                "Move billing edge cases behind tests before changing calculation code.",
                "Apply migration in small patches and rerun regression logs after every patch.",
            ],
            blockers=[],
        )


class TestSynthesisAgent(MigrationAgent):
    name = "TestSynthesisAgent"

    def analyze(self, round_index, snapshot, graph, risks, memory) -> AgentResult:
        failures = [file.text for file in snapshot.files if file.path.endswith(".log")]
        return AgentResult(
            round=round_index,
            agent=self.name,
            finding=f"Regression logs provide {sum(text.count('FAILED') for text in failures)} failing cases to codify.",
            actions=[
                "Add unit test for legacy customer_id payload.",
                "Add unit test for v2 customer.id payload.",
                "Add unit test for empty invoice lines returning 0.00.",
            ],
            blockers=[],
        )


class RegressionTriageAgent(MigrationAgent):
    name = "RegressionTriageAgent"

    def analyze(self, round_index, snapshot, graph, risks, memory) -> AgentResult:
        return AgentResult(
            round=round_index,
            agent=self.name,
            finding="The likely regression source is inconsistent payload shape before invoice creation.",
            actions=[
                "Route all API inputs through the adapter.",
                "Attach failing log snippets to the next review round.",
            ],
            blockers=[] if round_index > 1 else ["Need another iteration after adapter tests are generated."],
        )


class CodeReviewAgent(MigrationAgent):
    name = "CodeReviewAgent"

    def analyze(self, round_index, snapshot, graph, risks, memory) -> AgentResult:
        open_blockers = [blocker for item in memory for blocker in item.blockers]
        return AgentResult(
            round=round_index,
            agent=self.name,
            finding="Migration is acceptable once adapter tests and billing compatibility checks are both green.",
            actions=[
                "Require review on API boundary changes.",
                "Block merge if compatibility tests are absent.",
                "Record context and regression evidence for auditability.",
            ],
            blockers=[] if round_index >= 3 else open_blockers[:2],
        )


def default_agents() -> list[MigrationAgent]:
    return [
        ApiCompatibilityAgent(),
        RefactorPlanningAgent(),
        TestSynthesisAgent(),
        RegressionTriageAgent(),
        CodeReviewAgent(),
    ]

