"""
Tests for Obsidian Context Provider
"""

from app.context.obsidian_context import ObsidianContext


def test_obsidian_context_loads():

    context = ObsidianContext()

    assert context is not None


def test_vault_exists():

    context = ObsidianContext()

    assert context.exists() is True


def test_list_notes():

    context = ObsidianContext()

    notes = context.list_notes()

    assert len(notes) == 3

    assert "Welcome.md" in notes


def test_read_note():

    context = ObsidianContext()

    content = context.read_note("Welcome.md")

    assert len(content) > 0


def test_get_all_notes():

    context = ObsidianContext()

    notes = context.get_all_notes()

    assert len(notes) == 3

    assert "Welcome.md" in notes