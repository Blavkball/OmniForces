import pytest
from app.agents.agent_manager import (
    AgentManager,
    AgentAlreadyExistsError,
    AgentNotFoundError,
    AgentExecutionError,
    AgentProfile
)
from app.skills.skill_loader import SkillRegistry, SkillDefinition


def test_register_and_get_agent():
    manager = AgentManager()
    agent = manager.register_agent(
        name="TestAgent",
        role="Tester",
        system_prompt="You test things."
    )
    assert agent.name == "TestAgent"
    assert agent.role == "Tester"
    
    retrieved = manager.get_agent(agent.agent_id)
    assert retrieved.agent_id == agent.agent_id


def test_register_duplicate_id_raises():
    manager = AgentManager()
    manager.register_agent(name="Agent1", role="Role1", agent_id="fixed_id")
    with pytest.raises(AgentAlreadyExistsError):
        manager.register_agent(name="Agent2", role="Role2", agent_id="fixed_id")


def test_get_nonexistent_agent_raises():
    manager = AgentManager()
    with pytest.raises(AgentNotFoundError):
        manager.get_agent("unknown_id")


def test_assign_and_get_skills():
    registry = SkillRegistry()
    skill_def = SkillDefinition(
        name="repository_skill",
        description="Reads repo code",
        permissions=["repo:read"]
    )
    registry.register_skill(skill_def)

    manager = AgentManager(skill_registry=registry)
    agent = manager.register_agent(name="Coder", role="Developer")
    
    manager.assign_skill_to_agent(agent.agent_id, "repository_skill")
    skills = manager.get_agent_skills(agent.agent_id)

    assert len(skills) == 1
    assert skills[0].name == "repository_skill"


def test_assign_unregistered_skill_raises():
    manager = AgentManager()
    agent = manager.register_agent(name="Coder", role="Developer")
    
    with pytest.raises(ValueError, match="not registered"):
        manager.assign_skill_to_agent(agent.agent_id, "missing_skill")