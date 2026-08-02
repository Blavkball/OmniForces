"""
Tests for Memory Manager
"""

from app.memory.memory_manager import MemoryManager


def test_memory_manager_loads():

    memory = MemoryManager()

    assert memory is not None
    assert memory.working is not None
    assert memory.session is not None
    assert memory.long_term is not None


def test_working_memory_task():

    memory = MemoryManager()

    memory.working.set_task("Testing Memory System")

    result = memory.working.to_dict()

    assert result["task"] == "Testing Memory System"


def test_session_memory_project_and_milestone():

    memory = MemoryManager()

    memory.session.set_project("OmniForces")
    memory.session.set_milestone("Milestone 3")

    result = memory.session.to_dict()

    assert result["project"] == "OmniForces"
    assert result["milestone"] == "Milestone 3"


def test_long_term_memory_add_and_get():

    memory = MemoryManager()

    memory.long_term.add_knowledge(
        "architecture",
        "MemoryManager controls all memory access"
    )

    result = memory.long_term.get_knowledge("architecture")

    assert "MemoryManager controls all memory access" in result