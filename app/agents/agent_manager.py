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
import uuid
import logging
import asyncio
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable, Union

from app.memory.agent_memory import AgentMemory
from app.skills.skill_loader import SkillRegistry, SkillDefinition, SkillLoader
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
from dataclasses import dataclass, field

@dataclass
class AgentProfile:
    """Represents a managed agent instance and its properties."""
    agent_id: str
    name: str
    role: str
    system_prompt: str = ""
    model_name: str = "gpt-4"
    temperature: float = 0.7
    skills: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "active"

class AgentManagerError(Exception):
    """Base exception for AgentManager errors."""
    pass


class AgentNotFoundError(AgentManagerError):
    """Raised when an agent is not found."""
    pass


class AgentAlreadyExistsError(AgentManagerError):
    """Raised when registering an agent with an ID that already exists."""
    pass


class AgentExecutionError(AgentManagerError):
    """Raised when execution of an agent task fails."""
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


# --------------------------------------------------
# Knowledge context caps.
#
# No relevance ranking exists yet (no RAG / vector
# search — see knowledge_provider.py). Until it does,
# these are hard limits, not smart filtering. They
# exist to stop the prompt growing unbounded as
# GLOBAL_KNOWLEDGE.md, the Obsidian vault, or search
# hit-counts grow over time.
# --------------------------------------------------

_MAX_LIST_ITEMS = 10
_MAX_GLOBAL_KNOWLEDGE_CHARS = 1500


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
        engine: Optional[Any] = None,
        ollama_client: Optional[Any] = None,
        supervisor: Optional[Any] = None,
        skill_registry: Optional[SkillRegistry] = None,
        context_builder: Optional[Any] = None,
        **kwargs: Any
    ):
        # (keep all original __init__ body lines here)
        self.skill_registry: SkillRegistry = skill_registry or SkillRegistry()

        self.agents = {}

        self.skill_loader = self.skill_registry

        self.supervisor = SupervisorControl()

        self.engine = engine or AtomicTaskEngine()

        self.ollama_client = ollama_client or OllamaClient()

        if context_builder is not None:
            self.context_builder = context_builder
        else:
            try:
                self.context_builder = ContextBuilder()
            except NameError:
                self.context_builder = None


    # --------------------------------------------------
    # Agent Registration
    # --------------------------------------------------

    def register_agent(
        self,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        role: str = "default",
        system_prompt: str = "",
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        skills: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> AgentProfile:
        # If called like register_agent(name="TestAgent", role="Tester") without positional agent_id
        if agent_id is None and name is not None:
            final_id = name
        elif agent_id is not None:
            final_id = agent_id
        else:
            final_id = str(uuid.uuid4())

        final_name = name or final_id

        if final_id in self.agents:
            raise AgentAlreadyExistsError(f"Agent with ID '{final_id}' already exists.")

        profile = AgentProfile(
            agent_id=final_id,
            name=final_name,
            role=role,
            system_prompt=system_prompt,
            model_name=model_name,
            temperature=temperature,
            skills=list(skills) if skills else [],
            metadata=metadata or {},
            status="active"
        )
        self.agents[final_id] = profile
        return profile

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


    def get_agent(self, agent_id: str) -> AgentProfile:
        if agent_id not in self.agents:
            raise AgentNotFoundError(f"Agent with ID '{agent_id}' not found.")
        return self.agents[agent_id]


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


    def _cap_list(self, items):
        """
        Truncate a list to _MAX_LIST_ITEMS.

        Returns (visible_items, omitted_count).
        """

        if len(items) <= _MAX_LIST_ITEMS:

            return items, 0

        return (
            items[:_MAX_LIST_ITEMS],
            len(items) - _MAX_LIST_ITEMS,
        )


    def _format_knowledge_section(
        self,
        context: dict,
    ) -> str:
        """
        Render retrieved knowledge as a prompt section.

        Empty categories are omitted. Nothing is included
        that the search did not actually return. Lists are
        capped at _MAX_LIST_ITEMS; global_knowledge is capped
        at _MAX_GLOBAL_KNOWLEDGE_CHARS. These are hard limits,
        not relevance ranking — no RAG/vector search exists yet.
        """

        lines = []

        code = context.get("code") or []

        if code:

            visible, omitted = self._cap_list(code)

            labels = ", ".join(
                node.get("label", "?")
                for node in visible
            )

            suffix = (
                f" (+{omitted} more, not shown)"
                if omitted
                else ""
            )

            lines.append(
                f"Related code: {labels}{suffix}"
            )


        related_code = context.get("related_code") or []

        if related_code:

            lines.append(
                f"Related links: {len(related_code)} found"
            )


        documentation = context.get("documentation") or []

        if documentation:

            visible, omitted = self._cap_list(documentation)

            docs = ", ".join(
                str(path)
                for path in visible
            )

            suffix = (
                f" (+{omitted} more, not shown)"
                if omitted
                else ""
            )

            lines.append(
                f"Related documentation: {docs}{suffix}"
            )


        obsidian = context.get("obsidian") or {}

        if obsidian:

            visible, omitted = self._cap_list(
                list(obsidian.keys())
            )

            notes = ", ".join(visible)

            suffix = (
                f" (+{omitted} more, not shown)"
                if omitted
                else ""
            )

            lines.append(
                f"Relevant notes: {notes}{suffix}"
            )


        global_knowledge = context.get("global_knowledge") or ""

        if global_knowledge:

            if len(global_knowledge) > _MAX_GLOBAL_KNOWLEDGE_CHARS:

                global_knowledge = (
                    global_knowledge[:_MAX_GLOBAL_KNOWLEDGE_CHARS]
                    + "\n[truncated]"
                )

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


        assigned_agent = task.assigned_to
        if assigned_agent is None:
            raise AgentManagerError(
                f"task {task_id} has no assigned agent"
            )

        agent = self.get_agent(assigned_agent)

        if task.required_skills:
            skill_results = {}
            for skill_name in task.required_skills:
                skill_results[skill_name] = self._run_skill(
                    task,
                    agent,
                    skill_name,
                )
            return self.report_result(
                task_id,
                skill_results,
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

    def _run_skill(
        self,
        task: Any,
        agent: Any,
        skill_name: str,
    ) -> Any:
        """
        Executes a registered skill assigned to the task's agent.
        """
        if skill_name not in getattr(agent, "skills", []):
            raise AgentManagerError(
                f"agent '{agent.agent_id}' is not assigned skill '{skill_name}'"
            )

        skill_def = self.skill_registry.get_skill(skill_name)
        if skill_def is None:
            raise AgentManagerError(
                f"skill '{skill_name}' is not registered"
            )
        if not skill_def.enabled:
            raise AgentManagerError(
                f"skill '{skill_name}' is disabled"
            )

        entry_point = skill_def.entry_point
        if entry_point is None:
            raise AgentManagerError(
                f"skill '{skill_name}' has no executable entry point"
            )

        if isinstance(entry_point, type):
            skill = entry_point()
        elif callable(entry_point):
            try:
                skill = entry_point()
            except TypeError:
                skill = entry_point
        else:
            skill = entry_point

        if hasattr(skill, "execute"):
            return skill.execute(task)

        if hasattr(skill, "read_file") and isinstance(task.input, str):
            if "/" in task.input or task.input.endswith(".py") or task.input.endswith(".md"):
                return skill.read_file(task.input)
            return skill.search_code(task.input)

        if hasattr(skill, "query_graph"):
            return skill.query_graph(task.input or task.title)

        raise AgentManagerError(
            f"skill '{skill_name}' cannot be executed automatically"
        )


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
    def assign_skill_to_agent(self, agent_id: str, skill_name: str) -> bool:
        """Assigns a registered skill from SkillRegistry to an existing agent."""
        agent = self.get_agent(agent_id)
        skill = self.skill_registry.get_skill(skill_name)
        if not skill:
            raise ValueError(f"Skill '{skill_name}' is not registered in SkillRegistry.")

        if hasattr(agent, "skills"):
            if skill_name not in agent.skills:
                agent.skills.append(skill_name)
        elif isinstance(agent, dict):
            agent.setdefault("skills", [])
            if skill_name not in agent["skills"]:
                agent["skills"].append(skill_name)
        return True

    def get_agent_skills(self, agent_id: str) -> List[SkillDefinition]:
        """Retrieves full SkillDefinition instances for all skills assigned to an agent."""
        agent = self.get_agent(agent_id)
        skill_names = getattr(agent, "skills", agent.get("skills", []) if isinstance(agent, dict) else [])
        definitions = []
        for name in skill_names:
            skill = self.skill_registry.get_skill(name)
            if skill:
                definitions.append(skill)
        return definitions