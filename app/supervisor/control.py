# ============================================
# OmniForces
# Supervisor Control Foundation
# ============================================


class SupervisorControl:
    """
    Controls AI agent permissions and requests.
    """

    def __init__(self):
        self.agent_limits = {}

    def register_agent(self, agent_id, limit):
        self.agent_limits[agent_id] = limit

    def check_limit(self, agent_id):
        return self.agent_limits.get(agent_id)

    def request_approval(self, agent_id, action):
        return {
            "agent_id": agent_id,
            "action": action,
            "approved": False,
            "requires_human": True
        }