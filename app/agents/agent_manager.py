# ============================================
# OmniForces
# Agent Manager
# Implements AGENT_MANAGER.md v1.1 Interface
#
# Responsibilities:
# - Receive tasks from Atomic Task Engine
# - Coordinate registered agents
# - Retrieve relevant knowledge before execution
# - Route execution through OllamaClient
# - Apply role context
# - Report results back through ATE
# - Escalate failures through SupervisorControl
# ============================================

from typing import Optional

from app.memory.agent_memory import AgentMemory
from app.skills.skill_loader import SkillLoader
from app.supervisor.control import SupervisorControl
from app.context.context_builder import ContextBuilder

from app.tasks.atomic_task_engine import (
    AtomicTaskEngine,
    AtomicTask,
    TaskStatus,
    TaskEngineError,
)

from app.ollama import OllamaClient
from app.router import choose_model
from app.roles import get_role_context


class AgentManagerError(Exception):
    """
    Raised when Agent Manager cannot accept
    or process a task.
    """
    pass


_REQUIRED_FIELDS = (
    "task_id",
    "owner",
    "purpose",
    "success_criteria",
)


_ACCEPTABLE_STATUSES = (
    TaskStatus.CREATED,
    TaskStatus.ASSIGNED,
    TaskStatus.APPROVED,
    TaskStatus.READY,
)


class AgentManager:
    """
    Coordinates AI agents.

    Agent Manager:
    - does not create tasks
    - does not approve tasks
    - does not own task state

    Atomic Task Engine remains the source of truth.
    """

    def __init__(
        self,
        engine: Optional[AtomicTaskEngine] = None,
        ollama_client: Optional[OllamaClient] = None,
        context_builder: Optional[ContextBuilder] = None,
    ):

        self.agents = {}

        self.skill_loader = SkillLoader()

        self.supervisor = SupervisorControl()

        self.engine = engine or AtomicTaskEngine()

        self.ollama_client = ollama_client or OllamaClient()

        self.context_builder = context_builder or ContextBuilder()


    # --------------------------------------------------
    # Agent Registration
    # --------------------------------------------------

    def register_agent(
        self,
        agent_id,
        role,
        limit,
    ):

        agent = AgentMemory(
            agent_id,
            role,
        )

        self.agents[agent_id] = agent

        self.supervisor.register_agent(
            agent_id,
            limit,
        )

        return agent


    def get_agent(self, agent_id):

        return self.agents.get(agent_id)


    # --------------------------------------------------
    # Task Acceptance
    # --------------------------------------------------

    def accept_task(
        self,
        task_id: str,
        assigned_to: str,
    ) -> dict:

        try:

            task = self.engine.get_task(
                task_id
            )

        except TaskEngineError as error:

            raise AgentManagerError(
                f"cannot accept unknown task: {error}"
            )


        missing = [
            field
            for field in _REQUIRED_FIELDS
            if not getattr(task, field, None)
        ]

        if missing:

            raise AgentManagerError(
                f"task {task_id} rejected - missing required fields: {missing}"
            )


        if task.status not in _ACCEPTABLE_STATUSES:

            raise AgentManagerError(
                f"task {task_id} rejected - "
                f"status {task.status} cannot be accepted"
            )


        if assigned_to not in self.agents:

            raise AgentManagerError(
                f"task {task_id} rejected - "
                f"agent '{assigned_to}' is not registered"
            )


        #
        # Only CREATED tasks should be assigned.
        #
        # Already assigned tasks belong to ATE.
        #
        if task.status == TaskStatus.CREATED:

            self.engine.assign_task(
                task_id,
                assigned_to,
            )

        elif task.assigned_to is None:

            task.assigned_to = assigned_to


        #
        # READY tasks may begin execution.
        #
        if task.status == TaskStatus.READY:

            self.engine.start_execution(
                task_id
            )


        return {
            "task_id": task_id,
            "assigned_to": assigned_to,
            "status": task.status.value,
            "role": task.role,
        }


    # --------------------------------------------------
    # Knowledge Retrieval
    # --------------------------------------------------

    def _gather_knowledge(
        self,
        task: AtomicTask,
    ) -> dict:
        """
        Query the Context Builder for knowledge relevant
        to this task, keyed by task title.
        """

        return self.context_builder.build(
            task.title
        )


    def _format_knowledge_section(
        self,
        context: dict,
    ) -> str:
        """
        Render retrieved knowledge as a prompt section.

        Empty categories are omitted. Nothing is included
        that the search did not actually return.
        """

        lines = []

        code = context.get("code") or []

        if code:

            labels = ", ".join(
                node.get("label", "?")
                for node in code
            )

            lines.append(
                f"Related code: {labels}"
            )


        related_code = context.get("related_code") or []

        if related_code:

            lines.append(
                f"Related links: {len(related_code)} found"
            )


        documentation = context.get("documentation") or []

        if documentation:

            docs = ", ".join(
                str(path)
                for path in documentation
            )

            lines.append(
                f"Related documentation: {docs}"
            )


        obsidian = context.get("obsidian") or {}

        if obsidian:

            notes = ", ".join(
                obsidian.keys()
            )

            lines.append(
                f"Relevant notes: {notes}"
            )


        global_knowledge = context.get("global_knowledge") or ""

        if global_knowledge:

            lines.append(
                "Global knowledge:\n"
                + global_knowledge
            )


        if not lines:

            return ""

        return (
            "Knowledge context:\n"
            + "\n".join(lines)
        )


    # --------------------------------------------------
    # Execution
    # --------------------------------------------------

    def _build_prompt(
        self,
        task: AtomicTask,
    ) -> str:

        lines = [
            f"Task: {task.title}",
            f"Purpose: {task.purpose}",
            f"Description: {task.description}",
            f"Expected output: {task.expected_output}",
        ]

        if task.success_criteria:

            lines.append(
                "Success criteria: "
                + "; ".join(task.success_criteria)
            )


        knowledge = self._gather_knowledge(
            task
        )

        knowledge_section = self._format_knowledge_section(
            knowledge
        )

        if knowledge_section:

            lines.append(
                knowledge_section
            )


        return "\n".join(lines)



    def execute_task(
        self,
        task_id: str,
    ) -> dict:


        task = self.engine.get_task(
            task_id
        )


        if task.status != TaskStatus.EXECUTING:

            raise AgentManagerError(
                f"cannot execute task {task_id}; "
                f"must be {TaskStatus.EXECUTING}"
            )


        role_context = get_role_context(
            task.role
        )


        prompt = (
            f"{role_context}\n\n"
            f"{self._build_prompt(task)}"
        )


        model = choose_model(
            role=task.role,
            prompt=prompt,
        )


        self.report_progress(
            task_id,
            f"calling model {model}",
        )


        try:

            response = self.ollama_client.generate(
                prompt,
                model=model,
            )

        except Exception as error:

            return self.report_blocked(
                task_id,
                f"model call failed: {error}",
            )


        return self.report_result(
            task_id,
            response.response,
        )


    # --------------------------------------------------
    # Reporting
    # --------------------------------------------------

    def report_progress(
        self,
        task_id,
        detail,
    ):

        task = self.engine.report_status(
            task_id,
            "in_progress",
            detail,
        )

        return {
            "task_id": task_id,
            "status": task.status.value,
            "detail": detail,
        }



    def report_result(
        self,
        task_id,
        result,
    ):

        task = self.engine.submit_for_review(
            task_id,
            result,
        )

        return {
            "task_id": task_id,
            "status": task.status.value,
        }



    def report_blocked(
        self,
        task_id,
        reason,
    ):

        return self.supervisor.handle_escalation(
            self.engine,
            task_id,
            reason,
        )


    # --------------------------------------------------
    # Permissions
    # --------------------------------------------------

    def check_permission(
        self,
        agent_id,
        required_limit,
    ) -> bool:

        current = self.supervisor.check_limit(
            agent_id
        )

        return (
            current is not None
            and current == required_limit
        )
