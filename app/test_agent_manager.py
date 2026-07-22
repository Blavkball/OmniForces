# ============================================
# OmniForces
# Agent Manager Test
# ============================================

from agents.agent_manager import AgentManager


manager = AgentManager()

agent = manager.register_agent(
    "KC-001",
    "Senior AI Software Engineer",
    "Standard AI Engineer Limit"
)

agent.add_skill("Software Development")
agent.add_skill("Documentation")

print(agent.to_dict())

print(manager.supervisor.check_limit("KC-001"))

print("Agent Manager test complete")