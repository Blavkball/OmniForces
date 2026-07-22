# ============================================
# OmniForces
# Memory Manager
# ============================================

from .working_memory import WorkingMemory
from .session_memory import SessionMemory
from .long_term_memory import LongTermMemory
from .storage import MemoryStorage


class MemoryManager:
    """
    Central access point for all memory.
    """

    def __init__(self):
        self.working = WorkingMemory()
        self.session = SessionMemory()
        self.long_term = LongTermMemory()
        self.storage = MemoryStorage()

    def save(self):
        self.storage.save(
            "session_memory.json",
            self.session.to_dict()
        )

        self.storage.save(
            "long_term_memory.json",
            self.long_term.to_dict()
        )

    def load(self):
        session = self.storage.load("session_memory.json")
        long_term = self.storage.load("long_term_memory.json")

        if session:
            self.session.__dict__.update(session)

        if long_term:
            self.long_term.knowledge = long_term.get(
                "knowledge", {}
            )

    def clear_working_memory(self):
        self.working.clear()

    def clear_session_memory(self):
        self.session.clear()

    def clear_long_term_memory(self):
        self.long_term.clear()