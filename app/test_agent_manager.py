"""
OmniForces
Agent Manager Tests

Pytest coverage for:
- Agent registration
- Task acceptance
- Execution lifecycle
- Reporting
- Supervisor escalation
- Knowledge context injection and capping
"""

import pytest

from app.agents.agent_manager import (
    AgentManager,
    AgentManagerError,
)

from app.tasks.atomic_task_engine import (
    AtomicTaskEngine,
    RiskLevel,
    TaskStatus,
)


class FakeResponse:
    def __init__(self, response):
        self.response = response


class FakeOllamaClient:
    def __init__(self):
        self.calls = []

    def generate(self, prompt, model=None):
        self.calls.append(
            {
                "prompt": prompt,
                "model": model,
            }
        )

        return FakeResponse(
            "test model response"
        )


class FakeContextBuilder:
    """
    Returns a fixed context package instead of querying
    real Graphify / AI_Knowledge / Obsidian sources.
    """

    def __init__(self, context):
        self.context = context
        self.queries = []

    def build(self, query):
        self.queries.append(query)
        return self.context


def create_test_task(engine):

    return engine.create_task(
        title="Test task",
        description="Testing Agent Manager",
        purpose="Validate execution flow",
        origin="manual",
        owner="tester",
        expected_output="Result text",
        success_criteria=[
            "Task completes"
        ],
        failure_conditions=[
            "Model failure"
        ],
        risk_level=RiskLevel.LOW,
        recovery_pointer="test",
        role="Software Engineer",
    )


def build_manager(context_builder=None):

    engine = AtomicTaskEngine()

    client = FakeOllamaClient()

    manager = AgentManager(
        engine=engine,
        ollama_client=client,
        context_builder=context_builder,
    )

    return manager, engine, client


def test_register_agent():

    manager, _, _ = build_manager()

    agent = manager.register_agent(
        "agent1",
        "Software Engineer",
        "standard",
    )

    assert agent.agent_id == "agent1"
    assert manager.get_agent("agent1") == agent


def test_agent_permission_check():

    manager, _, _ = build_manager()

    manager.register_agent(
        "agent1",
        "Engineer",
        "high",
    )

    assert manager.check_permission(
        "agent1",
        "high",
    )

    assert not manager.check_permission(
        "agent1",
        "low",
    )


def test_accept_created_task():

    manager, engine, _ = build_manager()

    manager.register_agent(
        "agent1",
        "Engineer",
        "standard",
    )

    task = create_test_task(
        engine
    )

    result = manager.accept_task(
        task.task_id,
        "agent1",
    )

    assert result["task_id"] == task.task_id

    assert engine.get_task(
        task.task_id
    ).status == TaskStatus.ASSIGNED


def test_accept_unknown_agent_rejected():

    manager, engine, _ = build_manager()

    task = create_test_task(
        engine
    )

    with pytest.raises(
        AgentManagerError
    ):

        manager.accept_task(
            task.task_id,
            "missing",
        )


def test_build_prompt():

    manager, engine, _ = build_manager()

    task = create_test_task(
        engine
    )

    prompt = manager._build_prompt(
        task
    )

    assert "Test task" in prompt
    assert "Validate execution flow" in prompt
    assert "Task completes" in prompt


def test_build_prompt_queries_context_builder_by_title():

    fake_builder = FakeContextBuilder({
        "code": [],
        "related_code": [],
        "documentation": [],
        "obsidian": {},
        "global_knowledge": "",
    })

    manager, engine, _ = build_manager(
        context_builder=fake_builder
    )

    task = create_test_task(
        engine
    )

    manager._build_prompt(task)

    assert fake_builder.queries == ["Test task"]


def test_build_prompt_omits_empty_knowledge_section():

    fake_builder = FakeContextBuilder({
        "code": [],
        "related_code": [],
        "documentation": [],
        "obsidian": {},
        "global_knowledge": "",
    })

    manager, engine, _ = build_manager(
        context_builder=fake_builder
    )

    task = create_test_task(
        engine
    )

    prompt = manager._build_prompt(task)

    assert "Knowledge context:" not in prompt


def test_build_prompt_includes_nonempty_knowledge_section():

    fake_builder = FakeContextBuilder({
        "code": [{"label": "AgentManager"}],
        "related_code": [],
        "documentation": [],
        "obsidian": {},
        "global_knowledge": "short doc",
    })

    manager, engine, _ = build_manager(
        context_builder=fake_builder
    )

    task = create_test_task(
        engine
    )

    prompt = manager._build_prompt(task)

    assert "Knowledge context:" in prompt
    assert "AgentManager" in prompt
    assert "short doc" in prompt


def test_build_prompt_caps_long_code_list():

    many_nodes = [
        {"label": f"Node{i}"}
        for i in range(25)
    ]

    fake_builder = FakeContextBuilder({
        "code": many_nodes,
        "related_code": [],
        "documentation": [],
        "obsidian": {},
        "global_knowledge": "",
    })

    manager, engine, _ = build_manager(
        context_builder=fake_builder
    )

    task = create_test_task(
        engine
    )

    prompt = manager._build_prompt(task)

    assert "Node0" in prompt
    assert "Node9" in prompt
    assert "Node24" not in prompt
    assert "+15 more, not shown" in prompt


def test_build_prompt_caps_long_global_knowledge():

    long_text = "x" * 5000

    fake_builder = FakeContextBuilder({
        "code": [],
        "related_code": [],
        "documentation": [],
        "obsidian": {},
        "global_knowledge": long_text,
    })

    manager, engine, _ = build_manager(
        context_builder=fake_builder
    )

    task = create_test_task(
        engine
    )

    prompt = manager._build_prompt(task)

    assert "[truncated]" in prompt
    assert len(prompt) < len(long_text) + 500


def test_execute_task():

    manager, engine, client = build_manager()

    manager.register_agent(
        "agent1",
        "Engineer",
        "standard",
    )

    task = create_test_task(
        engine
    )

    engine.assign_task(
        task.task_id,
        "agent1",
    )

    engine.record_approval(
        task.task_id,
        True,
    )

    engine.mark_ready(
        task.task_id
    )

    engine.start_execution(
        task.task_id
    )

    result = manager.execute_task(
        task.task_id
    )

    assert result["status"] == TaskStatus.REVIEW.value

    assert len(client.calls) == 1


def test_report_progress():

    manager, engine, _ = build_manager()

    task = create_test_task(
        engine
    )

    result = manager.report_progress(
        task.task_id,
        "working",
    )

    assert result["task_id"] == task.task_id


def test_failure_escalation():

    manager, engine, _ = build_manager()

    task = create_test_task(
        engine
    )

    result = manager.report_blocked(
        task.task_id,
        "model failed",
    )

    assert result["task_id"] == task.task_id

    assert (
        engine.get_task(
            task.task_id
        ).status
        == TaskStatus.SUPERVISOR_REVIEW
    )
