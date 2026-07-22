# ============================================
# OmniForces
# Agent Memory Test
# ============================================

from memory.agent_memory import AgentMemory


agent = AgentMemory(
    "KC-001",
    "Senior AI Software Engineer"
)

agent.add_skill(
    "Software Development"
)

agent.add_skill(
    "Documentation"
)

agent.set_context(
    "current_project",
    "OmniForces"
)

agent.set_context(
    "milestone",
    "Milestone 3"
)


print(agent.to_dict())

print("Agent memory test complete")