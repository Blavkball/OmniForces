# ============================================
# OmniForces
# Agent Memory Tests
# ============================================

from app.memory.agent_memory import AgentMemory


def test_agent_memory_creation():

    agent = AgentMemory(
        "KC-001",
        "Senior AI Software Engineer",
    )

    assert agent.agent_id == "KC-001"
    assert agent.role == "Senior AI Software Engineer"

    assert agent.skills == []
    assert agent.context == {}


def test_agent_memory_add_skill():

    agent = AgentMemory(
        "KC-001",
        "Senior AI Software Engineer",
    )

    agent.add_skill(
        "Software Development"
    )

    agent.add_skill(
        "Documentation"
    )

    assert "Software Development" in agent.skills
    assert "Documentation" in agent.skills


def test_agent_memory_set_context():

    agent = AgentMemory(
        "KC-001",
        "Senior AI Software Engineer",
    )

    agent.set_context(
        "current_project",
        "OmniForces",
    )

    agent.set_context(
        "milestone",
        "Milestone 3",
    )

    assert agent.context["current_project"] == "OmniForces"
    assert agent.context["milestone"] == "Milestone 3"


def test_agent_memory_to_dict():

    agent = AgentMemory(
        "KC-001",
        "Senior AI Software Engineer",
    )

    agent.add_skill(
        "Software Development"
    )

    agent.set_context(
        "current_project",
        "OmniForces",
    )

    result = agent.to_dict()

    assert result == {
        "agent_id": "KC-001",
        "role": "Senior AI Software Engineer",
        "skills": [
            "Software Development"
        ],
        "context": {
            "current_project": "OmniForces"
        },
    }