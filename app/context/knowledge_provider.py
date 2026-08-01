"""
OmniForces
Knowledge Provider

Central access point for repository knowledge.

Combines:
- Graphify code knowledge
- Repository knowledge
- Documentation knowledge

AI employees should query this layer
instead of accessing files directly.
"""

from pathlib import Path

from app.context.graphify_context import GraphifyContext
from app.context.repository_context import RepositoryContext


class KnowledgeProviderError(Exception):
    pass


class KnowledgeProvider:
    """
    Provides unified knowledge access.

    Future sources:
    - Obsidian
    - Memory
    - RAG
    - Vector search
    """

    def __init__(self):
        self.graph = GraphifyContext()
        self.repositories = RepositoryContext()


    def get_repository(self, name: str):
        """
        Return repository location.
        """

        repos = self.repositories.list_available()

        return repos.get(name)


    def find_code(self, query: str):
        """
        Search code knowledge through Graphify.
        """

        return self.graph.find_nodes(query)


    def find_related(self, query: str):
        """
        Find relationships around a code object.
        """

        return self.graph.find_related(query)


    def find_documentation(self, repository: str, filename: str):
        """
        Locate documentation files.
        """

        repo = self.get_repository(repository)

        if not repo:
            raise KnowledgeProviderError(
                f"Unknown repository: {repository}"
            )

        matches = list(repo.rglob(filename))

        return matches


    def search(self, query: str):
        """
        General knowledge search.

        Initial version:
        - Searches code graph
        - Searches documentation filenames
        """

        return {
            "code": self.find_code(query),
            "repositories": self.repositories.list_available()
        }