"""
OmniForces
Supervisor Control Test
"""

from app.supervisor.control import SupervisorControl


def test_supervisor_agent_limit():

    supervisor = SupervisorControl()

    supervisor.register_agent(
        "KC-001",
        "Standard AI Engineer Limit"
    )

    assert (
        supervisor.check_limit("KC-001")
        == "Standard AI Engineer Limit"
    )