# OmniForces Brain Architecture

**Document:** BRAIN_ARCHITECTURE.md

**Version:** 2.0

**Status:** Architecture Foundation Alignment

**Owner:** KingC Software

**Last Updated:** 23 July 2026

**Source of Truth:** OmniForces

**Engineering Standard:** KCES_v1.0

**Related Documents:**

- SYSTEM_ARCHITECTURE.md
- MEMORY_ARCHITECTURE.md
- SESSION_RESUME.md
- SUPERVISOR.md
- AGENT_MANAGER.md
- ATOMIC_TASK_ENGINE.md
- AI_Workstation/KCEF.md
- AI_Workstation/KCES_v1.0.md

---

# Purpose

The Brain is the knowledge and information operating system of OmniForces.

Its responsibility is to receive information, preserve original evidence, organise knowledge, maintain relationships, and provide reliable context to the AI workforce.

The Brain does not execute work.

The Brain provides information and recommendations to:

- Supervisor.
- Agent Manager.
- AI Employees.
- Atomic Task Engine.
- Resume Engine.
- Documentation systems.

---

# Core Principle

> The user provides information. The Brain organises knowledge.

The user should never be responsible for:

- Organising information.
- Choosing storage locations.
- Creating relationships.
- Maintaining indexes.
- Managing knowledge structure.

The Brain receives unstructured input and creates structured knowledge while preserving the original source.

---

# Architectural Law

## Raw is immutable.

## Wiki is derived.

Raw preserves what happened.

Wiki explains what it means.

Never reverse these responsibilities.

---

# Brain Architecture


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


Each component has one responsibility.

---

# Raw

## Purpose

Raw is the permanent evidence store.

Everything entering OmniForces is stored exactly as received.

Raw is the original source material.

---

# Raw Rules

Raw must never:

- Be edited.
- Be rewritten.
- Be summarised.
- Be reorganised.
- Be renamed.
- Be deleted without explicit human approval.

Raw is immutable.

Once stored, information remains exactly as it arrived.

---

# Raw Examples

Raw may contain:

- Ideas.
- Documents.
- Specifications.
- Notes.
- Screenshots.
- Code snippets.
- URLs.
- Voice transcripts.
- Conversations.
- Meeting information.
- Tasks.
- Research.
- Project information.

Example:


Raw

0001.md
0002.pdf
0003.png
0004.txt
0005.url


Raw is similar to Git history.

The original record is preserved permanently.

---

# Wiki

## Purpose

Wiki is the structured knowledge layer.

Wiki is generated from Raw information.

Wiki does not replace Raw.

---

# Wiki Responsibilities

Wiki creates:

- Project pages.
- Architecture documentation.
- Task summaries.
- Decisions.
- Timelines.
- People information.
- API documentation.
- Relationships.
- Indexes.
- Knowledge summaries.

---

# Wiki Traceability

Every Wiki item must reference its source information.

Example:


Wiki

Project Alpha Architecture

Source:

Raw Item 00142


No generated knowledge should exist without a known origin.

---

# Information Processing Pipeline


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

Wiki Generator

↓

Knowledge Graph


The user interacts mainly with:


Dump

and

Wiki


The middle processing stages are automated.

---

# Dump Principle

The primary user interaction should be:


Dump


Examples:


Dump this document

Dump this conversation

Dump these screenshots

Dump this Git history

Dump today's work

Dump this idea


The Brain determines:

- Project.
- Task.
- Decision.
- Documentation.
- Research.
- Bug.
- Learning.
- Person.
- Relationship.

---

# Working Memory

## Purpose

Working Memory stores temporary context required for active operations.

Examples:

- Current task.
- Current file.
- Current reasoning.
- Active workflow.
- Immediate decisions.

Working Memory is temporary.

---

# Session Memory

## Purpose

Session Memory records the active development session.

Examples:

- Current objective.
- Current milestone.
- Progress.
- Decisions made during the session.
- Recovery information.

Session Memory supports interruption recovery.

---

# Long-Term Memory

## Purpose

Long-Term Memory stores reusable knowledge.

Examples:

- Engineering patterns.
- Proven workflows.
- Lessons learned.
- Preferences.
- Reusable solutions.

Long-Term Memory does not replace:

- Documentation.
- Source code.
- Architecture records.
- Project history.

---

# Memory Relationship

Memory and documentation have different responsibilities.


Raw

↓

Evidence

Wiki

↓

Knowledge

Memory

↓

Context


Documentation preserves permanent knowledge.

Memory provides useful context.

---

# Brain Control Boundaries

The Brain can:

✅ Analyse information.

✅ Create relationships.

✅ Generate recommendations.

✅ Provide context.

✅ Support decisions.


The Brain cannot:

❌ Execute tasks.

❌ Approve actions.

❌ Override Supervisor decisions.

❌ Replace documentation.

❌ Modify Raw information.

---

# Integration With OmniForces

The Brain provides information to:

- Supervisor.
- Agent Manager.
- AI Employees.
- Atomic Task Engine.
- Resume Engine.
- Documentation systems.

The Brain supports intelligence.

The execution systems perform actions.

---

# Knowledge Graph Future Direction

Future Brain versions may include:

- Entity relationships.
- Cross-project connections.
- Semantic search.
- Duplicate detection.
- Knowledge discovery.
- Automatic recommendations.

These extend the Brain without changing its core principles.

---

# Design Rules

The Brain must:

- Preserve original information.
- Maintain traceability.
- Reduce user organisation effort.
- Protect information integrity.
- Support project recovery.
- Improve knowledge retrieval.
- Enable future AI employees.

---

# Recovery Principle

The project must survive losing the chat.

A future AI should be able to:

1. Read company standards.
2. Read OmniForces architecture.
3. Understand current knowledge.
4. Trace decisions back to sources.
5. Continue from documented state.

---

# Final Principle

> The Brain exists to preserve evidence, create knowledge, provide context, and allow AI systems to understand the world around them without losing the original source of truth.

---

# Change History

## Version 2.0

- Redesigned Brain as an Information Operating System.
- Established Raw as immutable evidence storage.
- Established Wiki as derived knowledge.
- Clarified Memory responsibilities.
- Added Dump-first user interaction model.
- Added processing pipeline.
- Added traceability requirements.
- Aligned with SYSTEM_ARCHITECTURE.md v2.0.
- Aligned with KCEF and KCES.