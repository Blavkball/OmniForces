# ============================================
# OmniForces
# Supervisor Control Test
# ============================================

from supervisor.control import SupervisorControl


supervisor = SupervisorControl()


supervisor.register_agent(
    "KC-001",
    "Standard AI Engineer Limit"
)


print(supervisor.check_limit("KC-001"))


approval = supervisor.request_approval(
    "KC-001",
    "Load advanced skill"
)


print(approval)

print("Supervisor control test complete")