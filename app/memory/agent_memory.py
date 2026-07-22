# ============================================
# OmniForces
# Agent Memory Foundation
# ============================================


class AgentMemory:
    """
    Stores identity and context for an AI agent.
    """

    def __init__(self, agent_id, role):
        self.agent_id = agent_id
        self.role = role
        self.skills = []
        self.context = {}

    def add_skill(self, skill):
        self.skills.append(skill)

    def set_context(self, key, value):
        self.context[key] = value

    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "skills": self.skills,
            "context": self.context
        }