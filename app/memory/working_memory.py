# ============================================
# OmniForces
# Working Memory
# ============================================

from typing import Any


class WorkingMemory:
    """
    Temporary memory used during a single request.

    This memory is cleared after the request is complete.
    """

    def __init__(self):
        self.clear()

    def start_request(self):
        """Start a new request."""
        self.clear()

    def set_task(self, task: str):
        self.task = task

    def set_context(self, context: dict):
        self.context = context

    def add_note(self, note: str):
        self.notes.append(note)

    def add_file(self, filename: str):
        if filename not in self.active_files:
            self.active_files.append(filename)

    def get_context(self) -> dict:
        return {
            "task": self.task,
            "context": self.context,
            "notes": self.notes,
            "active_files": self.active_files,
        }

    def clear(self):
        """Reset working memory."""
        self.task = ""
        self.context = {}
        self.notes = []
        self.active_files = []

    def to_dict(self) -> dict:
        return self.get_context()