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


def test_register_cline_agent_and_skill():
    manager = AgentManager()
    agent = manager.register_cline_agent(agent_id="cline", name="Cline")

    assert agent.role == "Cline"
    assert "cline_orchestration" in agent.skills
    assert manager.skill_registry.get_skill("cline_orchestration") is not None


def test_perform_cline_orchestration():
    manager = AgentManager()
    result = manager.perform_cline_orchestration(
        task_description="Coordinate a release",
        team=["Forge", "QA Engineer"],
    )

    assert "Orchestrating task: Coordinate a release" in result
    assert "Team: Forge, QA Engineer" in result


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


# --------------------------------------------------
# run_skill (Atomic Task 4: Execute Skill integration)
# --------------------------------------------------

def test_run_skill_instantiates_via_entry_point(tmp_path):
    from app.skills.repository_skill import get_repository_skill_definition, RepositorySkill

    registry = SkillRegistry()
    registry.register_skill(get_repository_skill_definition())

    manager = AgentManager(skill_registry=registry)

    result = manager.run_skill("repository_skill", root_dir=str(tmp_path))

    assert isinstance(result, RepositorySkill)
    assert result.root_dir == str(tmp_path)


def test_run_skill_unknown_skill_raises():
    manager = AgentManager()
    with pytest.raises(AgentManagerError):
        manager.run_skill("does_not_exist")


def test_run_skill_disabled_skill_raises():
    registry = SkillRegistry()
    skill_def = SkillDefinition(
        name="repository_skill",
        description="Reads repo code",
        entry_point=lambda: object(),
        enabled=False,
    )
    registry.register_skill(skill_def)
    manager = AgentManager(skill_registry=registry)

    with pytest.raises(AgentManagerError):
        manager.run_skill("repository_skill")


def test_run_skill_no_entry_point_raises():
    registry = SkillRegistry()
    skill_def = SkillDefinition(
        name="repository_skill",
        description="Reads repo code",
    )
    registry.register_skill(skill_def)
    manager = AgentManager(skill_registry=registry)

    with pytest.raises(AgentManagerError):
        manager.run_skill("repository_skill")


def test_run_skill_with_agent_id_requires_assignment():
    registry = SkillRegistry()
    skill_def = SkillDefinition(
        name="repository_skill",
        description="Reads repo code",
        entry_point=lambda: object(),
    )
    registry.register_skill(skill_def)
    manager = AgentManager(skill_registry=registry)
    agent = manager.register_agent(name="Coder", role="Developer")

    with pytest.raises(AgentManagerError, match="not assigned skill"):
        manager.run_skill("repository_skill", agent_id=agent.agent_id)


def test_run_skill_with_agent_id_succeeds_when_assigned():
    registry = SkillRegistry()
    skill_def = SkillDefinition(
        name="repository_skill",
        description="Reads repo code",
        entry_point=lambda: "ok",
    )
    registry.register_skill(skill_def)
    manager = AgentManager(skill_registry=registry)
    agent = manager.register_agent(name="Coder", role="Developer")
    manager.assign_skill_to_agent(agent.agent_id, "repository_skill")

    result = manager.run_skill("repository_skill", agent_id=agent.agent_id)

    assert result == "ok"

# --------------------------------------------------
# Atomic Task 5: skill_action execution in execute_task
# --------------------------------------------------

def test_execute_task_without_skill_action_has_no_skill_results_section():
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

    manager.execute_task(task.task_id)

    assert "Skill results:" not in fake_client.calls[0]["prompt"]


def test_execute_task_with_skill_action_runs_skill_and_includes_result():
    from app.tasks.atomic_task_engine import AtomicTaskEngine, TaskStatus

    def fake_entry_point(action, **kwargs):
        return f"ran {action} with {kwargs}"

    registry = SkillRegistry()
    skill_def = SkillDefinition(
        name="fake_skill",
        description="A fake skill for testing",
        entry_point=fake_entry_point,
    )
    registry.register_skill(skill_def)

    engine = AtomicTaskEngine()
    fake_client = _FakeOllamaClient()
    manager = AgentManager(engine=engine, ollama_client=fake_client, skill_registry=registry)
    agent = manager.register_agent(name="Coder", role="Developer")
    manager.assign_skill_to_agent(agent.agent_id, "fake_skill")

    task = engine.create_task(
        title="Use fake skill",
        description="Task requires fake_skill",
        purpose="Test skill_action execution",
        origin="manual",
        owner="Coder",
        expected_output="Result",
        success_criteria=["completed"],
        failure_conditions=["failed"],
        risk_level=1,
        recovery_pointer="commit-skill-action",
        role="Developer",
        required_skills=["fake_skill"],
        skill_action="lookup",
        skill_args={"query": "foo"},
    )
    engine.assign_task(task.task_id, agent.agent_id)
    task.status = TaskStatus.EXECUTING

    result = manager.execute_task(task.task_id)

    assert result["status"] == TaskStatus.REVIEW.value
    prompt = fake_client.calls[0]["prompt"]
    assert "Skill results:" in prompt
    assert "fake_skill: ran lookup with {'query': 'foo'}" in prompt


def test_execute_task_skill_action_failure_blocks_task():
    from app.tasks.atomic_task_engine import AtomicTaskEngine, TaskStatus

    def failing_entry_point(action, **kwargs):
        raise RuntimeError("skill exploded")

    registry = SkillRegistry()
    skill_def = SkillDefinition(
        name="fake_skill",
        description="A fake skill for testing",
        entry_point=failing_entry_point,
    )
    registry.register_skill(skill_def)

    engine = AtomicTaskEngine()
    fake_client = _FakeOllamaClient()
    manager = AgentManager(engine=engine, ollama_client=fake_client, skill_registry=registry)
    agent = manager.register_agent(name="Coder", role="Developer")
    manager.assign_skill_to_agent(agent.agent_id, "fake_skill")

    task = engine.create_task(
        title="Use failing skill",
        description="Task requires fake_skill",
        purpose="Test skill_action failure handling",
        origin="manual",
        owner="Coder",
        expected_output="Result",
        success_criteria=["completed"],
        failure_conditions=["failed"],
        risk_level=1,
        recovery_pointer="commit-skill-failure",
        role="Developer",
        required_skills=["fake_skill"],
        skill_action="lookup",
    )
    engine.assign_task(task.task_id, agent.agent_id)
    task.status = TaskStatus.EXECUTING

    result = manager.execute_task(task.task_id)

    assert result["status"] == TaskStatus.SUPERVISOR_REVIEW.value
    assert len(fake_client.calls) == 0