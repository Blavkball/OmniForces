# OmniForces Engineering Workflow

Status:

Working Process Document

Source of Truth:

AI_Workstation contains company-wide engineering standards.

This document defines the OmniForces development workflow.

---

# Purpose

Create a repeatable development process that protects:

- Software quality.
- Documentation.
- Knowledge.
- Progress.
- Recovery ability.

---

# Core Principle

## The project must survive losing the chat.

The project should never depend on one conversation.

A new AI session should be able to:

1. Read documentation.
2. Understand the current position.
3. Continue development.

---

# Session Start Procedure

Before development:

Read:

AI_Workstation:

- CURRENT_STATUS.md
- AI_ONBOARDING.md
- DEVELOPMENT_RULES.md
- SESSION_RESUME.md

Then read OmniForces:

- SESSION_NOTES.md
- SYSTEM_ARCHITECTURE.md
- MEMORY_ARCHITECTURE.md
- ENGINEERING_WORKFLOW.md

Confirm:

- Current project.
- Current milestone.
- Last completed task.
- Next task.

---

# Development Process

Every task follows:


Understand

↓

Plan

↓

Build

↓

Test

↓

Document

↓

Commit

↓

Resume Update


---

# Atomic Development

Work should be broken into small safe steps.

Example:

Large task:

Build Agent System

Becomes:

- Create folder.
- Create file.
- Add code.
- Test.
- Verify.
- Document.

Each step should have:

- Clear purpose.
- Clear result.
- Easy recovery.

---

# File Creation Rules

Always create files using the editor.

Correct:

VS Code:

Folder

↓

New File

↓

Filename

Example:

models.py


Avoid:

app/models.py

Reason:

Prevents accidental nested folders.

---

# Coding Rules

Always:

- Replace complete files.
- Test after changes.
- Protect working versions.
- Keep solutions simple.
- Explain important decisions.

Avoid:

- Large uncontrolled changes.
- Unnecessary complexity.
- Breaking working features.

---

# Git Workflow

Before major changes:

Create checkpoint.

During development:

- Commit working code.
- Use clear messages.
- Keep commits logical.

Before ending:

Run:

git status

Repository should be clean.

---

# Documentation Workflow

Working documents:

OmniForces/docs

Master documents:

AI_Workstation

Process:

Build

↓

Update working documentation

↓

Review milestone

↓

Promote approved information

↓

Update AI_Workstation

---

# Session Close Procedure

When user says:

"Stop for today"

Complete:

## Session Close Checklist

□ Code tested

□ Git status checked

□ Working docs updated

□ Master docs updated if milestone complete

□ Completed tasks removed

□ Next atomic task recorded

□ Resume point updated

□ Source of truth verified

□ New ideas captured

□ Ready for any AI to resume

---

# Resume Principle

Every session should leave:

- Working code.
- Clean repository.
- Updated knowledge.
- Clear next action.

---

# Future Automation

OmniForces should eventually create:

resume.json

Containing:

- Project.
- Milestone.
- Last completed task.
- Next task.
- Documents required.
- Git state.

Goal:

Any AI can resume quickly.