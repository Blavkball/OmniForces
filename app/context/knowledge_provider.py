"""
OmniForces
Knowledge Provider

Central knowledge access layer.

Provides:
- Graphify code knowledge
- Repository knowledge
- AI_Knowledge documentation
- Obsidian knowledge

Future:
- Memory
- RAG
- Vector search
"""

import json
from pathlib import Path

from app.context.graphify_context import GraphifyContext
from app.context.repository_context import RepositoryContext
from app.context.ai_knowledge_context import AIKnowledgeContext
from app.context.obsidian_context import ObsidianContext


class KnowledgeProviderError(Exception):
    """Raised when the Knowledge Provider encounters an error."""
    pass


class KnowledgeProvider:
    """
    Central access point for all knowledge sources used by OmniForces.
    """

    def __init__(self):
        sources = self._load_sources()

        self.graph = GraphifyContext(
            sources.get("graphify", "graphify-out")
        )
        self.repositories = RepositoryContext(
            sources.get("repositories", None)
        )
        self.ai_knowledge = AIKnowledgeContext(
            sources.get("ai_knowledge", "AI_Knowledge")
        )
        self.obsidian = ObsidianContext(
            sources.get("obsidian", "obsidian-vault")
        )

    def _load_sources(self) -> dict:
        config_path = Path(__file__).resolve().parent.parent.parent / "knowledge_sources.json"

        if not config_path.exists():
            return {}

        try:
            with open(config_path, "r", encoding="utf-8") as config_file:
                return json.load(config_file)
        except json.JSONDecodeError as error:
            raise KnowledgeProviderError(
                f"Failed to parse knowledge_sources.json: {error}"
            )

    def get_repository(self, name: str):
        """
        Return the path to a repository by name.
        """

        repositories = self.repositories.list_available()

        return repositories.get(name)

    def find_code(self, query: str):
        """
        Search Graphify code knowledge.
        """

        return self.graph.find_nodes(query)

    def find_related(self, query: str):
        """
        Search Graphify relationships.
        """

        return self.graph.find_related(query)

    def find_documentation(self, query: str):
        """
        Search documentation across all registered repositories.
        """

        results = []

        repositories = self.repositories.list_available()

        for _, path in repositories.items():

            matches = list(
                path.rglob(f"*{query}*")
            )

            results.extend(matches)

        return results

    def get_all_repositories(self):
        """
        Return all known repositories.
        """

        return self.repositories.list_available()

    def get_global_knowledge(self):
        """
        Return the AI_Knowledge documentation repository.
        """

        return self.ai_knowledge.get_global_knowledge()

    def get_obsidian_notes(self):
        """
        Return every note currently stored in the Obsidian vault.

        Returns:
            dict[str, str]:
                Dictionary of filename -> note contents.
        """

        return self.obsidian.get_all_notes()

    def get_obsidian_note(self, filename: str):
        """
        Return a single Obsidian note.

        Args:
            filename:
                Markdown filename.

        Returns:
            str:
                Note contents.
        """

        return self.obsidian.read_note(filename)

    def search(self, query: str):
        """
        Unified knowledge search.

        Returns knowledge collected from every available provider.
        """

        return {
            "code": self.find_code(query),
            "related": self.find_related(query),
            "documentation": self.find_documentation(query),
            "repositories": self.get_all_repositories(),
            "global_knowledge": self.get_global_knowledge(),
            "obsidian": self.get_obsidian_notes(),
        }