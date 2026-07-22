# OmniForces System Architecture

Status:

Working Architecture Document

Source of Truth:

AI_Workstation contains company-wide standards.

This document defines the OmniForces platform design.

---

# Purpose

OmniForces is an AI engineering platform designed to support safe, structured, AI-assisted software development.

The system allows AI employees to:

- Understand projects.
- Maintain memory.
- Load skills.
- Receive controlled tasks.
- Work within limits.
- Communicate through shared systems.

---

# Core Principle

## The project must survive losing the chat.

Development must not depend on a single AI conversation.

All important information must exist within:

- Documentation.
- Memory systems.
- Resume information.
- Project records.

A new AI session should be able to continue with minimal information loss.

---

# High Level Architecture


Human Leadership

    ↓

Supervisor

    ↓

Agent Manager

    ↓

AI Agents

    ↓

Skills + Memory + Tasks


---

# Core Systems

## Memory System

Purpose:

Provide different levels of knowledge storage.

Components:

### WorkingMemory

Short-term request state.

Used for:

- Current task.
- Current action.
- Temporary information.

---

### SessionMemory

Active development session state.

Used for:

- Current project.
- Milestone.
- Decisions.
- Progress.

---

### LongTermMemory

Persistent project knowledge.

Used for:

- Architecture decisions.
- Learned information.
- Important history.

---

### MemoryManager

Controls all memory access.

Agents should not directly manage memory storage.

---

### Housekeeper

Maintains memory quality.

Responsibilities:

- Archive old information.
- Summarise memories.
- Remove unnecessary data.
- Maintain useful knowledge.

---

# Agent System

Each AI employee contains:

## Agent ID

Identifies the AI employee.

Example:

KC-001

---

## Agent Role

Defines the job responsibility.

Example:

Senior AI Software Engineer

---

## Agent Skills

Loaded when required.

Examples:

- Coding.
- Documentation.
- Testing.
- Research.

---

## Agent Memory

Stores agent-specific context.

---

# Supervisor System

Purpose:

Maintain control and safety.

Responsibilities:

- Approve actions.
- Enforce limits.
- Manage permissions.
- Request human approval when required.

Agents communicate through supervisor control.

---

# Future Job System

Planned:


Supervisor

↓

Job

↓

Atomic Tasks

↓

Agent Actions

↓

Result

↓

Memory Update


---

# Future Workforce

Planned AI employees:

- Development AI.
- Testing AI.
- Documentation AI.
- Research AI.
- AI Supervisor.
- Hermes integration.

---

# Future Automation

Autopilot concept:

Allow approved repetitive work to run automatically.

Examples:

- Documentation updates.
- Testing.
- Maintenance tasks.
- Research tasks.

Human approval remains available for controlled actions.

---

# Documentation Structure

AI_Workstation:

Master company documentation.

OmniForces:

Development workspace.

Rules:

- One source of truth.
- Avoid duplication.
- Promote approved information at milestones.