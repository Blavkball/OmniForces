# OmniForces Engineering Workflow

**Document:** ENGINEERING_WORKFLOW.md

**Version:** 2.0

**Status:** Approved

**Owner:** KingC Software

**Last Updated:** 23 July 2026

**Source of Truth:** OmniForces

**Engineering Standard:** KCES_v1.0

**Related Documents:**

- AI_Workstation/KCES_v1.0.md
- AI_Workstation/AI_ONBOARDING.md
- SESSION_RESUME.md
- SYSTEM_ARCHITECTURE.md
- MEMORY_ARCHITECTURE.md

---

# Purpose

This document defines the OmniForces development workflow.

It describes **how work is performed within this project**.

Company engineering standards are defined by KCES and are not duplicated here.

---

# Project Objective

Develop OmniForces as a professional AI Engineering Platform through controlled, incremental and well-documented development.

Every implementation should improve:

- Software
- Architecture
- Documentation
- Knowledge
- Maintainability

---

# Development Strategy

OmniForces is developed using incremental milestones.

Each milestone should produce:

- Working software
- Updated documentation
- Clean Git history
- Clear continuation point

Avoid large uncontrolled implementation phases.

---

# Project Workflow

Each feature follows the same lifecycle.

```
Review

↓

Design

↓

Implementation

↓

Testing

↓

Documentation

↓

Commit

↓

Resume Update
```

Project-specific implementation should remain small, testable and recoverable.

---

# Atomic Development

Every feature should be divided into Atomic Tasks.

Each task should:

- Solve one problem.
- Modify the minimum number of files.
- Be independently testable.
- Be easy to review.
- Be easy to recover.

Large objectives are completed through multiple Atomic Tasks.

---

# File Update Policy

Within OmniForces:

- Complete one file before moving to the next.
- Replace complete files unless a smaller change is specifically requested.
- Test completed files before continuing.
- Avoid partially completed implementations.

---

# Architecture First

Before implementing new functionality:

- Review existing architecture.
- Reuse existing components where appropriate.
- Extend architecture instead of replacing it.
- Avoid duplicate systems.

Architecture changes should be documented.

---

# Documentation Workflow

Project documentation is maintained alongside implementation.

When architecture changes:

- Update architecture documents.
- Update SESSION_RESUME.md if project status changes.
- Record significant decisions.
- Ensure documentation matches implementation.

Documentation should always reflect the current state of the project.

---

# Testing Workflow

Every completed Atomic Task should be verified.

Testing may include:

- Application startup
- API validation
- Functional testing
- Integration testing
- Manual verification

Do not continue until the current task is working.

---

# Git Workflow

Development should produce logical Git history.

Recommended workflow:

- Complete Atomic Task.
- Verify implementation.
- Update documentation.
- Commit.
- Confirm clean repository.

Each commit should represent one completed piece of work.

---

# Session Workflow

Every development session should:

- Continue from SESSION_RESUME.md.
- Complete one or more Atomic Tasks.
- Update documentation.
- Leave a clear continuation point.
- Finish with a clean repository.

---

# Architecture Documents

Primary architecture documentation includes:

```
SYSTEM_ARCHITECTURE.md

MEMORY_ARCHITECTURE.md

SUPERVISOR.md

AGENT_MANAGER.md

ATOMIC_TASK_ENGINE.md

AI_EMPLOYEE_RULES.md
```

Review only the documents relevant to the current implementation.

---

# Engineering Principles

Within OmniForces:

- Keep solutions simple.
- Prefer maintainability.
- Protect working software.
- Build incrementally.
- Reduce technical debt.
- Keep documentation current.

---

# Milestone Completion

A milestone is complete when:

- Objectives achieved.
- Software tested.
- Documentation updated.
- Git committed.
- Repository clean.
- SESSION_RESUME.md updated.

---

# Future Automation

OmniForces will eventually automate portions of this workflow through:

- Repository analysis
- Engineering Session Briefing
- Resume generation
- Task planning
- Documentation validation
- Knowledge management

The long-term objective is to reduce manual project administration while maintaining engineering quality.

---

# Change History

## Version 2.0

- Refactored to reference KCES.
- Removed duplicated company engineering standards.
- Focused on OmniForces-specific development workflow.
- Added Atomic Development guidance.
- Simplified project workflow.
- Improved documentation responsibilities.