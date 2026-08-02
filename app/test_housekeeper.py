# ============================================
# OmniForces
# Housekeeper Tests
# ============================================

from app.memory.memory_manager import MemoryManager
from app.memory.housekeeper import Housekeeper


def test_housekeeper_initialises():

    memory = MemoryManager()

    housekeeper = Housekeeper(
        memory
    )

    assert housekeeper.manager == memory


def test_housekeeper_runs_without_error():

    memory = MemoryManager()

    memory.session.set_project(
        "OmniForces"
    )

    memory.session.set_milestone(
        "Milestone 3"
    )

    memory.session.add_todo(
        "Test housekeeping"
    )

    housekeeper = Housekeeper(
        memory
    )

    housekeeper.run()

    assert memory.session.project == "OmniForces"
    assert memory.session.milestone == "Milestone 3"
    assert "Test housekeeping" in memory.session.todos


def test_housekeeper_maintenance_methods_exist():

    memory = MemoryManager()

    housekeeper = Housekeeper(
        memory
    )

    assert hasattr(
        housekeeper,
        "archive",
    )

    assert hasattr(
        housekeeper,
        "prune",
    )

    assert hasattr(
        housekeeper,
        "summarise",
    )