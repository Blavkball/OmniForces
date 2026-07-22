# ============================================
# OmniForces
# Long-Term Memory
# ============================================


class LongTermMemory:
    """
    Persistent project knowledge.
    """

    def __init__(self):
        self.clear()

    def add_knowledge(self, category: str, item: str):
        self.knowledge.setdefault(category, []).append(item)

    def get_knowledge(self, category: str):
        return self.knowledge.get(category, [])

    def remove_knowledge(self, category: str, item: str):
        if category in self.knowledge and item in self.knowledge[category]:
            self.knowledge[category].remove(item)

    def clear(self):
        self.knowledge = {}

    def to_dict(self):
        return {
            "knowledge": self.knowledge
        }