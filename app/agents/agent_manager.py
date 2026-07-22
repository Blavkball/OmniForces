# ============================================
# OmniForces
# Agent Manager Foundation
# ============================================

from memory.agent_memory import AgentMemory
from skills.skill_loader import SkillLoader
from supervisor.control import SupervisorControl


class AgentManager:
    """
    Coordinates AI agents.
    """

    def __init__(self):
        self.agents = {}
        self.skill_loader = SkillLoader()
        self.supervisor = SupervisorControl()

    def register_agent(self, agent_id, role, limit):
        agent = AgentMemory(agent_id, role)

        self.agents[agent_id] = agent

        self.supervisor.register_agent(
            agent_id,
            limit
        )

        return agent

    def get_agent(self, agent_id):
        return self.agents.get(agent_id)