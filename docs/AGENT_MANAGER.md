# OmniForces Agent Manager Specification

**Document:** AGENT_MANAGER.md

**Version:** 1.0

**Status:** Architecture Complete

**Owner:** KingC Software

**Last Updated:** 24 July 2026

**Source of Truth:** AI_Workstation is the master company documentation system. OmniForces Agent Manager documentation defines the project implementation design.

**Related Documents:**

- KCEF.md
- KCES_v1.0.md
- ATOMIC_TASK_ENGINE.md
- BRAIN_ARCHITECTURE.md

---

# Purpose

The Agent Manager is the controlled operating layer responsible for managing AI Employees inside OmniForces.

The Agent Manager provides:

- Agent lifecycle management.
- Task assignment control.
- Permission enforcement.
- Health monitoring.
- Error handling.
- Recovery coordination.
- Audit logging.

The Agent Manager does not replace the Supervisor.

The Supervisor remains the authority and decision layer.

The Agent Manager does not replace the Atomic Task Engine (ATE).

ATE remains the single source of task state.

---

# Core Principle

> The Agent Manager controls AI Employee operations but does not make business decisions and does not hold task state independently of ATE.

The Agent Manager ensures AI Employees operate safely, consistently, and traceably.

---

# Position In System

Human
|
Supervisor
|
Atomic Task Engine (approval, task record)
|
Agent Manager
|
AI Employees
|
Results
|
Agent Manager (status report)
|
Atomic Task Engine (record / close / recovery trigger)
|
Memory Update
|
Documentation Update


Agent Manager never receives a task directly from Supervisor. Every task arrives through ATE, and every result is reported back through ATE. This satisfies the ATE contract requirement: *"ATE hands approved tasks to Agent Manager for assignment and execution. Agent Manager returns status updates."*

---

# Interface With Atomic Task Engine

This section defines the contract required by ATOMIC_TASK_ENGINE.md.

## Receiving a Task

Agent Manager accepts a task only when:

- It arrives from ATE, not from any other source.
- It carries a valid `task_id`, `owner`, `objective`, and `completion_criteria` as defined in ATE's data model.
- Its status is `assigned`.

A task without these fields is rejected back to ATE, not silently dropped and not executed on partial information.

## Reporting Status

Agent Manager reports to ATE at each of these points:

- Task accepted → ATE sets `in_progress`.
- Task result available → ATE sets `tested` or `complete`, depending on Testing Standard outcome.
- Task cannot proceed → ATE sets `blocked` or `failed`, with the reason attached.

Agent Manager never sets ATE task state directly. It reports; ATE transitions the state.

## Escalation Routing

Escalation to Supervisor is routed through ATE, not as a side-channel from Agent Manager. A failure that requires Supervisor judgment becomes an ATE state transition (`blocked` → `escalated`), and ATE presents it to Supervisor. Agent Manager does not contact Supervisor directly except through this recorded path.

---

# Responsibilities

The Agent Manager is responsible for:

## Agent Registration

Maintain:

- Agent identity.
- Agent status.
- Agent capabilities.
- Available skills.
- Permission level.

---

## Task Management

The Agent Manager:

- Receives ATE-assigned Atomic Tasks only.
- Assigns tasks to suitable AI Employees.
- Tracks task progress.
- Collects results.
- Reports completion or failure back to ATE.

---

## Lifecycle Management

The Agent Manager controls:

- Agent startup.
- Agent availability.
- Agent pause.
- Agent recovery.
- Agent shutdown.

---

# Agent States

Supported states:

Healthy
Busy
Waiting
Warning
Failed
Recovery Required
Offline


---

# Communication Rules

Communication flow:

Supervisor
|
v
Atomic Task Engine
|
v
Agent Manager
|
v
AI Employee
|
v
Result
|
v
Agent Manager
|
v
Atomic Task Engine
|
v
Supervisor (escalation or completion notice only)


AI Employees do not communicate directly with external systems without approved control.

Agent Manager does not communicate directly with Supervisor for routine task handling. All routine flow passes through ATE.

---

# Memory Usage During Execution

Required by ATE's integration contract. Agent Manager's relationship to Memory is limited:

## Agent Manager MAY

- Read agent state from Memory for recovery purposes (last known good state, recovery pointer lookup).
- Write agent health and status history to Memory for monitoring continuity.
- Read audit trail entries relevant to a task it is currently managing.

## Agent Manager MUST NOT

- Store long-form knowledge. That is Brain's Wiki layer responsibility.
- Write business decisions or task outcomes into Memory directly — those go through ATE's task record and Documentation Update step.
- Grant AI Employees Memory access beyond what their individual agent context and permission level allow.

AI Employees hold their own Memory access (WorkingMemory, SessionMemory) as established in the OmniForces Memory Foundation. Agent Manager supervises that access; it does not mediate every read/write.

---

# Authority Limits

The Agent Manager CAN:

- Assign approved tasks received from ATE.
- Monitor agents.
- Check permissions.
- Pause unhealthy agents.
- Start recovery procedures.
- Record events.
- Report problems to ATE.

---

The Agent Manager CANNOT:

- Create its own objectives.
- Change task requirements.
- Override Supervisor decisions.
- Override ATE task state directly.
- Grant itself permissions.
- Bypass approval requirements.
- Hide failures.
- Delete audit history.

---

# Error Handling

When an AI Employee fails:

AI Employee Error
|
v
Agent Manager Detection
|
v
Problem Classification
|
v
Recovery Attempt
|
v
Report to Atomic Task Engine
|
v
Supervisor Review (if escalated by ATE)
|
v
Resolution
|
v
Audit Record


---

# Recovery Levels

## Level 1 — Automatic Recovery

Allowed:

- Safe restart.
- Retry operation.
- Restore known state.

Reported to ATE as a status update, not an escalation.

---

## Level 2 — Supervisor Recovery

Routed through ATE as an `escalated` state. Supervisor decides:

- Replan task.
- Assign another AI Employee.
- Request Brain analysis.
- Change execution route.

---

## Level 3 — Human Approval

Routed through ATE and Supervisor. Required for:

- Data risk.
- Security concerns.
- Unknown failures.
- Irreversible actions.

---

# No Orphaned Work Policy

An AI Employee task must never remain:

- Forgotten.
- Hidden.
- Without owner.
- Without recovery path.

Every failed task must become, in ATE:

Completed
OR
Retry
OR
Replanned
OR
Escalated
OR
Cancelled With Reason


---

# Monitoring And Health Checks

The Agent Manager monitors:

- Agent availability.
- Current tasks.
- Response times.
- Errors.
- Memory health.
- Resource usage.
- Skill availability.

Health information is continuously recorded.

---

# Audit Logging

The Agent Manager records:

- Task assignments received from ATE.
- Agent actions.
- Status changes.
- Permission checks.
- Errors.
- Recovery attempts.
- Status reports sent to ATE.
- Final outcomes.

---

# Audit Rules

Important actions must always answer:

- What happened?
- Who performed it?
- Why did it happen?
- What was the result?

Logs cannot be silently removed or altered.

---

# Security Model

All requests must pass:

Request
|
Authentication
|
Permission Check
|
Agent Manager
|
Approved Action
|
Audit Log


---

# Permission Levels

## Read

Allowed:

- View status.
- View approved information.

---

## Execute

Allowed:

- Perform approved Atomic Tasks.

---

## Manage

Allowed:

- Control approved agent lifecycle.

---

## Admin

Reserved for:

- Supervisor.
- Human approval.

---

# Brain Relationship

The Brain provides analysis and recommendations.

The Agent Manager:

- Does not replace the Brain.
- Does not blindly follow Brain output.
- Executes only approved instructions.

Flow:

Brain
|
Recommendation
|
Supervisor
|
Decision
|
Atomic Task Engine
|
Agent Manager
|
Execution


---

# Documentation Requirements

Agent Manager actions must support:

- Recovery.
- Auditing.
- Future AI understanding.
- System maintenance.

Important decisions must be promoted into documentation.

---

# Future AI Resume Rule

A future AI should understand:

- Why the Agent Manager exists.
- What it controls.
- What limits it has.
- How failures are handled.
- Where authority exists.
- Why every task passes through ATE rather than being handled directly with Supervisor.

No critical knowledge should exist only inside chat history.

---

# Final Principle

> The Agent Manager is the controlled operating layer between the Atomic Task Engine and AI Employees. It enables safe execution while preserving human authority, accountability, and system recovery. It holds no task state of its own — ATE is the single source of task truth.

---

# Change History

## Version 1.0

- Initial AGENT_MANAGER.md.
- Corrected task and communication flow to route through Atomic Task Engine rather than direct Supervisor contact, per ATOMIC_TASK_ENGINE.md's integration contract.
- Added Interface With Atomic Task Engine section defining receive/report/escalate behavior.
- Added Memory Usage During Execution section, required by ATE's integration contract.
- Aligned document header to standard.