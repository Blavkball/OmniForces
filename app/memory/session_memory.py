# ============================================
# OmniForces
# Session Memory
# ============================================


class SessionMemory:
    """
    Stores information for the current development session.
    """

    def __init__(self):
        self.clear()

    def set_project(self, project: str):
        self.project = project

    def set_milestone(self, milestone: str):
        self.milestone = milestone

    def set_task(self, task: str):
        self.task = task

    def add_todo(self, todo: str):
        self.todos.append(todo)

    def complete_todo(self, todo: str):
        if todo in self.todos:
            self.todos.remove(todo)

    def add_decision(self, decision: str):
        self.decisions.append(decision)

    def add_file(self, filename: str):
        if filename not in self.edited_files:
            self.edited_files.append(filename)

    def clear(self):
        self.project = ""
        self.milestone = ""
        self.task = ""
        self.todos = []
        self.decisions = []
        self.edited_files = []

    def to_dict(self):
        return {
            "project": self.project,
            "milestone": self.milestone,
            "task": self.task,
            "todos": self.todos,
            "decisions": self.decisions,
            "edited_files": self.edited_files,
        }