import unittest
from pathlib import Path

from migration_agents.dependency_graph import build_dependency_graph
from migration_agents.repository import load_repository


class DependencyGraphTests(unittest.TestCase):
    def test_builds_import_and_call_edges(self):
        root = Path(__file__).resolve().parents[1]
        snapshot = load_repository(root / "sample_legacy_repo")
        graph = build_dependency_graph(snapshot)
        self.assertIn("api", graph.modules)
        self.assertTrue(any(edge["to"] == "calculate_invoice" for edge in graph.call_edges))


if __name__ == "__main__":
    unittest.main()

