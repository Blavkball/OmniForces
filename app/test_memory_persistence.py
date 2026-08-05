# ============================================
# OmniForces
# Memory Persistence Test
# ============================================

from app.memory.memory_manager import MemoryManager
from app.memory.storage import MemoryStorage


def test_memory_persists_across_save_and_load(tmp_path):

    storage = MemoryStorage(base_path=tmp_path)

    memory = MemoryManager(storage=storage)

    memory.session.set_project("OmniForces")
    memory.session.set_milestone("Milestone 3 Persistence Test")

    memory.long_term.add_knowledge(
        "test",
        "Memory survived save and reload"
    )

    memory.save()

    reloaded = MemoryManager(storage=storage)

    reloaded.load()

    assert reloaded.session.to_dict()["project"] == "OmniForces"
    assert reloaded.session.to_dict()["milestone"] == "Milestone 3 Persistence Test"

    assert (
        "Memory survived save and reload"
        in reloaded.long_term.get_knowledge("test")
    )
