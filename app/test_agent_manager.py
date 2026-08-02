"""
OmniForces
Agent Manager Tests

Pytest coverage for:
- Agent registration
- Task acceptance
- Execution lifecycle
- Reporting
- Supervisor escalation
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


def build_manager():

    engine = AtomicTaskEngine()

    client = FakeOllamaClient()

    manager = AgentManager(
        engine=engine,
        ollama_client=client,
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