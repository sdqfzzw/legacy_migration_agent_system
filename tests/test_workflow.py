import unittest
from pathlib import Path

from migration_agents.main import run_migration_analysis


class WorkflowTests(unittest.TestCase):
    def test_migration_analysis_generates_complete_report(self):
        root = Path(__file__).resolve().parents[1]
        report = run_migration_analysis(root / "sample_legacy_repo", rounds=3)
        self.assertEqual(report["rounds"], 3)
        self.assertEqual(len(report["agent_results"]), 15)
        self.assertGreater(len(report["risk_map"]), 0)
        self.assertGreater(report["context_budget"]["total_estimated_tokens"], 1_000_000)


if __name__ == "__main__":
    unittest.main()
