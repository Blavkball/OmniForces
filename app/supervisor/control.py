# ============================================
# OmniForces
# Supervisor Control
# Implements SUPERVISOR.md v1.1 decision control
# against ATOMIC_TASK_ENGINE.md v1.2
# ============================================

from typing import Optional

from app.tasks.atomic_task_engine import (
    AtomicTaskEngine,
    AtomicTask,
    RiskLevel,
    TaskStatus,
    TaskEngineError,
)


# Approval-requirement flags that always force human approval, regardless
# of risk_level, per SUPERVISOR.md's Human Approval Model: "irreversible,
# security risk exists, data could be lost, financial impact exists, the
# AI is uncertain, the outcome cannot be safely evaluated."
_HUMAN_REQUIRED_FLAGS = {
    "irreversible",
    "security",
    "data_loss",
    "financial",
    "uncertain",
    "unsafe_to_evaluate",
}


class SupervisorControlError(Exception):
    """Raised when a Supervisor decision is invalid or out of order."""


class SupervisorControl:
    """
    Control and decision coordination layer. Holds no task state of its
    own — task state lives in the Atomic Task Engine. The Supervisor
    makes decisions; ATE records them.

    Every task control action here operates on an AtomicTaskEngine
    instance passed in by the caller (Agent Manager, in the normal
    flow) — Supervisor never holds its own copy of task state.
    """

    def __init__(self):
        self.agent_limits = {}

    # ------------------------------------------------------------------
    # Agent limits — unchanged from the original foundation.
    # ------------------------------------------------------------------

    def register_agent(self, agent_id, limit):
        self.agent_limits[agent_id] = limit

    def check_limit(self, agent_id):
        return self.agent_limits.get(agent_id)

    # ------------------------------------------------------------------
    # Task Control / Decision Control
    # (SUPERVISOR.md — Main Responsibilities)
    # ------------------------------------------------------------------

    def review_task(self, engine: AtomicTaskEngine, task_id: str) -> dict:
        """
        Reviews an Assigned task and decides whether it can proceed
        automatically or requires human approval. Returns a decision
        record; does not execute the task or assign it to an agent —
        that remains Agent Manager's responsibility once approved.
        """
        task = engine.get_task(task_id)
        if task.status != TaskStatus.ASSIGNED:
            raise SupervisorControlError(
                f"cannot review task in status {task.status}; must be {TaskStatus.ASSIGNED}"
            )

        requires_human, reason = self._requires_human_approval(task)

        if requires_human:
            engine.enter_waiting(task_id, TaskStatus.WAITING_FOR_HUMAN_DECISION, reason)
            return {
                "task_id": task_id,
                "approved": False,
                "requires_human": True,
                "reason": reason,
            }

        engine.record_approval(task_id, approved=True, reason="Auto-approved: " + reason)
        return {
            "task_id": task_id,
            "approved": True,
            "requires_human": False,
            "reason": reason,
        }

    def _requires_human_approval(self, task: AtomicTask) -> tuple:
        """
        Evaluates a task against the Human Approval Model. Returns
        (requires_human: bool, reason: str).
        """
        flagged = _HUMAN_REQUIRED_FLAGS.intersection(set(task.approval_requirements))
        if flagged:
            return True, f"approval_requirements flags human review: {sorted(flagged)}"
        if task.risk_level == RiskLevel.HIGH:
            return True, "risk_level is high"
        return False, f"risk_level is {task.risk_level.value}, no human-required flags present"

    def record_human_decision(
        self, engine: AtomicTaskEngine, task_id: str, approved: bool, reason: Optional[str] = None
    ) -> dict:
        """
        Records the outcome of an actual human decision on a task
        sitting in Waiting For Human Decision.
        """
        task = engine.resolve_human_decision(task_id, approved=approved, reason=reason)
        return {"task_id": task_id, "approved": approved, "status": task.status.value}

    # ------------------------------------------------------------------
    # Replanning Responsibility (SUPERVISOR.md)
    # ------------------------------------------------------------------

    def replan(
        self,
        engine: AtomicTaskEngine,
        task_id: str,
        decision: str,
        reason: Optional[str] = None,
        **kwargs,
    ) -> dict:
        """
        Handles a task that has reached Supervisor Review after a
        failure. `decision` must be one of: "retry", "escalate",
        "cancel". "new_route" and "different_agent" both map to retry
        at this layer — Agent Manager is responsible for the actual
        route or agent change before re-attempting; ATE only tracks
        that the task returned to Ready.
        """
        task = engine.get_task(task_id)
        if task.status != TaskStatus.SUPERVISOR_REVIEW:
            raise SupervisorControlError(
                f"cannot replan task in status {task.status}; must be {TaskStatus.SUPERVISOR_REVIEW}"
            )

        if decision in ("retry", "new_route", "different_agent"):
            engine.retry_task(task_id)
            return {"task_id": task_id, "decision": decision, "status": TaskStatus.READY.value}

        if decision == "escalate":
            engine.escalate_task(task_id, reason or "escalated by Supervisor")
            return {"task_id": task_id, "decision": decision, "status": TaskStatus.ESCALATED.value}

        if decision == "cancel":
            required = ("cancelled_by", "attempted", "alternative_considered", "retry_possible")
            missing = [k for k in required if k not in kwargs]
            if missing:
                raise SupervisorControlError(
                    f"cancel decision requires: {missing}"
                )
            engine.cancel_task(
                task_id,
                cancelled_by=kwargs["cancelled_by"],
                reason=reason or "cancelled by Supervisor",
                attempted=kwargs["attempted"],
                alternative_considered=kwargs["alternative_considered"],
                retry_possible=kwargs["retry_possible"],
            )
            return {"task_id": task_id, "decision": decision, "status": TaskStatus.CANCELLED.value}

        raise SupervisorControlError(
            f"unknown replan decision '{decision}'; must be retry, new_route, "
            "different_agent, escalate, or cancel"
        )

    # ------------------------------------------------------------------
    # Escalation entry point
    # (matches AGENT_MANAGER.md's Escalation Routing: blocked -> escalated
    # via ATE, then presented to Supervisor)
    # ------------------------------------------------------------------

    def handle_escalation(self, engine: AtomicTaskEngine, task_id: str, failure_reason: str) -> dict:
        """
        Entry point when Agent Manager reports a task cannot proceed.
        Moves the task into Supervisor Review via ATE's failure path,
        ready for a `replan` decision.
        """
        task = engine.report_failure(task_id, failure_reason)
        return {"task_id": task_id, "status": task.status.value}