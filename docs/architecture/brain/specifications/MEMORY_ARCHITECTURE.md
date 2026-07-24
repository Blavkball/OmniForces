# OmniForces Memory Architecture

**Document:** MEMORY_ARCHITECTURE.md

**Version:** 2.0

**Status:** Architecture Approved

**Owner:** KingC Software

**Last Updated:** 23 July 2026

**Source of Truth:**

AI_Workstation contains company-wide engineering standards.

This document defines the OmniForces memory subsystem.

**Engineering Standard:**

KCES_v1.0

**Related Documents:**

- SYSTEM_ARCHITECTURE.md
- BRAIN_ARCHITECTURE.md
- SESSION_RESUME.md
- ATOMIC_TASK_ENGINE.md
- AI_EMPLOYEE_RULES.md

---

# Purpose

The OmniForces memory architecture defines how AI employees maintain useful context across tasks, sessions and long-term development.

Memory exists to:

- Prevent unnecessary knowledge loss.
- Maintain operational continuity.
- Support AI employee workflows.
- Improve future decision making.
- Reduce repeated work.

Memory is not the primary storage location for information.

The Brain manages information.

Memory supports the operation of the Brain and AI workforce.

---

# Core Principle

> Memory remembers what the AI needs to operate. The Brain preserves and organises knowledge.

OmniForces separates:


Information

↓

Brain

↓

Knowledge

↓

Memory

↓

AI Operation


This prevents memory from becoming an uncontrolled storage system.

---

# Relationship Between Brain and Memory

The Brain is responsible for:

- Receiving information.
- Preserving original evidence.
- Organising knowledge.
- Creating relationships.
- Building the Wiki.

Memory is responsible for:

- Maintaining active context.
- Supporting reasoning.
- Preserving useful operational knowledge.
- Supporting continuity.

---

# Brain Architecture Relationship

The complete information architecture is:


Brain

├── Raw
│
├── Wiki
│
├── Working Memory
│
├── Session Memory
│
└── Long-Term Memory


Each component has a different responsibility.

---

# Raw

## Purpose

Raw is the permanent evidence layer.

Raw is not memory.

Raw stores information exactly as received.

Examples:

- Documents.
- Conversations.
- Notes.
- Images.
- Code snippets.
- URLs.
- Specifications.
- Ideas.
- Voice transcripts.
- Tasks.

---

# Raw Rules

Raw is immutable.

Raw must never:

- Be edited.
- Be rewritten.
- Be summarised.
- Be reorganised.
- Be deleted without approval.
- Lose its original content.

Raw provides permanent traceability.

---

# Wiki

## Purpose

Wiki is the structured knowledge layer.

Wiki is created from Raw information.

Wiki does not replace Raw.

---

# Wiki Responsibilities

Wiki creates organised knowledge such as:

- Project information.
- Architecture documentation.
- Decisions.
- Timelines.
- Tasks.
- Relationships.
- Summaries.
- Indexes.
- Technical knowledge.

Every Wiki item should reference its original Raw source.

---

# Memory System

Memory contains three operational layers:


Working Memory

Session Memory

Long-Term Memory


---

# Working Memory

## Purpose

Working Memory stores temporary information required for the current operation.

Scope:

Current task only.

---

# Working Memory Contains

Examples:

- Current objective.
- Active files.
- Current reasoning context.
- Temporary calculations.
- Immediate task information.
- Current AI instructions.

---

# Working Memory Rules

Working Memory:

- Is temporary.
- Can be discarded.
- Does not contain permanent knowledge.
- Supports active execution only.

---

# Session Memory

## Purpose

Session Memory maintains continuity during an engineering session.

Scope:

Current development session.

---

# Session Memory Contains

Examples:

- Current project.
- Current milestone.
- Current objective.
- Completed actions.
- Active decisions.
- Modified files.
- Testing results.
- Next steps.

---

# Session Memory Relationship

Session Memory supports:

- SESSION_RESUME.md
- Engineering sessions.
- Recovery after interruption.

Important session information should be promoted into documentation.

---

# Long-Term Memory

## Purpose

Long-Term Memory stores reusable knowledge that improves future AI operation.

Long-Term Memory is not a document archive.

---

# Long-Term Memory Contains

Examples:

- Proven workflows.
- Engineering patterns.
- Lessons learned.
- User preferences.
- Successful approaches.
- Reusable solutions.

---

# Long-Term Memory Rules

Long-Term Memory should:

- Remain useful.
- Avoid duplication.
- Avoid storing unnecessary information.
- Support future decisions.

---

# Memory Manager

## Purpose

Memory Manager provides controlled access to memory systems.

AI Employees should not directly manage memory storage.

---

# Memory Manager Responsibilities

Memory Manager controls:

- Creating memories.
- Retrieving memories.
- Updating memories.
- Removing outdated memories.
- Applying retention rules.
- Controlling memory access.

---

# Memory Architecture


AI Employee

↓

Memory Manager

↓

Memory Systems

↓

Storage


---

# Housekeeper

## Purpose

The Housekeeper maintains memory quality.

---

# Housekeeper Responsibilities

The Housekeeper:

- Removes unnecessary memories.
- Archives outdated information.
- Identifies duplicates.
- Maintains retention rules.
- Prevents memory overload.

---

# Information Flow


User

↓

Dump

↓

Raw

↓

Indexer

↓

Classifier

↓

Entity Extraction

↓

Relationship Builder

↓

Wiki

↓

Memory Update

↓

AI Workforce


---

# Design Rules

The memory system must:

- Protect information integrity.
- Maintain clear ownership.
- Avoid uncontrolled growth.
- Support recovery.
- Preserve useful context.
- Work with the Brain architecture.

---

# Memory Must Not Replace Documentation

Memory stores:

> Information the AI needs to remember.

Documentation stores:

> Information humans and AI need to understand.

Both systems work together.

Neither replaces the other.

---

# Traceability

Important knowledge must always have an origin.

Information should flow:


Raw Source

↓

Wiki Knowledge

↓

Memory Reference


Generated knowledge without traceability should be avoided.

---

# Future Expansion

Future versions may include:

- Semantic memory search.
- Knowledge graphs.
- Automatic summaries.
- Agent-specific memory.
- Cross-project learning.
- Automatic resume generation.
- Memory scoring.

These features must preserve the separation between:

- Evidence.
- Knowledge.
- Memory.

---

# Final Principle

> The Brain preserves and organises information. Memory provides controlled context for AI operation. Raw protects the evidence. Wiki creates understanding.

OmniForces should never depend on uncontrolled memory.

Knowledge belongs in structured systems.

---

# Change History

## Version 2.0

- Redesigned memory architecture around Brain principles.
- Separated Raw and Wiki from memory responsibilities.
- Defined Raw as immutable evidence storage.
- Defined Wiki as derived knowledge.
- Clarified Working, Session and Long-Term Memory responsibilities.
- Added Memory Manager concept.
- Added Housekeeper responsibility.
- Aligned architecture with OmniForces Information Operating System direction.