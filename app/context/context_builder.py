"""
OmniForces
Context Builder

Creates structured AI employee context.
"""

from app.context.knowledge_provider import KnowledgeProvider


class ContextBuilder:

    def __init__(self):

        self.knowledge = KnowledgeProvider()


    def build(self, query: str):
        """
        Build complete context package.
        """

        knowledge = self.knowledge.search(query)

        return {
            "query": query,
            "code": knowledge.get("code", []),
            "related_code": knowledge.get("related", []),
            "documentation": knowledge.get("documentation", []),
            "repositories": knowledge.get("repositories", {}),
            "global_knowledge": knowledge.get("global_knowledge", ""),
            "obsidian": knowledge.get("obsidian", {}),
        }
