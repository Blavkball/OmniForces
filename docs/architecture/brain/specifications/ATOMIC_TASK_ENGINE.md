# Atomic Task Engine

**Document:** ATOMIC_TASK_ENGINE.md

**Version:** 1.0

**Status:** Draft

**Owner:** KingC Software

**Last Updated:** 24 July 2026

**Source of Truth:** OmniForces

**Related Documents:**

- KCEF.md
- KCES_v1.0.md
- BRAIN_ARCHITECTURE.md
- AI_ONBOARDING.md

---

# Purpose

The Atomic Task Engine (ATE) creates, tracks, executes, and closes atomic tasks across OmniForces.

ATE does not think. ATE does not know. ATE tracks state and enforces the task lifecycle.

---

# Position in Architecture

Brain (knowledge)
↓ reference only, no duplication
Atomic Task Engine (task state)
↓ approved task
Supervisor (approval)
↓ assignment
Agent Manager (execution)
↓ result
Atomic Task Engine (close/record)


ATE sits between knowledge and execution. It does not store knowledge and it does not execute code.

---

# Boundary Definitions

## Does ATE store knowledge that belongs in Brain/Wiki?

No. ATE stores task records only: what the task is, who owns it, what state it is in. Any knowledge required to complete a task is retrieved from Brain by reference. Duplicating knowledge into a task record is a boundary violation.

## Does every task have traceability back to Raw?

Yes. Every task carries an `origin` field:

- `raw_id` — task was generated from a Raw dump entry, or
- `manual` — task was created directly, tagged with the creating identity.

No task exists without an origin. Orphan tasks are a validation failure at creation.

## Does every task have ownership and recovery?

Yes. Every task carries:

- `owner` — the agent id or role responsible.
- `recovery_pointer` — last known good state (commit hash, checkpoint id, or null if not applicable).

A task without an owner cannot leave `queued`. A task without a recovery pointer cannot enter `in_progress` if it modifies working software.

## Does ATE integrate correctly with Supervisor and Agent Manager?

Yes, by contract:

- ATE hands a validated, queued task to Supervisor for approval.
- Supervisor returns approved or rejected.
- ATE hands approved tasks to Agent Manager for assignment and execution.
- Agent Manager returns status updates.
- ATE records final state and closes or escalates.

ATE never assigns execution directly. ATE never approves its own tasks.

---

# Task Data Model

| Field | Type | Required | Notes |
|---|---|---|---|
| task_id | string | yes | unique |
| title | string | yes | |
| objective | string | yes | one objective only |
| origin | raw_id \| manual | yes | traceability |
| owner | agent id / role | yes | ownership |
| status | enum | yes | see lifecycle |
| created_at | timestamp | yes | |
| updated_at | timestamp | yes | |
| recovery_pointer | string \| null | conditional | required if task modifies working software |
| dependencies | task_id[] | no | |
| completion_criteria | string | yes | defines done |
| risk_level | low \| medium \| high | yes | |

---

# Task Lifecycle

Create
↓
Validate (objective, origin, completion criteria present?)
↓
Queued
↓
Supervisor Approval
↓ approved ↓ rejected
Assigned (Agent Manager) Closed (rejected, recorded)
↓
In Progress
↓
Tested
↓ pass ↓ fail
Complete Blocked / Failed
↓ ↓
Recorded Recovery (rollback via recovery_pointer)
↓ ↓
Archived Re-queued or escalated to Supervisor


A task cannot skip a state. A task cannot enter `In Progress` without Supervisor approval, except tasks explicitly marked low-risk and pre-approved by standing rule.

---

# Failure Handling

On failure or block:

1. Status set to `blocked` or `failed`.
2. `recovery_pointer` used to restore last known good state, if the task touched working software.
3. Task either re-queued with updated context, or escalated to Supervisor if the failure indicates a planning error rather than an execution error.

A failed task is never silently dropped. It is recorded.

---

# Non-Goals

ATE does not:

- Classify, extract entities, or build the knowledge graph. That is Brain's responsibility (Phase 3 — Intelligence).
- Make architectural decisions. That is Supervisor and human approval.
- Execute code. That is Agent Manager and the assigned agent.
- Store long-form knowledge. That is Brain's Wiki layer.

---

# Integration Requirements for Dependent Documents

`AGENT_MANAGER.md` must define: how it receives an assigned task, how it reports status back to ATE, how it uses Memory during execution.

`SUPERVISOR.md` must define: approval authority, rejection criteria, escalation handling from ATE.

Both are still unwritten. ATE's contracts above are the interface those documents must satisfy — do not diverge from the field names or state names here without updating this document first.

---

# Change History

## Version 1.0

- Initial ATOMIC_TASK_ENGINE.md.
- Defined position in architecture relative to Brain, Supervisor, Agent Manager.
- Answered the four boundary review questions from FRAMEWORK_MIGRATION_PLAN.md.
- Defined task data model, lifecycle, and failure handling.
- Defined non-goals to prevent scope drift into Brain or Agent Manager responsibility.