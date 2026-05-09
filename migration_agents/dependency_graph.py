from __future__ import annotations

import ast
from dataclasses import dataclass, field

from .repository import RepositorySnapshot


@dataclass
class DependencyGraph:
    modules: dict[str, list[str]] = field(default_factory=dict)
    call_edges: list[dict] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"modules": self.modules, "call_edges": self.call_edges}


class _CallVisitor(ast.NodeVisitor):
    def __init__(self, module: str) -> None:
        self.module = module
        self.calls: list[dict] = []

    def visit_Call(self, node: ast.Call) -> None:
        name = ""
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        if name:
            self.calls.append({"from": self.module, "to": name, "line": node.lineno})
        self.generic_visit(node)


def build_dependency_graph(snapshot: RepositorySnapshot) -> DependencyGraph:
    graph = DependencyGraph()
    for source in snapshot.get(".py"):
        module = source.path.removesuffix(".py").replace("/", ".")
        imports: list[str] = []
        try:
            tree = ast.parse(source.text)
        except SyntaxError:
            graph.modules[module] = ["<syntax-error>"]
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)

        visitor = _CallVisitor(module)
        visitor.visit(tree)
        graph.modules[module] = sorted(set(imports))
        graph.call_edges.extend(visitor.calls)
    return graph

