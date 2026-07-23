# OmniForces Agent Manager Specification

Version:
1.0

Status:
Architecture Complete

Source of Truth:

AI_Workstation is the master company documentation system.

OmniForces Agent Manager documentation defines the project implementation design.

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

---

# Core Principle

> The Agent Manager controls AI Employee operations but does not make business decisions.

The Agent Manager ensures AI Employees operate safely, consistently, and traceably.

---

# Position In System

```
Human
  |
Supervisor
  |
Agent Manager
  |
AI Employees
  |
Atomic Tasks
  |
Results
  |
Memory Update
  |
Documentation Update
```

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

- Receives approved Atomic Tasks.
- Assigns tasks to suitable AI Employees.
- Tracks task progress.
- Collects results.
- Reports completion.

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

```
Healthy
Busy
Waiting
Warning
Failed
Recovery Required
Offline
```

---

# Communication Rules

Communication flow:

```
Supervisor
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
Supervisor
```

AI Employees do not communicate directly with external systems without approved control.

---

# Authority Limits

The Agent Manager CAN:

- Assign approved tasks.
- Monitor agents.
- Check permissions.
- Pause unhealthy agents.
- Start recovery procedures.
- Record events.
- Report problems.

---

The Agent Manager CANNOT:

- Create its own objectives.
- Change task requirements.
- Override Supervisor decisions.
- Grant itself permissions.
- Bypass approval requirements.
- Hide failures.
- Delete audit history.

---

# Error Handling

When an AI Employee fails:

```
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
Supervisor Review
        |
        v
Resolution
        |
        v
Audit Record
```

---

# Recovery Levels

## Level 1 — Automatic Recovery

Allowed:

- Safe restart.
- Retry operation.
- Restore known state.

---

## Level 2 — Supervisor Recovery

Supervisor decides:

- Replan task.
- Assign another AI Employee.
- Request Brain analysis.
- Change execution route.

---

## Level 3 — Human Approval

Required for:

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

Every failed task must become:

```
Completed
OR
Retry
OR
Replanned
OR
Escalated
OR
Cancelled With Reason
```

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

- Task assignments.
- Agent actions.
- Status changes.
- Permission checks.
- Errors.
- Recovery attempts.
- Communication events.
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

```
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
```

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

```
Brain
 |
Recommendation
 |
Supervisor
 |
Decision
 |
Agent Manager
 |
Execution
```

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

No critical knowledge should exist only inside chat history.

---

# Final Principle

> The Agent Manager is the controlled operating layer between the Supervisor and AI Employees. It enables safe execution while preserving human authority, accountability, and system recovery.