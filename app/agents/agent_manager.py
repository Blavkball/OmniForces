# ============================================
# OmniForces
# Agent Manager
# Implements AGENT_MANAGER.md v1.1's Interface
# With Atomic Task Engine contract
# ============================================

from typing import Optional

from app.memory.agent_memory import AgentMemory
from app.skills.skill_loader import SkillLoader
from app.supervisor.control import SupervisorControl
from app.tasks.atomic_task_engine import (
    AtomicTaskEngine,
    AtomicTask,
    TaskStatus,
    TaskEngineError,
)


class AgentManagerError(Exception):
    """Raised when Agent Manager cannot accept or process a task as given."""


# Fields an ATE task must carry before Agent Manager will accept it,
# per AGENT_MANAGER.md — "Agent Manager accepts a task only when ...
# it carries a valid task_id, owner, objective, and completion_criteria."
# In ATE's actual data model these are: task_id, owner, purpose
# (objective) and success_criteria (completion_criteria).
_REQUIRED_FIELDS = ("task_id", "owner", "purpose", "success_criteria")

# ATE statuses Agent Manager is allowed to accept a task from.
_ACCEPTABLE_STATUSES = (TaskStatus.ASSIGNED, TaskStatus.APPROVED, TaskStatus.READY)


class AgentManager:
    """
    Coordinates AI agents. Never receives a task directly from
    Supervisor — every task arrives through ATE, and every result is
    reported back through ATE. Never sets ATE task state directly;
    reports status and lets ATE perform the transition.
    """

    def __init__(self, engine: Optional[AtomicTaskEngine] = None):
        self.agents = {}
        self.skill_loader = SkillLoader()
        self.supervisor = SupervisorControl()
        self.engine = engine or AtomicTaskEngine()

    # ------------------------------------------------------------------
    # Agent registration — unchanged from the original foundation.
    # ------------------------------------------------------------------

    def register_agent(self, agent_id, role, limit):
        agent = AgentMemory(agent_id, role)
        self.agents[agent_id] = agent
        self.supervisor.register_agent(agent_id, limit)
        return agent

    def get_agent(self, agent_id):
        return self.agents.get(agent_id)

    # ------------------------------------------------------------------
    # Receiving a Task (AGENT_MANAGER.md — Interface With ATE)
    # ------------------------------------------------------------------

    def accept_task(self, task_id: str, assigned_to: str) -> dict:
        """
        Accepts a task from ATE. Validates it carries the required
        fields and is in an acceptable status before taking it on.
        A task without these is rejected back to ATE, not silently
        dropped and not executed on partial information.
        """
        try:
            task = self.engine.get_task(task_id)
        except TaskEngineError as e:
            raise AgentManagerError(f"cannot accept unknown task: {e}")

        missing = [f for f in _REQUIRED_FIELDS if not getattr(task, f, None)]
        if missing:
            raise AgentManagerError(
                f"task {task_id} rejected — missing required fields: {missing}"
            )

        if task.status not in _ACCEPTABLE_STATUSES:
            raise AgentManagerError(
                f"task {task_id} rejected — status {task.status} is not one Agent "
                f"Manager can accept from; must be one of {_ACCEPTABLE_STATUSES}"
            )

        if assigned_to not in self.agents:
            raise AgentManagerError(
                f"task {task_id} rejected — agent '{assigned_to}' is not registered"
            )

        if task.status == TaskStatus.ASSIGNED:
            self.engine.assign_task(task_id, assigned_to)
        elif task.assigned_to is None:
            task.assigned_to = assigned_to

        if task.status == TaskStatus.READY:
            self.engine.start_execution(task_id)

        return {"task_id": task_id, "assigned_to": assigned_to, "status": task.status.value}

    # ------------------------------------------------------------------
    # Reporting Status (AGENT_MANAGER.md — Interface With ATE)
    # Agent Manager reports; ATE transitions the state. Agent Manager
    # never sets ATE task state directly.
    # ------------------------------------------------------------------

    def report_progress(self, task_id: str, detail: str) -> dict:
        """Level 1 status update — does not change ATE's task status."""
        task = self.engine.report_status(task_id, "in_progress", detail)
        return {"task_id": task_id, "status": task.status.value, "detail": detail}

    def report_result(self, task_id: str, result: str) -> dict:
        """
        Task result available — submits for review. ATE moves the
        task to Review, not Agent Manager directly.
        """
        task = self.engine.submit_for_review(task_id, result)
        return {"task_id": task_id, "status": task.status.value}

    def report_blocked(self, task_id: str, reason: str) -> dict:
        """
        Task cannot proceed. Routed through ATE and Supervisor per
        AGENT_MANAGER.md's Escalation Routing — Agent Manager does not
        contact Supervisor directly except through this recorded path.
        """
        result = self.supervisor.handle_escalation(self.engine, task_id, reason)
        return result

    # ------------------------------------------------------------------
    # Authority Limits (AGENT_MANAGER.md)
    # ------------------------------------------------------------------

    def check_permission(self, agent_id: str, required_limit) -> bool:
        """
        Confirms an agent's registered limit satisfies a required
        permission level before a skill or action proceeds. Agent
        Manager cannot grant itself permissions — this only checks
        what Supervisor already recorded at registration.
        """
        current = self.supervisor.check_limit(agent_id)
        return current is not None and current == required_limit