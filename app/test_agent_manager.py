import pytest
from app.agents.agent_manager import (
    AgentManager,
    AgentAlreadyExistsError,
    AgentNotFoundError,
    AgentExecutionError,
    AgentManagerError,
    AgentProfile
)
from app.skills.skill_loader import SkillRegistry, SkillDefinition


class _FakeOllamaResponse:
    def __init__(self, response: str):
        self.response = response


class _FakeOllamaClient:
    def __init__(self):
        self.calls = []

    def generate(self, prompt, model):
        self.calls.append({"prompt": prompt, "model": model})
        return _FakeOllamaResponse("stub response")


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


def test_execute_task_requires_agent_skills():
    from app.tasks.atomic_task_engine import AtomicTaskEngine, TaskStatus

    registry = SkillRegistry()
    required_skill = SkillDefinition(
        name="repository_skill",
        description="Reads repo code",
    )
    registry.register_skill(required_skill)

    engine = AtomicTaskEngine()
    fake_client = _FakeOllamaClient()
    manager = AgentManager(engine=engine, ollama_client=fake_client, skill_registry=registry)
    agent = manager.register_agent(name="Coder", role="Developer")

    task = engine.create_task(
        title="Use repository skill",
        description="Task requires repository_skill",
        purpose="Test required skill enforcement",
        origin="manual",
        owner="Coder",
        expected_output="Result",
        success_criteria=["completed"],
        failure_conditions=["failed"],
        risk_level=1,
        recovery_pointer="commit-required-skill",
        role="Developer",
        required_skills=["repository_skill"],
    )
    engine.assign_task(task.task_id, agent.agent_id)
    task.status = TaskStatus.EXECUTING

    with pytest.raises(AgentManagerError, match="missing required skills"):
        manager.execute_task(task.task_id)


def test_execute_task_succeeds_with_required_skills():
    from app.tasks.atomic_task_engine import AtomicTaskEngine, TaskStatus

    registry = SkillRegistry()
    required_skill = SkillDefinition(
        name="repository_skill",
        description="Reads repo code",
    )
    registry.register_skill(required_skill)

    engine = AtomicTaskEngine()
    fake_client = _FakeOllamaClient()
    manager = AgentManager(engine=engine, ollama_client=fake_client, skill_registry=registry)
    agent = manager.register_agent(name="Coder", role="Developer")
    manager.assign_skill_to_agent(agent.agent_id, "repository_skill")

    task = engine.create_task(
        title="Use repository skill",
        description="Task requires repository_skill",
        purpose="Test required skill enforcement",
        origin="manual",
        owner="Coder",
        expected_output="Result",
        success_criteria=["completed"],
        failure_conditions=["failed"],
        risk_level=1,
        recovery_pointer="commit-required-skill",
        role="Developer",
        required_skills=["repository_skill"],
    )
    engine.assign_task(task.task_id, agent.agent_id)
    task.status = TaskStatus.EXECUTING

    result = manager.execute_task(task.task_id)

    assert result["status"] == TaskStatus.REVIEW.value
    assert len(fake_client.calls) == 1
    assert "Task: Use repository skill" in fake_client.calls[0]["prompt"]


def test_execute_task_requires_agent_permissions():
    from app.tasks.atomic_task_engine import AtomicTaskEngine, TaskStatus

    registry = SkillRegistry()
    permission_skill = SkillDefinition(
        name="repo_skill",
        description="Provides repo read permission",
        permissions=["repo:read"],
    )
    registry.register_skill(permission_skill)

    engine = AtomicTaskEngine()
    fake_client = _FakeOllamaClient()
    manager = AgentManager(engine=engine, ollama_client=fake_client, skill_registry=registry)
    agent = manager.register_agent(name="Coder", role="Developer")
    manager.assign_skill_to_agent(agent.agent_id, "repo_skill")

    task = engine.create_task(
        title="Permission-based task",
        description="Task requires repo:write permission",
        purpose="Test required permission enforcement",
        origin="manual",
        owner="Coder",
        expected_output="Result",
        success_criteria=["completed"],
        failure_conditions=["failed"],
        risk_level=1,
        recovery_pointer="commit-required-permission",
        role="Developer",
        required_permissions=["repo:write"],
    )
    engine.assign_task(task.task_id, agent.agent_id)
    task.status = TaskStatus.EXECUTING

    with pytest.raises(AgentManagerError, match="missing required permissions"):
        manager.execute_task(task.task_id)


def test_execute_task_succeeds_with_required_permissions():
    from app.tasks.atomic_task_engine import AtomicTaskEngine, TaskStatus

    registry = SkillRegistry()
    permission_skill = SkillDefinition(
        name="repo_skill",
        description="Provides repo write permission",
        permissions=["repo:write"],
    )
    registry.register_skill(permission_skill)

    engine = AtomicTaskEngine()
    fake_client = _FakeOllamaClient()
    manager = AgentManager(engine=engine, ollama_client=fake_client, skill_registry=registry)
    agent = manager.register_agent(name="Coder", role="Developer")
    manager.assign_skill_to_agent(agent.agent_id, "repo_skill")

    task = engine.create_task(
        title="Permission-based task",
        description="Task requires repo:write permission",
        purpose="Test required permission enforcement",
        origin="manual",
        owner="Coder",
        expected_output="Result",
        success_criteria=["completed"],
        failure_conditions=["failed"],
        risk_level=1,
        recovery_pointer="commit-required-permission",
        role="Developer",
        required_permissions=["repo:write"],
    )
    engine.assign_task(task.task_id, agent.agent_id)
    task.status = TaskStatus.EXECUTING

    result = manager.execute_task(task.task_id)

    assert result["status"] == TaskStatus.REVIEW.value
    assert len(fake_client.calls) == 1
    assert "Task: Permission-based task" in fake_client.calls[0]["prompt"]


def test_execute_task_rejects_disabled_skill_permissions():
    from app.tasks.atomic_task_engine import AtomicTaskEngine, TaskStatus

    registry = SkillRegistry()
    disabled_skill = SkillDefinition(
        name="repo_skill",
        description="Provides blocked repo write permission",
        permissions=["repo:write"],
        enabled=True,
    )
    registry.register_skill(disabled_skill)

    engine = AtomicTaskEngine()
    fake_client = _FakeOllamaClient()
    manager = AgentManager(engine=engine, ollama_client=fake_client, skill_registry=registry)
    agent = manager.register_agent(name="Coder", role="Developer")
    manager.assign_skill_to_agent(agent.agent_id, "repo_skill")
    registry.disable_skill("repo_skill")

    task = engine.create_task(
        title="Permission-based task",
        description="Task requires repo:write permission",
        purpose="Test disabled-skill permission enforcement",
        origin="manual",
        owner="Coder",
        expected_output="Result",
        success_criteria=["completed"],
        failure_conditions=["failed"],
        risk_level=1,
        recovery_pointer="commit-disabled-permission",
        role="Developer",
        required_permissions=["repo:write"],
    )
    engine.assign_task(task.task_id, agent.agent_id)
    task.status = TaskStatus.EXECUTING

    with pytest.raises(AgentManagerError, match="missing required permissions"):
        manager.execute_task(task.task_id)
