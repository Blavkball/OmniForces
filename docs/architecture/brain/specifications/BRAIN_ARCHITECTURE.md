# OmniForces Brain Architecture

**Document:** BRAIN_ARCHITECTURE.md

**Version:** 2.2

**Status:** Architecture Foundation Alignment

**Owner:** KingC Software

**Last Updated:** 24 July 2026

**Source of Truth:** OmniForces

**Engineering Standard:** KCES_v1.0

**Related Documents:**

- SYSTEM_ARCHITECTURE.md
- MEMORY_ARCHITECTURE.md
- RAW_ARCHITECTURE.md
- WIKI_ARCHITECTURE.md
- BRAIN_PROCESSING_PIPELINE.md
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

Raw and Wiki are specified in full in RAW_ARCHITECTURE.md and WIKI_ARCHITECTURE.md — those are the single source of truth for those two components. This document covers the overall Brain structure and how the components relate, not their internal detail.

Working Memory, Session Memory, and Long-Term Memory are specified in full in MEMORY_ARCHITECTURE.md.

---

# Raw — Summary

Permanent, immutable evidence store. Everything entering OmniForces is preserved exactly as received. Full specification: RAW_ARCHITECTURE.md.

---

# Wiki — Summary

Structured knowledge layer, generated from Raw, always traceable back to its source. Full specification: WIKI_ARCHITECTURE.md.

---

# Information Processing Pipeline

Full pipeline definition, including Validation, all processing stages, and error/recovery handling: BRAIN_PROCESSING_PIPELINE.md. Not repeated here.

Summary only, for orientation:

User
↓
Dump
↓
Raw
↓
Brain Processing Pipeline (see BRAIN_PROCESSING_PIPELINE.md)
↓
Wiki


The user interacts mainly with:

Dump


and

Wiki


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

# Memory — Summary

Working Memory, Session Memory, and Long-Term Memory provide operational context to the AI workforce. Full specification: MEMORY_ARCHITECTURE.md.

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

The Brain CAN:

- Analyse information.
- Create relationships.
- Generate recommendations.
- Provide context.
- Support decisions.

The Brain CANNOT:

- Execute tasks.
- Approve actions.
- Override Supervisor decisions.
- Replace documentation.
- Modify Raw information.

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

# Future Direction

Future Brain and pipeline capability — including Knowledge Graph generation, cross-project connections, semantic search, duplicate detection, and automated recommendations — is defined in BRAIN_PROCESSING_PIPELINE.md's Future Expansion section, aligned to Phase 4 (Automation) of FRAMEWORK_MIGRATION_PLAN.md.

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

## Version 2.1

- Removed duplicate Information Processing Pipeline diagram; now references BRAIN_PROCESSING_PIPELINE.md.
- Removed Knowledge Graph Future Direction section; superseded by BRAIN_PROCESSING_PIPELINE.md's Future Expansion section.
- Replaced ✅/❌ emoji in Brain Control Boundaries with plain CAN/CANNOT text.
- Added BRAIN_PROCESSING_PIPELINE.md to Related Documents.

## Version 2.2

- Removed duplicate Raw Rules, Raw Examples, Wiki Responsibilities, and Wiki Traceability sections; replaced with summaries referencing RAW_ARCHITECTURE.md and WIKI_ARCHITECTURE.md as single sources of truth.
- Removed duplicate Working/Session/Long-Term Memory detail; replaced with summary referencing MEMORY_ARCHITECTURE.md.
- Updated Related Documents to include RAW_ARCHITECTURE.md and WIKI_ARCHITECTURE.md.
- This document now covers Brain structure and component relationships only — detailed specification of each component lives in its own document.