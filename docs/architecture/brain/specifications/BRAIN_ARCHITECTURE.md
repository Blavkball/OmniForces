# Brain Architecture

Version:
1.0

Status:
Architecture Draft

Source of Truth:

AI_Workstation is the master company documentation system.

This document defines the Brain architecture for OmniForces.

---

# Purpose

The Brain is the knowledge and information management system for OmniForces.

Its responsibility is to receive information, preserve original evidence, organise knowledge automatically and provide reliable context to the AI workforce.

The Brain does not execute work.

The Brain supplies information to the Supervisor, Agent Manager, AI Employees and future resume systems.

---

# Core Principle

> The user should never be responsible for organising information.

The user provides information.

The Brain organises it.

---

# Brain Structure

```
Brain
│
├── Raw
│
├── Wiki
│
├── Working Memory
│
├── Session Memory
│
└── Long-Term Memory
```

Each component has a single responsibility.

---

# Raw

## Purpose

Raw is the permanent evidence store.

Everything entering OmniForces is stored exactly as received.

Raw is immutable.

---

## Rules

Raw must never:

- Be edited.
- Be rewritten.
- Be summarised.
- Be reorganised.
- Be renamed.
- Be deleted without explicit human approval.

Raw is the permanent source of truth.

---

## Accepted Input

Raw accepts any information including:

- Notes
- Documents
- Specifications
- Images
- PDFs
- Code
- Conversations
- Voice transcripts
- URLs
- Ideas
- Tasks
- Project information

The Brain decides how information should later be organised.

---

# Wiki

## Purpose

Wiki is the structured knowledge layer.

Wiki is generated from Raw.

Wiki never replaces Raw.

---

## Responsibilities

Wiki creates:

- Project pages
- Architecture pages
- Task summaries
- Documentation
- Decisions
- Relationships
- Timelines
- Indexes
- Cross references

Every Wiki page must reference its originating Raw information.

---

# Working Memory

## Purpose

Working Memory stores temporary context required for the current operation.

Examples:

- Current task
- Current file
- Current reasoning
- Active workflow

Working Memory is temporary.

---

# Session Memory

## Purpose

Session Memory records the current development session.

Examples:

- Current milestone
- Current objective
- Active discussions
- Current progress

Session Memory supports interruption recovery.

---

# Long-Term Memory

## Purpose

Long-Term Memory stores reusable knowledge.

Examples:

- Engineering patterns
- Proven workflows
- Lessons learned
- Best practices
- Reusable knowledge

Long-Term Memory does not replace documentation.

---

# Information Flow

```
User
│
▼
Input
│
▼
Raw
│
▼
Classification
│
▼
Relationship Analysis
│
▼
Wiki Generation
│
▼
Memory Update
│
▼
AI Workforce
```

---

# Design Rules

The Brain must:

- Preserve original information.
- Organise information automatically.
- Minimise user effort.
- Maintain traceability.
- Support future AI resume.
- Protect information integrity.

---

# User Experience Rule

The user should never be required to:

- Choose folders.
- Decide categories.
- Create links.
- Build indexes.
- Maintain documentation manually.

The user simply provides information.

The Brain performs the organisation.

---

# Traceability

Every piece of structured knowledge must be traceable back to its original Raw source.

No generated information should exist without a known origin.

---

# Integration

The Brain provides information to:

- Supervisor
- Agent Manager
- Atomic Task Engine
- AI Employees
- Resume Engine
- Documentation System

The Brain does not control execution.

---

# Future Expansion

Future versions may include:

- Automatic entity extraction
- Knowledge graphs
- Duplicate detection
- Semantic search
- Background processing
- Multi-project relationships
- Learning improvements

These features extend the Brain without changing its core responsibilities.

---

# Final Principle

> The Brain exists to preserve knowledge, organise information automatically and provide reliable context. The user supplies information; the Brain performs the organisation while preserving every original source unchanged.