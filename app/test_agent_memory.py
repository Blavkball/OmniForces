# ============================================
# OmniForces
# Memory Manager Tests
# ============================================

from app.memory.memory_manager import MemoryManager


def test_memory_manager_initialises():

    memory = MemoryManager()

    assert memory.working is not None
    assert memory.session is not None
    assert memory.long_term is not None
    assert memory.storage is not None


def test_working_memory_through_manager():

    memory = MemoryManager()

    memory.working.set_task(
        "Testing MemoryManager integration"
    )

    memory.working.add_note(
        "All memory systems connect through MemoryManager"
    )

    result = memory.working.to_dict()

    assert result["task"] == (
        "Testing MemoryManager integration"
    )

    assert (
        "All memory systems connect through MemoryManager"
        in result["notes"]
    )


def test_session_memory_through_manager():

    memory = MemoryManager()

    memory.session.set_project(
        "OmniForces"
    )

    memory.session.set_milestone(
        "Milestone 3"
    )

    memory.session.add_todo(
        "Complete memory subsystem"
    )

    result = memory.session.to_dict()

    assert result["project"] == "OmniForces"

    assert result["milestone"] == "Milestone 3"

    assert (
        "Complete memory subsystem"
        in result["todos"]
    )


def test_long_term_memory_through_manager():

    memory = MemoryManager()

    memory.long_term.add_knowledge(
        "architecture",
        "Agents communicate through MemoryManager"
    )

    result = memory.long_term.to_dict()

    assert (
    "Agents communicate through MemoryManager"
    in result["knowledge"]["architecture"]
    )


def test_memory_manager_clear_methods():

    memory = MemoryManager()

    memory.working.set_task(
        "temporary"
    )

    memory.session.set_project(
        "temporary"
    )

    memory.long_term.add_knowledge(
        "test",
        "temporary"
    )

    memory.clear_working_memory()
    memory.clear_session_memory()
    memory.clear_long_term_memory()

    assert memory.working.to_dict()["task"] == ""
    assert memory.working.to_dict()["notes"] == []

    session_state = memory.session.to_dict()

    assert session_state["project"] == ""
    assert session_state["milestone"] == ""
    assert session_state["todos"] == []

    assert memory.long_term.to_dict()["knowledge"] == {}