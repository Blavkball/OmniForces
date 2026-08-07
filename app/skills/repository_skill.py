from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os
from pathlib import Path

from app.skills.skill_loader import SkillDefinition, SkillRegistry


@dataclass
class RepositorySkill:
    """
    RepositorySkill provides safe, read-only access to a repository.

    Constructor supports legacy usage in tests:
      RepositorySkill(root_dir=...)
    and also supports a registry: RepositorySkill(registry=..., root_dir=...)
    """
    registry: Optional[SkillRegistry] = None
    root_dir: str = "."

    def __post_init__(self):
        # normalize root_dir to absolute path
        self.root_dir = os.path.abspath(self.root_dir)
        if self.registry is not None:
            definition = get_repository_skill_definition()
            self.registry.register_skill(definition)

    # -----------------------------
    # Public skill execution entry
    # -----------------------------
    def execute(self, action: str, **kwargs: Any) -> Any:
        if action == "read_file":
            return self.read_file(kwargs.get("path"))
        if action == "list_files":
            return self.list_files(kwargs.get("path"))
        if action == "search_code":
            return self.search_code(kwargs.get("query"))
        raise ValueError(f"Unknown repository action: {action}")

    # -----------------------------
    # Repository operations
    # -----------------------------
    def _secure_path(self, path: str) -> str:
        if not path:
            raise ValueError("Path cannot be empty")
        candidate = os.path.abspath(os.path.join(self.root_dir, path))
        # prevent path traversal outside root_dir
        if not candidate.startswith(self.root_dir):
            raise ValueError("Access denied: path outside repository root")
        return candidate

    def read_file(self, path: str) -> str:
        file_path = self._secure_path(path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def list_files(self, path: Optional[str] = None) -> List[str]:
        base = self._secure_path(path) if path else self.root_dir
        if not os.path.isdir(base):
            raise NotADirectoryError(f"Directory not found: {path or base}")
        return os.listdir(base)

    def search_code(self, query: str) -> List[Dict[str, Any]]:
        """
        Search files under root_dir for query string.
        Return list of { "file": relative_path, "line": line_number, "text": line }.
        """
        if not query:
            return []
        results: List[Dict[str, Any]] = []
        for root, _, files in os.walk(self.root_dir):
            for fname in files:
                # check text files only (simple heuristic)
                if not fname.endswith((".py", ".txt", ".md")):
                    continue
                full = os.path.join(root, fname)
                try:
                    with open(full, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f, start=1):
                            if query.lower() in line.lower():
                                rel = os.path.relpath(full, self.root_dir)
                                results.append({"file": rel, "line": i, "text": line.rstrip("\n")})
                except (UnicodeDecodeError, OSError):
                    continue
        return results

    def inspect_structure(self) -> List[str]:
        """
        Return a simple list of files/directories under root_dir for testing.
        """
        out = []
        for root, dirs, files in os.walk(self.root_dir):
            for d in dirs:
                rel = os.path.relpath(os.path.join(root, d), self.root_dir)
                out.append(rel)
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), self.root_dir)
                out.append(rel)
        return out


def get_repository_skill_definition() -> SkillDefinition:
    """
    Factory to return a SkillDefinition for tests and registry registration.
    Test expects:
      - name == 'repository_skill'
      - 'repo:read' in permissions
    """
    return SkillDefinition(
        name="repository_skill",
        description="Provides safe read-only repository access.",
        permissions=["repo:read"],
        metadata={"version": "1.0"},
        entry_point=RepositorySkill,
    )