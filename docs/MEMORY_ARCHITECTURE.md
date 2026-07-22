# OmniForces Memory Architecture

Status:

Working Architecture Document

Source of Truth:

AI_Workstation contains company-wide standards.

This document defines the OmniForces memory subsystem.

---

# Purpose

The memory system allows AI employees to maintain useful information across:

- Tasks.
- Sessions.
- Projects.
- Long-term development.

Memory exists to prevent knowledge loss and reduce repeated work.

---

# Memory Design Principle

Memory should be:

- Useful.
- Controlled.
- Searchable.
- Maintainable.

The system should not store everything forever.

The Housekeeper maintains memory quality.

---

# Memory Layers

## WorkingMemory

Purpose:

Short-term request memory.

Scope:

Current task only.

Stores:

- Current action.
- Temporary context.
- Active files.
- Immediate notes.

Example:

```text
Task:
Create Agent Manager

Files:
agent_manager.py

Status:
Testing
SessionMemory

Purpose:

Active development session memory.

Scope:

Current working session.

Stores:

Project.
Milestone.
Current task.
Decisions.
Progress.
Edited files.

Example:

Project:
OmniForces

Milestone:
Milestone 3

Task:
Agent Foundation
LongTermMemory

Purpose:

Permanent project knowledge.

Scope:

Long-term information.

Stores:

Architecture decisions.
Important lessons.
Project knowledge.
System history.

Example:

Architecture:

MemoryManager controls memory access.
MemoryManager

Purpose:

Single access point for all memory operations.

Agents should not directly manage memory storage.

Responsibilities:

Create memory.
Read memory.
Update memory.
Save memory.
Retrieve information.

Architecture:

AI Agent

↓

MemoryManager

↓

Memory Systems

↓

Storage
Housekeeper

Purpose:

Maintain clean memory.

Responsibilities:

Archive old memories.
Summarise information.
Remove unnecessary data.
Apply retention policies.

The goal:

Keep useful knowledge while avoiding memory overload.

Future Memory Improvements

Planned:

Automatic summaries.
Memory search.
Project awareness.
Agent-specific memory.
Shared knowledge between approved agents.
Automatic resume generation.
Memory Rules

Always:

Store important decisions.
Protect useful knowledge.
Keep information organised.
Remove outdated information.

Never:

Store unnecessary temporary data forever.
Allow uncontrolled memory growth.
Relationship With Documentation

Memory stores:

"Things the AI needs to remember."

Documentation stores:

"Things humans and AI need to understand."

Both work together but have different purposes.