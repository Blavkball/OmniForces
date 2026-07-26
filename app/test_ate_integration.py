# ============================================
# OmniForces
# Integration Test — Atomic Task Engine,
# SupervisorControl, and AgentManager working
# together across the full task lifecycle.
# Closes Milestone 4 (ATE implementation).
# ============================================

from app.tasks.atomic_task_engine import AtomicTaskEngine, RiskLevel, TaskStatus
from app.agents.agent_manager import AgentManager, AgentManagerError
from app.supervisor.control import SupervisorControlError


def _build_system():
    """
    One shared AtomicTaskEngine, one AgentManager holding one
    SupervisorControl — the same wiring described in
    SYSTEM_ARCHITECTURE.md's Execution Flow: a single ATE instance is
    the source of truth that Supervisor and Agent Manager both operate
    against, never their own private copies.
    """
    engine = AtomicTaskEngine()
    manager = AgentManager(engine=engine)
    manager.register_agent("forge", "senior_engineer", "execute")
    return engine, manager


def test_full_happy_path():
    """
    Human/Supervisor request -> Atomic Task Engine (approval, task
    state) -> Agent Manager -> AI Employee -> Results -> Agent Manager
    (status report) -> Atomic Task Engine (record/close).
    Matches SYSTEM_ARCHITECTURE.md's Execution Flow end to end.
    """
    engine, manager = _build_system()

    task = engine.create_task(
        title="Write integration test",
        description="Confirm ATE, SupervisorControl, and AgentManager work together",
        purpose="Close Milestone 4",
        origin="manual",
        owner="forge",
        expected_output="A passing integration test",
        success_criteria=["all assertions pass"],
        failure_conditions=["any assertion fails"],
        risk_level=RiskLevel.LOW,
        recovery_pointer="commit-integration-test",
    )
    assert task.status == TaskStatus.CREATED

    # Supervisor path: Assigned -> reviewed -> Approved (auto, low risk)
    engine.assign_task(task.task_id, "forge")
    assert task.status == TaskStatus.ASSIGNED

    decision = manager.supervisor.review_task(engine, task.task_id)
    assert decision["approved"] is True
    assert decision["requires_human"] is False
    assert task.status == TaskStatus.APPROVED

    engine.mark_ready(task.task_id)
    assert task.status == TaskStatus.READY

    # Agent Manager path: accept moves Ready -> Executing
    accept_result = manager.accept_task(task.task_id, "forge")
    assert accept_result["status"] == TaskStatus.EXECUTING.value
    assert task.assigned_to == "forge"

    manager.report_progress(task.task_id, "test scaffolding in place")
    manager.report_progress(task.task_id, "assertions written")

    manager.report_result(task.task_id, "integration test passes")
    assert task.status == TaskStatus.REVIEW
    assert task.result == "integration test passes"

    engine.complete_task(task.task_id)
    assert task.status == TaskStatus.COMPLETED
    assert not engine.is_orphaned(task.task_id)

    # Execution history should read as a coherent story, not just a
    # final state — per ATE's own requirement that Memory Integration
    # let a future AI understand what happened and why.
    events = [e.event for e in task.execution_history]
    assert events == [
        "Created",
        "Assigned",
        "Approved",
        "Ready",
        "Executing",
        "in_progress",
        "in_progress",
        "Review",
        "Completed",
    ]
    print("test_full_happy_path: OK")


def test_human_approval_path():
    """
    A high-risk task with an irreversible-action flag must stop for a
    real human decision, not auto-approve, per SUPERVISOR.md's Human
    Approval Model.
    """
    engine, manager = _build_system()

    task = engine.create_task(
        title="Irreversible deploy",
        description="Deploy something that can't be undone",
        purpose="Test human approval routing",
        origin="manual",
        owner="forge",
        expected_output="Deployment confirmation",
        success_criteria=["deploy succeeds"],
        failure_conditions=["deploy fails"],
        risk_level=RiskLevel.HIGH,
        approval_requirements=["irreversible"],
        recovery_pointer="commit-deploy",
    )
    engine.assign_task(task.task_id, "forge")

    decision = manager.supervisor.review_task(engine, task.task_id)
    assert decision["requires_human"] is True
    assert task.status == TaskStatus.WAITING_FOR_HUMAN_DECISION

    # Agent Manager must not be able to accept a task still awaiting
    # a human decision — it is not in an acceptable status yet.
    try:
        manager.accept_task(task.task_id, "forge")
        raise AssertionError("accept_task should have rejected a task awaiting human decision")
    except AgentManagerError:
        pass

    # Human approves
    manager.supervisor.record_human_decision(engine, task.task_id, approved=True, reason="cleared by human")
    assert task.status == TaskStatus.APPROVED

    engine.mark_ready(task.task_id)
    accept_result = manager.accept_task(task.task_id, "forge")
    assert accept_result["status"] == TaskStatus.EXECUTING.value
    print("test_human_approval_path: OK")


def test_failure_escalation_retry_path():
    """
    Execution fails -> Agent Manager reports blocked -> routed through
    Supervisor -> Supervisor Review -> Supervisor decides retry ->
    task returns to Ready -> succeeds on second attempt.
    """
    engine, manager = _build_system()

    task = engine.create_task(
        title="Flaky task",
        description="Fails once, then succeeds",
        purpose="Test failure/replan path",
        origin="manual",
        owner="forge",
        expected_output="Eventually succeeds",
        success_criteria=["completes after retry"],
        failure_conditions=["fails permanently"],
        risk_level=RiskLevel.LOW,
        recovery_pointer="commit-flaky",
    )
    engine.assign_task(task.task_id, "forge")
    manager.supervisor.review_task(engine, task.task_id)
    engine.mark_ready(task.task_id)
    manager.accept_task(task.task_id, "forge")

    # First attempt fails
    manager.report_blocked(task.task_id, "transient network error")
    assert task.status == TaskStatus.SUPERVISOR_REVIEW

    # Supervisor decides to retry
    replan_result = manager.supervisor.replan(engine, task.task_id, decision="retry")
    assert replan_result["status"] == TaskStatus.READY.value
    assert task.status == TaskStatus.READY

    # Second attempt succeeds
    accept_result = manager.accept_task(task.task_id, "forge")
    assert accept_result["status"] == TaskStatus.EXECUTING.value
    manager.report_result(task.task_id, "succeeded on retry")
    engine.complete_task(task.task_id)
    assert task.status == TaskStatus.COMPLETED
    print("test_failure_escalation_retry_path: OK")


def test_failure_escalation_cancel_path():
    """
    Execution fails -> escalated -> Supervisor decides cancel, with
    full cancellation record per ATE's Cancellation Rules.
    """
    engine, manager = _build_system()

    task = engine.create_task(
        title="Not worth retrying",
        description="Fails and gets cancelled",
        purpose="Test cancel path",
        origin="manual",
        owner="forge",
        expected_output="N/A",
        success_criteria=["N/A"],
        failure_conditions=["fails permanently"],
        risk_level=RiskLevel.LOW,
        recovery_pointer="commit-cancel",
    )
    engine.assign_task(task.task_id, "forge")
    manager.supervisor.review_task(engine, task.task_id)
    engine.mark_ready(task.task_id)
    manager.accept_task(task.task_id, "forge")
    manager.report_blocked(task.task_id, "requirements changed mid-task")

    manager.supervisor.replan(
        engine,
        task.task_id,
        decision="cancel",
        reason="requirements no longer apply",
        cancelled_by="supervisor",
        attempted="one execution attempt",
        alternative_considered=True,
        retry_possible=False,
    )
    assert task.status == TaskStatus.CANCELLED
    assert not engine.is_orphaned(task.task_id)
    print("test_failure_escalation_cancel_path: OK")


def test_no_orphaned_task_across_full_run():
    """
    Sanity sweep: every task created across a full run must resolve
    to a defined state, never orphaned, per ATE's No Orphaned Task
    Policy and SUPERVISOR.md's mirrored policy.
    """
    engine, manager = _build_system()
    task_ids = []

    for i in range(3):
        t = engine.create_task(
            title=f"Sweep task {i}",
            description="d",
            purpose="p",
            origin="manual",
            owner="forge",
            expected_output="e",
            success_criteria=["c"],
            failure_conditions=["f"],
            risk_level=RiskLevel.LOW,
            recovery_pointer=f"commit-sweep-{i}",
        )
        engine.assign_task(t.task_id, "forge")
        manager.supervisor.review_task(engine, t.task_id)
        engine.mark_ready(t.task_id)
        manager.accept_task(t.task_id, "forge")
        manager.report_result(t.task_id, "done")
        engine.complete_task(t.task_id)
        task_ids.append(t.task_id)

    for task_id in task_ids:
        assert not engine.is_orphaned(task_id)
    print("test_no_orphaned_task_across_full_run: OK")


if __name__ == "__main__":
    test_full_happy_path()
    test_human_approval_path()
    test_failure_escalation_retry_path()
    test_failure_escalation_cancel_path()
    test_no_orphaned_task_across_full_run()
    print("\nAll integration tests passed. Milestone 4 (Atomic Task Engine) confirmed working end to end.")