"""
Tests for Knowledge Provider
"""

from app.context.knowledge_provider import KnowledgeProvider


def test_knowledge_provider_loads():

    provider = KnowledgeProvider()

    assert provider is not None


def test_repository_lookup():

    provider = KnowledgeProvider()

    repo = provider.get_repository("OmniForces")

    assert repo is not None


def test_code_search():

    provider = KnowledgeProvider()

    result = provider.find_code("AgentManager")

    assert len(result) > 0

    assert result[0]["label"] == "AgentManager"