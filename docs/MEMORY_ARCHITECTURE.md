# OmniForces Memory Architecture

## Purpose

The OmniForces memory system provides structured memory for AI-assisted software development.

The goal is to allow AI agents to maintain useful context while keeping memory controlled, efficient, and maintainable.

---

# Memory Design

OmniForces uses multiple memory layers.


Working Memory
|
v
Session Memory
|
v
Long-Term Memory
|
v
Housekeeper


---

# Working Memory

## Purpose

Temporary memory for the current request.

## Stores

- Current task.
- Temporary context.
- Notes.
- Active files.

## Lifetime

Exists only during the active request.

Working memory should not become permanent knowledge.

---

# Session Memory

## Purpose

Stores the current development session state.

## Stores

- Project.
- Milestone.
- Current task.
- TODO items.
- Decisions.
- Edited files.

## Lifetime

Survives during an active development session.

Can be saved and restored.

---

# Long-Term Memory

## Purpose

Stores important persistent knowledge.

## Stores

- Architecture decisions.
- Project knowledge.
- Engineering rules.
- Historical information.
- Reusable solutions.

Long-term memory should contain valuable knowledge, not every conversation.

---

# Memory Storage

Current implementation:

- JSON storage.
- Human readable.
- Easy backup.
- Easy debugging.

Future options:

- SQLite.
- Search indexes.
- Vector memory.

---

# MemoryManager

MemoryManager is the single access point for all memory operations.

Other systems should not directly control memory components.

Responsibilities:

- Coordinate memory layers.
- Save memory.
- Load memory.
- Provide unified access.

Future AI agents will communicate through MemoryManager.

---

# Housekeeper

The Housekeeper maintains memory health.

Future responsibilities:

- Archive old sessions.
- Remove duplicates.
- Summarise conversations.
- Remove outdated information.
- Maintain clean memory storage.

---

# Future AI Agent Support

The memory system is designed to support future AI employees.

Examples:

- Supervisor.
- Development AI.
- Testing AI.
- Documentation AI.
- Research AI.

Each agent can maintain domain knowledge while sharing approved project knowledge.

---

# Current Status

Milestone:

OmniForces Milestone 3

Completed:

- WorkingMemory.
- SessionMemory.
- LongTermMemory.
- MemoryStorage.
- MemoryManager.
- Housekeeper foundation.
- Persistence testing.
- Integration testing.

---

# Design Principles

The memory system follows KingC Software principles:

- Keep solutions simple.
- Protect working software.
- Separate responsibilities.
- Test before expanding.
- Document important decisions.