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
            "code": knowledge["code"],
            "relationships": knowledge["related"],
            "documentation": knowledge["documentation"],
            "repositories": knowledge["repositories"]
        }