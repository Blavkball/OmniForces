"""
Tests for Cline AI employee role registration and model routing.
"""

from app.roles import get_role_context
from app.router import choose_model
from app.config import settings


def test_cline_role_context_includes_role_name():
    context = get_role_context("Cline")

    assert "Role: Cline." in context
    assert "coordinate the AI workforce" in context


def test_cline_routes_to_knowledge_model():
    model = choose_model(role="Cline")

    assert model == settings.LLAMA_MODEL
