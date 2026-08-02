# ============================================
# OmniForces
# Memory Persistence Tests
# ============================================

from app.memory.memory_manager import MemoryManager


def test_memory_manager_save_and_load():

    memory = MemoryManager()

    memory.session.set_project(
        "OmniForces"
    )

    memory.session.set_milestone(
        "Milestone 3 Persistence Test"
    )

    memory.long_term.add_knowledge(
        "test",
        "Memory survived save and reload"
    )

    memory.save()

    loaded = MemoryManager()

    loaded.load()

    session = loaded.session.to_dict()
    knowledge = loaded.long_term.to_dict()

    assert session["project"] == "OmniForces"

    assert (
        session["milestone"]
        == "Milestone 3 Persistence Test"
    )

    assert (
        "Memory survived save and reload"
        in knowledge["knowledge"]["test"]
    )


def test_memory_storage_files_exist_after_save():

    memory = MemoryManager()

    memory.save()

    assert memory.storage.exists(
        "session_memory.json"
    )

    assert memory.storage.exists(
        "long_term_memory.json"
    )