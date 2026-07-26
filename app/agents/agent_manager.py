# ============================================
# OmniForces
# Agent Manager
# Implements AGENT_MANAGER.md v1.1's Interface
# With Atomic Task Engine contract, plus real
# model execution via OllamaClient (Phase 2).
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
from app.ollama import OllamaClient
from app.router import choose_model


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

    def __init__(
        self,
        engine: Optional[AtomicTaskEngine] = None,
        ollama_client: Optional[OllamaClient] = None,
    ):
        self.agents = {}
        self.skill_loader = SkillLoader()
        self.supervisor = SupervisorControl()
        self.engine = engine or AtomicTaskEngine()
        self.ollama_client = ollama_client or OllamaClient()

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
    # Real execution (Phase 2 — wires OllamaClient + router.choose_model
    # into the task lifecycle). Requires the task to already be
    # Executing — call accept_task first.
    # ------------------------------------------------------------------

    def _build_prompt(self, task: AtomicTask) -> str:
        """
        Builds a single instruction prompt from the task's own fields.
        No role/system context yet — that is a follow-up atomic task,
        not folded into this one.
        """
        lines = [
            f"Task: {task.title}",
            f"Purpose: {task.purpose}",
            f"Description: {task.description}",
            f"Expected output: {task.expected_output}",
        ]
        if task.success_criteria:
            lines.append("Success criteria: " + "; ".join(task.success_criteria))
        return "\n".join(lines)

    def execute_task(self, task_id: str) -> dict:
        """
        Runs a task that is already in Executing (per accept_task)
        through the real model: builds a prompt from the task,
        selects a model via router.choose_model, calls OllamaClient,
        and reports the result back through ATE. On failure, routes
        through report_blocked instead of raising past Agent Manager,
        so the failure enters Supervisor Review rather than crashing
        the caller.
        """
        task = self.engine.get_task(task_id)
        if task.status != TaskStatus.EXECUTING:
            raise AgentManagerError(
                f"cannot execute task {task_id} in status {task.status}; "
                f"must be {TaskStatus.EXECUTING} — call accept_task first"
            )

        prompt = self._build_prompt(task)
        model = choose_model(prompt)
        self.report_progress(task_id, f"calling model {model}")

        try:
            ai_response = self.ollama_client.generate(prompt, model=model)
        except Exception as error:
            return self.report_blocked(task_id, f"model call failed: {error}")

        return self.report_result(task_id, ai_response.response)

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