# OmniForces Supervisor Specification

**Document:** SUPERVISOR.md

**Version:** 1.0

**Status:** Architecture Complete

**Owner:** KingC Software

**Last Updated:** 24 July 2026

**Source of Truth:** AI_Workstation is the master company documentation system. OmniForces Supervisor documentation defines the project implementation design.

**Related Documents:**

- KCEF.md
- KCES_v1.0.md
- ATOMIC_TASK_ENGINE.md
- AGENT_MANAGER.md
- BRAIN_ARCHITECTURE.md

---

# Purpose

The Supervisor is the control and decision coordination layer of OmniForces.

The Supervisor exists to ensure:

- AI Employees operate safely.
- Tasks follow approved objectives.
- Decisions are reviewed.
- Failures are handled correctly.
- Human authority is preserved.

The Supervisor manages the workforce but does not replace human judgement.

The Supervisor holds no task state of its own. Task state lives in the Atomic Task Engine (ATE). The Supervisor makes decisions; ATE records them.

---

# Core Principle

> The Supervisor controls execution flow, but Human approval remains the final authority for important decisions.

---

# Position In System

Human
|
Supervisor
|
Atomic Task Engine (approval recorded, task state)
|
Agent Manager
|
AI Employees
|
Results
|
Agent Manager (status report)
|
Atomic Task Engine (record / escalate)
|
Supervisor (if escalated)
|
Memory
|
Documentation


This matches the flow defined in AGENT_MANAGER.md's Interface With Atomic Task Engine section. Supervisor approves work by approving the ATE task record, not by instructing Agent Manager directly.

---

# Why The Supervisor Exists

Without a Supervisor:

- AI Employees could act independently.
- Tasks could lose ownership.
- Failures could remain unresolved.
- Decisions could become untraceable.

The Supervisor provides:

- Control.
- Coordination.
- Safety.
- Accountability.
- Recovery.

---

# Main Responsibilities

The Supervisor is responsible for:

## Task Control

The Supervisor:

- Receives objectives.
- Reviews tasks queued in ATE.
- Approves execution, moving an ATE task from `queued` to `assigned`.
- Monitors progress via ATE status.
- Reviews outcomes reported through ATE.

---

## Workforce Coordination

The Supervisor manages, through ATE:

- Task priorities.
- Escalations arriving from ATE.

The Supervisor does not issue instructions to Agent Manager directly. See AGENT_MANAGER.md — Agent Manager accepts tasks from ATE only.

---

## Decision Control

The Supervisor decides:

- Whether work can proceed (ATE `queued` → `assigned`).
- Whether human approval is required.
- Whether a task should be replanned.
- Whether a failure requires escalation.

---

# Relationship With The Brain

The Brain is the reasoning and analysis capability.

The Brain provides:

- Analysis.
- Recommendations.
- Possible solutions.
- Route suggestions.

The Brain does not have execution authority.

Flow:

Problem
|
v
Brain Analysis
|
v
Recommendation
|
v
Supervisor Review
|
v
Decision
|
v
Atomic Task Engine
|
v
Execution


---

# Brain Decision Rules

The Supervisor must evaluate Brain recommendations.

The Supervisor cannot:

- Automatically execute every Brain suggestion.
- Allow Brain output to bypass controls.
- Treat a recommendation as approval.

The Brain provides intelligence.

The Supervisor provides controlled action.

---

# Human Approval Model

Human approval is required when:

- The action is irreversible.
- Security risk exists.
- Data could be lost.
- Financial impact exists.
- The AI is uncertain.
- The outcome cannot be safely evaluated.

Flow:

AI Analysis
|
v
Supervisor Review
|
v
Human Approval
|
v
Atomic Task Engine (state updated)
|
v
Execution


---

# Task Ending States — Terminology Alignment

This document originally defined task-ending states independently of ATE's data model. They do not match. Both sets are listed here until one is chosen as canonical:

| This document (Supervisor-facing) | ATOMIC_TASK_ENGINE.md (task record state) |
|---|---|
| Completed | `complete` |
| Failed With Record | `failed` |
| Cancelled With Reason | (no direct equivalent — needs adding to ATE, or mapped to `failed` with a cancellation reason) |
| Escalated | (no direct equivalent — needs adding to ATE as a state, or treated as a sub-state of `blocked`) |
| Waiting For Decision | (no direct equivalent — closest is `blocked`) |

Recommend ATE's data model gets extended with `escalated` and `cancelled` as explicit states rather than overloading `blocked`/`failed`, since Supervisor decision-making depends on telling those apart. Not changed here — this is Supervisor's document, not ATE's; ATE needs its own confirmed update.

---

# Replanning Responsibility

When a task cannot complete, reported to Supervisor via ATE escalation:

Task Failure (ATE: blocked or failed)
|
v
Escalated to Supervisor
|
v
Review Problem
|
+---- Retry (ATE: re-queued)
|
+---- New Route (ATE: re-queued with updated context)
|
+---- Different Agent (ATE: re-assigned)
|
+---- Human Decision (ATE: blocked, pending)
|
+---- Cancel With Reason (ATE: closed, reason recorded)


A task must never remain abandoned. Every decision here is recorded back into ATE's task record — the Supervisor decides, ATE stores the decision.

---

# No Orphaned Task Policy

The Supervisor ensures every task has, via ATE:

- Owner.
- Current status.
- Next action.
- Recovery route.

A task can only end as one of the states in the Terminology Alignment table above. See that section — the exact end-state vocabulary needs reconciling with ATE before this is implementation-ready.

---

# Approval Responsibilities

The Supervisor controls:

- When approval is required.
- What information is presented.
- Why approval is needed.

Human approval requests must include:

- Problem.
- Recommended action.
- Reason.
- Risks.
- Expected result.

---

# Supervisor Limits

The Supervisor CAN:

- Approve tasks for execution via ATE.
- Approve safe execution.
- Request analysis.
- Replan tasks.
- Escalate problems.
- Stop unsafe operations.

---

The Supervisor CANNOT:

- Override human approval.
- Ignore security rules.
- Hide failures.
- Remove audit history.
- Create unsafe permissions.
- Allow uncontrolled AI access.
- Instruct Agent Manager directly, bypassing ATE.

---

# Communication Model

Human
|
Supervisor
|
Atomic Task Engine
|
Agent Manager
|
AI Employee

AI Employee
|
Agent Manager
|
Atomic Task Engine
|
Supervisor (if escalated)
|
Human (if required)


All workforce communication is controlled and passes through ATE. This matches AGENT_MANAGER.md's Communication Rules section — neither document routes Supervisor and Agent Manager directly to each other for routine task flow.

---

# Failure Handling

When something goes wrong:

Failure Detected (Agent Manager)
|
v
Reported to Atomic Task Engine
|
v
Escalated to Supervisor (if required)
|
v
Understand Cause
|
v
Choose Action
|
+---- Recover
|
+---- Replan
|
+---- Escalate to Human
|
+---- Stop
|
v
Record Decision (in ATE)


---

# Audit Requirements

The Supervisor must maintain visibility of:

- Decisions.
- Approvals.
- Changes.
- Failures.
- Recoveries.

Every major decision must explain:

- What happened?
- Why the decision was made?
- Who approved it?
- What was the result?

---

# Future AI Resume Rule

A future AI must understand:

- The Supervisor is the control layer.
- The Brain provides recommendations.
- The Atomic Task Engine holds all task state.
- The Agent Manager executes approved work, receiving tasks only from ATE.
- Humans retain final authority.
- Supervisor and Agent Manager never communicate directly for routine task flow — ATE mediates.

No critical Supervisor decision should exist only in chat history.

---

# Final Principle

> The Supervisor is the guardian of controlled AI operation. It coordinates intelligence, execution, and safety through the Atomic Task Engine, while ensuring human authority remains above the AI workforce.

---

# Change History

## Version 1.0

- Initial SUPERVISOR.md.
- Corrected Position In System and Communication Model to route through Atomic Task Engine rather than direct Agent Manager contact, matching the pattern established in AGENT_MANAGER.md.
- Added Task Ending States terminology alignment table — flags unresolved mismatch between Supervisor's state vocabulary and ATE's data model, not yet reconciled.
- Aligned document header to standard.