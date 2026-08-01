"""
OmniForces
Knowledge Provider

Central knowledge access layer.

Provides:
- Graphify code knowledge
- Repository knowledge
- AI_Knowledge documentation

Future:
- Obsidian
- Memory
- RAG
- Vector search
"""

from app.context.graphify_context import GraphifyContext
from app.context.repository_context import RepositoryContext
from app.context.ai_knowledge_context import AIKnowledgeContext


class KnowledgeProviderError(Exception):
    pass


class KnowledgeProvider:

    def __init__(self):

        self.graph = GraphifyContext()
        self.repositories = RepositoryContext()
        self.ai_knowledge = AIKnowledgeContext()


    def get_repository(self, name: str):
        """
        Return repository path.
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
        Search documentation across knowledge sources.
        """

        results = []

        repositories = self.repositories.list_available()

        for name, path in repositories.items():

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
        Return central AI knowledge.
        """

        return self.ai_knowledge.get_global_knowledge()


    def search(self, query: str):
        """
        Unified knowledge search.
        """

        return {
            "code": self.find_code(query),
            "related": self.find_related(query),
            "documentation": self.find_documentation(query),
            "repositories": self.get_all_repositories()
        }