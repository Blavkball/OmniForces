# ============================================
# OmniForces
# Atomic Task Engine
# Implements ATOMIC_TASK_ENGINE.md v1.2
# ============================================
 
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
import uuid
 
 
class TaskStatus(str, Enum):
    CREATED = "Created"
    ASSIGNED = "Assigned"
    APPROVED = "Approved"
    READY = "Ready"
    EXECUTING = "Executing"
    REVIEW = "Review"
    COMPLETED = "Completed"
 
    WAITING_FOR_APPROVAL = "Waiting For Approval"
    WAITING_FOR_INFORMATION = "Waiting For Information"
    WAITING_FOR_DEPENDENCY = "Waiting For Dependency"
    WAITING_FOR_HUMAN_DECISION = "Waiting For Human Decision"
 
    EXECUTION_FAILURE = "Execution Failure"
    RECORD_FAILURE = "Record Failure"
    SUPERVISOR_REVIEW = "Supervisor Review"
    ESCALATED = "Escalated"
    CANCELLED = "Cancel With Reason"
    FAILED = "Failed With Explanation"
 
 
class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
 
 
class TaskEngineError(Exception):
    """Raised on invalid task creation or an illegal state transition."""
 
 
# States a task may legally hold before Supervisor approval is required to
# enter Executing. Per spec: "except tasks explicitly marked low-risk and
# pre-approved by standing rule."
_LOW_RISK_PRE_APPROVED = {RiskLevel.LOW}
 
# Valid forward transitions in the primary lifecycle.
_LIFECYCLE_ORDER = [
    TaskStatus.CREATED,
    TaskStatus.ASSIGNED,
    TaskStatus.APPROVED,
    TaskStatus.READY,
    TaskStatus.EXECUTING,
    TaskStatus.REVIEW,
    TaskStatus.COMPLETED,
]
 
_WAITING_STATES = {
    TaskStatus.WAITING_FOR_APPROVAL,
    TaskStatus.WAITING_FOR_INFORMATION,
    TaskStatus.WAITING_FOR_DEPENDENCY,
    TaskStatus.WAITING_FOR_HUMAN_DECISION,
}
 
_TERMINAL_STATES = {
    TaskStatus.COMPLETED,
    TaskStatus.FAILED,
    TaskStatus.CANCELLED,
    TaskStatus.ESCALATED,
    TaskStatus.WAITING_FOR_HUMAN_DECISION,
}
 
# Failure-handling states: mid-route to a terminal outcome, not orphaned
# while passing through them.
_FAILURE_HANDLING_STATES = {
    TaskStatus.EXECUTION_FAILURE,
    TaskStatus.RECORD_FAILURE,
    TaskStatus.SUPERVISOR_REVIEW,
}
 
_KNOWN_NON_ORPHAN_STATES = (
    set(_LIFECYCLE_ORDER) | _TERMINAL_STATES | _FAILURE_HANDLING_STATES
)
 
 
def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
 
 
@dataclass
class ExecutionEvent:
    timestamp: str
    event: str
    detail: Optional[str] = None
 
 
@dataclass
class AtomicTask:
    task_id: str
    title: str
    description: str
    purpose: str
    origin: str                      # raw_id value, or the literal "manual"
    owner: str
    expected_output: str
    success_criteria: list
    failure_conditions: list
    risk_level: RiskLevel
 
    assigned_to: Optional[str] = None
    priority: Optional[str] = None
    status: TaskStatus = TaskStatus.CREATED
    dependencies: list = field(default_factory=list)
    required_skills: list = field(default_factory=list)
    required_permissions: list = field(default_factory=list)
    input: Optional[str] = None
    recovery_pointer: Optional[str] = None
    approval_requirements: list = field(default_factory=list)
    execution_history: list = field(default_factory=list)
    result: Optional[str] = None
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)
 
    def _record(self, event: str, detail: Optional[str] = None):
        self.execution_history.append(
            ExecutionEvent(timestamp=_now(), event=event, detail=detail)
        )
        self.updated_at = _now()
 
 
class AtomicTaskEngine:
    """
    Creates, tracks, and closes Atomic Tasks per ATOMIC_TASK_ENGINE.md.
 
    ATE does not think and does not know. It tracks state and enforces
    the task lifecycle. It never assigns execution directly and never
    approves its own tasks.
    """
 
    def __init__(self):
        self._tasks: dict[str, AtomicTask] = {}
 
    # ------------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------------
 
    def create_task(
        self,
        title: str,
        description: str,
        purpose: str,
        origin: str,
        owner: str,
        expected_output: str,
        success_criteria: list,
        failure_conditions: list,
        risk_level: RiskLevel,
        priority: Optional[str] = None,
        dependencies: Optional[list] = None,
        required_skills: Optional[list] = None,
        required_permissions: Optional[list] = None,
        input: Optional[str] = None,
        recovery_pointer: Optional[str] = None,
        approval_requirements: Optional[list] = None,
    ) -> AtomicTask:
        if not origin:
            raise TaskEngineError("origin is required — no task exists without an origin")
        if origin != "manual" and not origin.strip():
            raise TaskEngineError("raw_id origin must be non-empty")
        if not owner:
            raise TaskEngineError("owner is required — a task without an owner cannot leave Created")
        if risk_level in (RiskLevel.MEDIUM, RiskLevel.HIGH) and not approval_requirements:
            raise TaskEngineError(
                "approval_requirements is required when risk_level is medium or high"
            )
        if not success_criteria:
            raise TaskEngineError("success_criteria is required — defines done")
        if not failure_conditions:
            raise TaskEngineError("failure_conditions is required")
 
        task = AtomicTask(
            task_id=str(uuid.uuid4()),
            title=title,
            description=description,
            purpose=purpose,
            origin=origin,
            owner=owner,
            expected_output=expected_output,
            success_criteria=success_criteria,
            failure_conditions=failure_conditions,
            risk_level=risk_level,
            priority=priority,
            dependencies=dependencies or [],
            required_skills=required_skills or [],
            required_permissions=required_permissions or [],
            input=input,
            recovery_pointer=recovery_pointer,
            approval_requirements=approval_requirements or [],
        )
        task._record("Created", f"origin={origin}, owner={owner}")
        self._tasks[task.task_id] = task
        return task
 
    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------
 
    def get_task(self, task_id: str) -> AtomicTask:
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskEngineError(f"no task with id {task_id}")
        return task
 
    # ------------------------------------------------------------------
    # Assignment (ATE -> Agent Manager, per AGENT_MANAGER.md contract)
    # ------------------------------------------------------------------
 
    def assign_task(self, task_id: str, assigned_to: str) -> AtomicTask:
        task = self.get_task(task_id)
        if task.status != TaskStatus.CREATED:
            raise TaskEngineError(
                f"cannot assign task in status {task.status}; must be {TaskStatus.CREATED}"
            )
        task.assigned_to = assigned_to
        task.status = TaskStatus.ASSIGNED
        task._record("Assigned", f"assigned_to={assigned_to}")
        return task
 
    # ------------------------------------------------------------------
    # Approval (Supervisor decision, recorded here — ATE never approves
    # its own tasks; this method records Supervisor's decision)
    # ------------------------------------------------------------------
 
    def record_approval(self, task_id: str, approved: bool, reason: Optional[str] = None) -> AtomicTask:
        task = self.get_task(task_id)
        if task.status != TaskStatus.ASSIGNED:
            raise TaskEngineError(
                f"cannot record approval for task in status {task.status}; must be {TaskStatus.ASSIGNED}"
            )
        if approved:
            task.status = TaskStatus.APPROVED
            task._record("Approved", reason)
        else:
            task.status = TaskStatus.FAILED
            task._record("Rejected by Supervisor", reason)
        return task
 
    def mark_ready(self, task_id: str) -> AtomicTask:
        task = self.get_task(task_id)
        if task.status != TaskStatus.APPROVED:
            raise TaskEngineError(
                f"cannot mark ready from status {task.status}; must be {TaskStatus.APPROVED}"
            )
        task.status = TaskStatus.READY
        task._record("Ready")
        return task
 
    # ------------------------------------------------------------------
    # Execution (Agent Manager reports into these)
    # ------------------------------------------------------------------
 
    def start_execution(self, task_id: str) -> AtomicTask:
        task = self.get_task(task_id)
        if task.status != TaskStatus.READY:
            if not (task.status == TaskStatus.CREATED and task.risk_level in _LOW_RISK_PRE_APPROVED):
                raise TaskEngineError(
                    f"cannot start execution from status {task.status}; "
                    f"must be {TaskStatus.READY}, or {TaskStatus.CREATED} if low-risk pre-approved"
                )
        if task.recovery_pointer is None:
            raise TaskEngineError(
                "recovery_pointer is required before entering Executing if task modifies working software"
            )
        task.status = TaskStatus.EXECUTING
        task._record("Executing")
        return task
 
    def report_status(self, task_id: str, event: str, detail: Optional[str] = None) -> AtomicTask:
        """
        Agent Manager status updates during execution that do not change
        ATE's task status — recorded to execution_history only.
        """
        task = self.get_task(task_id)
        task._record(event, detail)
        return task
 
    def submit_for_review(self, task_id: str, result: str) -> AtomicTask:
        task = self.get_task(task_id)
        if task.status != TaskStatus.EXECUTING:
            raise TaskEngineError(
                f"cannot submit for review from status {task.status}; must be {TaskStatus.EXECUTING}"
            )
        task.result = result
        task.status = TaskStatus.REVIEW
        task._record("Review", "submitted for review")
        return task
 
    def complete_task(self, task_id: str) -> AtomicTask:
        task = self.get_task(task_id)
        if task.status != TaskStatus.REVIEW:
            raise TaskEngineError(
                f"cannot complete from status {task.status}; must be {TaskStatus.REVIEW}"
            )
        if not task.result:
            raise TaskEngineError("a task is complete only when output is recorded")
        task.status = TaskStatus.COMPLETED
        task._record("Completed")
        return task
 
    # ------------------------------------------------------------------
    # Waiting states
    # ------------------------------------------------------------------
 
    def enter_waiting(self, task_id: str, waiting_status: TaskStatus, reason: str) -> AtomicTask:
        if waiting_status not in _WAITING_STATES:
            raise TaskEngineError(f"{waiting_status} is not a valid waiting state")
        if not reason:
            raise TaskEngineError("a waiting task always carries a reason")
        task = self.get_task(task_id)
        task.status = waiting_status
        task._record(str(waiting_status.value), reason)
        return task
 
    # ------------------------------------------------------------------
    # Failure handling
    # ------------------------------------------------------------------
 
    def report_failure(self, task_id: str, reason: str) -> AtomicTask:
        task = self.get_task(task_id)
        task.status = TaskStatus.RECORD_FAILURE
        task._record("Execution Failure", reason)
        task.status = TaskStatus.SUPERVISOR_REVIEW
        task._record("Supervisor Review", "awaiting decision")
        return task
 
    def retry_task(self, task_id: str) -> AtomicTask:
        task = self.get_task(task_id)
        if task.status != TaskStatus.SUPERVISOR_REVIEW:
            raise TaskEngineError("retry only valid from Supervisor Review")
        task.status = TaskStatus.READY
        task._record("Retry")
        return task
 
    def escalate_task(self, task_id: str, reason: str) -> AtomicTask:
        task = self.get_task(task_id)
        task.status = TaskStatus.ESCALATED
        task._record("Escalated", reason)
        return task
 
    def cancel_task(
        self,
        task_id: str,
        cancelled_by: str,
        reason: str,
        attempted: str,
        alternative_considered: bool,
        retry_possible: bool,
    ) -> AtomicTask:
        task = self.get_task(task_id)
        task.status = TaskStatus.CANCELLED
        task._record(
            "Cancel With Reason",
            (
                f"cancelled_by={cancelled_by}; reason={reason}; attempted={attempted}; "
                f"alternative_considered={alternative_considered}; retry_possible={retry_possible}"
            ),
        )
        return task
 
    def resolve_human_decision(
        self, task_id: str, approved: bool, reason: Optional[str] = None
    ) -> AtomicTask:
        """
        Resolves a task sitting in Waiting For Human Decision. Approved
        moves the task to Approved (ready for the Ready/Executing steps);
        rejected moves it to Failed With Explanation.
        """
        task = self.get_task(task_id)
        if task.status != TaskStatus.WAITING_FOR_HUMAN_DECISION:
            raise TaskEngineError(
                f"cannot resolve human decision from status {task.status}; "
                f"must be {TaskStatus.WAITING_FOR_HUMAN_DECISION}"
            )
        if approved:
            task.status = TaskStatus.APPROVED
            task._record("Approved", reason or "approved by human decision")
        else:
            task.status = TaskStatus.FAILED
            task._record("Rejected by human decision", reason)
        return task
 
    def fail_task(self, task_id: str, explanation: str) -> AtomicTask:
        task = self.get_task(task_id)
        task.status = TaskStatus.FAILED
        task._record("Failed With Explanation", explanation)
        return task
 
    # ------------------------------------------------------------------
    # No Orphaned Task Policy
    # ------------------------------------------------------------------
 
    def is_orphaned(self, task_id: str) -> bool:
        """
        A task is never orphaned if it has an owner and is either still
        progressing through the lifecycle, in a waiting state with a
        reason, or has reached one of the defined terminal states.
        """
        task = self.get_task(task_id)
        if not task.owner:
            return True
        if task.status in _WAITING_STATES:
            has_reason = bool(task.execution_history and task.execution_history[-1].detail)
            return not has_reason
        return task.status not in _KNOWN_NON_ORPHAN_STATES
 
    def list_tasks(self, status: Optional[TaskStatus] = None) -> list:
        if status is None:
            return list(self._tasks.values())
        return [t for t in self._tasks.values() if t.status == status]
 
