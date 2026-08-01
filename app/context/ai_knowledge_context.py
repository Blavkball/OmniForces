"""
OmniForces
AI Knowledge Context Provider

Reads the central KingC Software knowledge repository.

Source:
E:/AI_Knowledge

Responsibilities:
- Load global knowledge
- Read architecture documents
- Read standards
- Provide shared ecosystem knowledge
"""

from pathlib import Path


class AIKnowledgeContextError(Exception):
    """Raised when AI Knowledge cannot be loaded."""
    pass


class AIKnowledgeContext:
    """
    Provides access to AI_Knowledge.
    """

    def __init__(self, path="E:/AI_Knowledge"):
        self.path = Path(path)

    def exists(self):
        """
        Check AI_Knowledge availability.
        """
        return self.path.exists()

    def read_document(self, filename):
        """
        Read a markdown document from AI_Knowledge root.
        """

        file_path = self.path / filename

        if not file_path.exists():
            raise AIKnowledgeContextError(
                f"Missing knowledge document: {file_path}"
            )

        return file_path.read_text(
            encoding="utf-8"
        )

    def get_global_knowledge(self):
        """
        Load GLOBAL_KNOWLEDGE.md
        """
        return self.read_document(
            "GLOBAL_KNOWLEDGE.md"
        )

    def list_domains(self):
        """
        Return available knowledge folders.
        """

        return [
            item.name
            for item in self.path.iterdir()
            if item.is_dir()
        ]