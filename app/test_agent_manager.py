import pytest
from app.agents.agent_manager import (
    AgentManager,
    AgentAlreadyExistsError,
    AgentNotFoundError,
    AgentExecutionError,
    AgentProfile
)
from app.skills.skill_loader import SkillRegistry, SkillDefinition
from app.skills.repository_skill import RepositorySkill
from app.tasks.atomic_task_engine import AtomicTaskEngine, RiskLevel, TaskStatus


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


def test_execute_task_with_required_skill(tmp_path):

    registry = SkillRegistry()
    registry.register_skill(
        SkillDefinition(
            name="repo_skill",
            description="Read repository files",
            entry_point=lambda: RepositorySkill(root_dir=str(tmp_path)),
            permissions=["repo:read"],
        )
    )

    engine = AtomicTaskEngine()
    manager = AgentManager(engine=engine, skill_registry=registry)
    agent = manager.register_agent(name="coder", role="Developer")
    manager.assign_skill_to_agent(agent.agent_id, "repo_skill")

    file_path = tmp_path / "sample.py"
    file_path.write_text("print('hello world')\n", encoding="utf-8")

    task = engine.create_task(
        title="Read a repository file",
        description="Verify skill execution through AgentManager",
        purpose="Test required skills",
        origin="manual",
        owner=agent.agent_id,
        expected_output="File contents",
        success_criteria=["file read"],
        failure_conditions=["file not read"],
        risk_level=RiskLevel.LOW,
        recovery_pointer="skill-execution-test",
        required_skills=["repo_skill"],
        input="sample.py",
    )

    engine.assign_task(task.task_id, agent.agent_id)
    manager.supervisor.review_task(engine, task.task_id)
    engine.mark_ready(task.task_id)
    manager.accept_task(task.task_id, agent.agent_id)

    result = manager.execute_task(task.task_id)
    assert result["task_id"] == task.task_id
    assert result["status"] == TaskStatus.REVIEW.value
    assert engine.get_task(task.task_id).result == {"repo_skill": "print('hello world')\n"}


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