from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SUPPORTED_SUFFIXES = {".py", ".md", ".log", ".txt", ".json", ".yaml", ".yml"}


@dataclass
class SourceFile:
    path: str
    text: str


@dataclass
class RepositorySnapshot:
    root: Path
    files: list[SourceFile]

    def get(self, suffix: str) -> list[SourceFile]:
        return [file for file in self.files if file.path.endswith(suffix)]

    @property
    def full_context(self) -> str:
        return "\n\n".join(f"### {file.path}\n{file.text}" for file in self.files)


def load_repository(root: str | Path) -> RepositorySnapshot:
    repo_root = Path(root)
    files: list[SourceFile] = []
    for path in sorted(repo_root.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            files.append(SourceFile(path.relative_to(repo_root).as_posix(), path.read_text(encoding="utf-8")))
    return RepositorySnapshot(root=repo_root, files=files)

