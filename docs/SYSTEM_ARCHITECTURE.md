# OmniForces System Architecture

**Document:** SYSTEM_ARCHITECTURE.md

**Version:** 2.0

**Status:** Architecture Foundation Alignment

**Owner:** KingC Software

**Last Updated:** 23 July 2026

**Source of Truth:** OmniForces

**Engineering Standard:** KCES_v1.0

**Related Documents:**

- SESSION_RESUME.md
- BRAIN_ARCHITECTURE.md
- MEMORY_ARCHITECTURE.md
- SUPERVISOR.md
- AGENT_MANAGER.md
- ATOMIC_TASK_ENGINE.md
- AI_EMPLOYEE_RULES.md
- AI_Workstation/KCEF.md
- AI_Workstation/KCES_v1.0.md

---

# Purpose

OmniForces is a controlled AI engineering platform designed to enable AI employees to perform useful work while maintaining:

- Human authority.
- Safety.
- Accountability.
- Recovery.
- Documentation.
- Long-term continuity.

The architecture provides a structured environment where intelligence, execution, memory, and knowledge systems operate together.

The system must remain understandable and recoverable even when previous AI sessions are unavailable.

---

# Core Architecture Principle

> Intelligence may be distributed, but control must remain structured.

OmniForces separates:

- Human authority.
- Reasoning.
- Knowledge.
- Memory.
- Decision approval.
- Execution.
- Documentation.
- Audit history.

No AI component has unrestricted authority.

---

# High-Level Architecture


Human Authority

    |

    v

Supervisor

    |

    v

Agent Manager

    |

    v

AI Employees

    |

    v

Atomic Task Engine

    |

    v

Execution Systems

    |

    +----------------------+
    |                      |
    v                      v

Memory Systems Documentation Systems
|
v

Brain Knowledge Architecture


---

# System Layers

## Layer 1 — Human Authority

Purpose:

Maintain final control over objectives, priorities, and approval.

Human responsibilities:

- Define goals.
- Approve major decisions.
- Set priorities.
- Review outcomes.
- Maintain business direction.

Human authority remains above all AI systems.

---

# Layer 2 — Supervisor

Purpose:

Controlled decision and coordination layer.

Responsibilities:

- Review objectives.
- Validate plans.
- Coordinate AI workforce.
- Manage exceptions.
- Request human approval.
- Control replanning.

The Supervisor does not replace human judgement.

See:


SUPERVISOR.md


---

# Layer 3 — Brain Architecture

Purpose:

Provide intelligence and knowledge capabilities.

The Brain is not only a reasoning system.

The Brain is the knowledge operating system of OmniForces.

Responsibilities:

- Analyse information.
- Build understanding.
- Generate recommendations.
- Manage knowledge relationships.
- Provide context.
- Support decision making.

The Brain does not directly execute work.

Flow:


Information

↓

Brain Processing

↓

Knowledge

↓

Recommendation

↓

Supervisor Decision

↓

Execution


See:


BRAIN_ARCHITECTURE.md


---

# Brain Architecture Model

The Brain consists of multiple knowledge layers.


Brain

├── Raw Knowledge
│
├── Processing Layer
│
├── Wiki Knowledge
│
├── Working Memory
│
├── Session Memory
│
└── Long-Term Memory


Core rules:


Raw is immutable.

Wiki is derived.

Memory provides context.

Documentation preserves knowledge.


---

# Layer 4 — Agent Manager

Purpose:

Operational control system for AI Employees.

Responsibilities:

- Register agents.
- Manage agent lifecycle.
- Assign tasks.
- Enforce permissions.
- Monitor activity.
- Track recovery.
- Maintain audit records.

The Agent Manager executes approved decisions.

It does not create business objectives.

See:


AGENT_MANAGER.md


---

# Layer 5 — AI Employees

Purpose:

Perform approved work.

AI Employees provide:

- Skills.
- Analysis.
- Implementation.
- Research.
- Testing.
- Documentation.

They operate under:

- Supervisor authority.
- Agent Manager control.
- Atomic Task rules.
- KCES standards.

See:


AI_EMPLOYEE_RULES.md


---

# Layer 6 — Atomic Task Engine

Purpose:

Convert objectives into controlled units of work.

Every AI activity should become an Atomic Task.

Each Atomic Task contains:

- Identity.
- Purpose.
- Owner.
- Status.
- Permissions.
- Success criteria.
- Testing requirements.
- Recovery information.
- Audit history.

A task must always have a known state.

See:


ATOMIC_TASK_ENGINE.md


---

# Supporting Architecture Systems

## Resume Engine

Purpose:

Maintain project continuity.

Future functionality:

- Generate resume information.
- Record milestones.
- Track current objectives.
- Identify next tasks.
- Provide AI restart capability.

Goal:

Any authorised AI should resume work from documented project state.

---

## Skills System

Purpose:

Provide controlled capabilities to AI Employees.

Skills define:

- Available actions.
- Required permissions.
- Usage rules.
- Validation requirements.

---

## Job System

Purpose:

Manage scheduled or automated work.

Responsibilities:

- Queue tasks.
- Execute approved jobs.
- Monitor progress.
- Record results.

---

## Knowledge Graph

Purpose:

Connect related knowledge across OmniForces.

The Knowledge Graph supports:

- Relationships.
- Discovery.
- Context.
- Decision support.

---

# Execution Flow

Normal operation:


Human Request

↓

Supervisor Review

↓

Create Atomic Task

↓

Agent Manager Assignment

↓

AI Employee Execution

↓

Result Validation

↓

Memory Update

↓

Documentation Update

↓

Commit / Resume Update


---

# Failure and Recovery Flow

When failure occurs:


Failure

↓

AI Employee Report

↓

Agent Manager Detection

↓

Supervisor Review

↓

Recovery

or

Escalation

↓

Resume Task


A failure must never become abandoned work.

---

# No Orphaned Work Principle

Every task must always have:

- Owner.
- Status.
- History.
- Next action.
- Recovery route.

A task may only finish as:


Completed

Failed With Explanation

Cancelled With Reason

Escalated

Waiting For Decision


---

# Memory Architecture

Memory supports:

- Context.
- Continuity.
- Learning.
- Recovery.

Memory does not replace documentation.

Important knowledge must become permanent through:

- Documentation.
- Decisions.
- Architecture records.
- Project history.

See:


MEMORY_ARCHITECTURE.md


---

# Documentation Architecture

Documentation is the permanent knowledge layer.

Structure:


AI_Workstation

├── Company Standards
├── Engineering Rules
├── Policies
└── Frameworks

OmniForces

├── Architecture
├── Design Decisions
├── Current Development State
├── Resume Information
└── Technical Documentation


Documentation and source code must remain synchronised.

---

# Security Architecture

All actions follow:


Request

↓

Authentication

↓

Permission Check

↓

Supervisor / Agent Manager Control

↓

Execution

↓

Audit Record


No uncontrolled actions enter the AI workforce.

---

# Audit Architecture

Important events are recorded:

- Decisions.
- Approvals.
- Actions.
- Errors.
- Recoveries.
- Results.

Every major action should answer:


What happened?

Why?

Who approved?

What was the outcome?


---

# Recovery Architecture

The project must survive losing the chat.

A new AI session must be able to:

1. Read company standards.
2. Understand architecture.
3. Find current milestone.
4. Identify completed work.
5. Continue from the next Atomic Task.

Required documents:


AI_Workstation:

CURRENT_STATUS.md
AI_ONBOARDING.md
KCES_v1.0.md

OmniForces:

SESSION_RESUME.md
SYSTEM_ARCHITECTURE.md
BRAIN_ARCHITECTURE.md
MEMORY_ARCHITECTURE.md
SUPERVISOR.md
AGENT_MANAGER.md
ATOMIC_TASK_ENGINE.md


---

# Design Philosophy

OmniForces follows:


Understand

↓

Plan

↓

Create Atomic Task

↓

Execute

↓

Test

↓

Document

↓

Commit

↓

Resume


---

# Final Principle

> OmniForces is a controlled AI engineering architecture where human authority, intelligence, knowledge, memory, execution, and documentation work together to build reliable software that can continue beyond any single AI session.

---

# Change History

## Version 2.0

- Expanded Brain from reasoning layer into knowledge architecture.
- Added Brain knowledge layers.
- Added Resume Engine direction.
- Added Skills System direction.
- Added Job System direction.
- Added Knowledge Graph direction.
- Aligned architecture with KCEF and KCES.
- Improved recovery and continuity model.