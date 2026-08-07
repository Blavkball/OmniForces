from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os

from app.skills.skill_loader import SkillDefinition, SkillRegistry


@dataclass
class RepositorySkill:
    """
    RepositorySkill provides safe, read-only access to the local repository.

    Capabilities:
    - Read file contents
    - List files in a directory
    - Search for text within files
    """

    registry: SkillRegistry

    def __post_init__(self):
        """
        Register this skill with the SkillRegistry.
        """
        definition = SkillDefinition(
            name="repository",
            description="Provides safe read-only access to repository files.",
            permissions=["read"],
            metadata={"version": "1.0"},
            execute=self.execute
        )
        self.registry.register_skill(definition)

    # -----------------------------
    # Public skill execution entry
    # -----------------------------
    def execute(self, action: str, **kwargs: Any) -> Any:
        """
        Execute a repository action.

        Supported actions:
        - read_file(path)
        - list_files(path)
        - search_text(path, query)
        """
        if action == "read_file":
            return self.read_file(kwargs.get("path"))

        if action == "list_files":
            return self.list_files(kwargs.get("path"))

        if action == "search_text":
            return self.search_text(kwargs.get("path"), kwargs.get("query"))

        raise ValueError(f"Unknown repository action: {action}")

    # -----------------------------
    # Repository operations
    # -----------------------------
    def read_file(self, path: str) -> str:
        """
        Read a file from the repository.
        """
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def list_files(self, path: str) -> List[str]:
        """
        List files in a directory.
        """
        if not path or not os.path.isdir(path):
            raise NotADirectoryError(f"Directory not found: {path}")

        return os.listdir(path)

    def search_text(self, path: str, query: str) -> Dict[str, Any]:
        """
        Search for text within a file.
        """
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        if not query:
            raise ValueError("Search query cannot be empty")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        matches = []
        for i, line in enumerate(content.splitlines(), start=1):
            if query.lower() in line.lower():
                matches.append({"line": i, "text": line})

        return {
            "path": path,
            "query": query,
            "matches": matches,
        }
