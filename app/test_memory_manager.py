# ============================================
# OmniForces
# Memory Manager Tests
# ============================================

from app.memory.memory_manager import MemoryManager
from app.memory.storage import MemoryStorage


def test_memory_manager_save_and_load(tmp_path):

    storage = MemoryStorage(base_path=tmp_path)

    memory = MemoryManager(storage=storage)

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

    loaded = MemoryManager(storage=storage)

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


def test_memory_storage_files_exist_after_save(tmp_path):

    storage = MemoryStorage(base_path=tmp_path)

    memory = MemoryManager(storage=storage)

    memory.save()

    assert memory.storage.exists(
        "session_memory.json"
    )

    assert memory.storage.exists(
        "long_term_memory.json"
    )
