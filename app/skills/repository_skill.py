import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.skills.skill_loader import SkillDefinition


class RepositorySkill:
    """
    Skill providing controlled read access to the project repository.
    """

    def __init__(self, root_dir: Optional[str] = None):
        self.root_dir = Path(root_dir) if root_dir else Path.cwd()

    def _resolve_path(self, relative_path: str) -> Path:
        target_path = (self.root_dir / relative_path).resolve()
        if not str(target_path).startswith(str(self.root_dir.resolve())):
            raise ValueError(f"Access denied: path '{relative_path}' is outside repository root.")
        return target_path

    def read_file(self, relative_path: str) -> str:
        """
        Reads and returns the text content of a file within the repository.
        """
        file_path = self._resolve_path(relative_path)
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"File not found: '{relative_path}'")
        return file_path.read_text(encoding="utf-8")

    def search_code(self, query: str, extension: Optional[str] = ".py") -> List[Dict[str, Any]]:
        """
        Searches for a string query across repository files.
        """
        results = []
        for path in self.root_dir.rglob("*"):
            if path.is_file() and not any(part.startswith(".") for part in path.parts):
                if extension and not path.name.endswith(extension):
                    continue
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                    for line_num, line in enumerate(content.splitlines(), 1):
                        if query in line:
                            rel_path = str(path.relative_to(self.root_dir))
                            results.append({
                                "file": rel_path,
                                "line": line_num,
                                "content": line.strip()
                            })
                except Exception:
                    continue
        return results

    def inspect_structure(self, relative_dir: str = ".") -> List[str]:
        """
        Returns a list of relative file paths within the given directory.
        """
        dir_path = self._resolve_path(relative_dir)
        if not dir_path.exists() or not dir_path.is_dir():
            raise FileNotFoundError(f"Directory not found: '{relative_dir}'")
        
        items = []
        for path in dir_path.rglob("*"):
            if not any(part.startswith(".") for part in path.parts):
                items.append(str(path.relative_to(self.root_dir)))
        return sorted(items)


def get_repository_skill_definition() -> SkillDefinition:
    """
    Factory function returning the SkillDefinition for RepositorySkill.
    """
    return SkillDefinition(
        name="repository_skill",
        description="Provides controlled read access to inspect files, search code, and explore repository structure.",
        entry_point=RepositorySkill,
        permissions=["repo:read"],
        metadata={"version": "1.0"}
    )