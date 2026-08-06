# OmniForces Session Resume

## Document

**Version:** 4.0
**Status:** Active
**Repository:** OmniForces
**Owner:** KingC Software

## Purpose

Allow a new AI engineer or human engineer to continue development without previous chat history.

---

# Current Development Rules

For every Atomic Task:

1. Inspect current repository state.
2. Understand dependencies before changes.
3. Agree design.
4. Generate complete replacement files only.
5. Human tests locally.
6. Commit.
7. Push.
8. Rebuild Graphify.
9. Commit Graphify updates.
10. Verify clean state.
11. Move to next task.

Keep communication:

* Short.
* Focused.
* No repeated decisions.
* Only raise previous information if it affects current work.

---

# Current Architecture State

Current execution flow:

```
Supervisor
    |
    v
Atomic Task Engine
    |
    v
AgentManager
    |
    v
ContextBuilder
    |
    v
KnowledgeProvider
    |
    +-- Repository Context
    +-- Graphify
    +-- AI_Knowledge
    +-- Obsidian
    |
    v
Prompt Builder
    |
    v
Ollama
```

Knowledge Injection is complete.

Knowledge context currently uses hard caps, not relevance ranking.

Future improvement:

* RAG/vector search replaces hard limits when required.

---

# Completed Work

## Phase 4 — Knowledge Injection

Status:
COMPLETE

Completed:

* AgentManager receives ContextBuilder dependency.
* AgentManager retrieves knowledge before execution.
* Prompt builder includes relevant knowledge sections.
* Obsidian knowledge is included.
* Knowledge output is capped.

Tests:

```
48 passing
0 failing
```

---

# Current Milestone

## Phase 5 — Skill Registry

Status:
IN PROGRESS

Current problem:

`SkillLoader` is only a dictionary:

```python
register_skill(name, description)
```

It stores descriptions only.

AgentManager creates:

```python
self.skill_loader = SkillLoader()
```

but skills are not executed.

---

# Agreed Design

Replace SkillLoader with:

```
SkillRegistry
        |
        +-- SkillDefinition
        |
        +-- Metadata
        +-- Permissions
        +-- Validation
        +-- Execution entry point
```

Initial scope:

DO:

* Register skills.
* Store metadata.
* Retrieve skills.
* Validate skills.
* Enable/disable skills.
* Validate task-required skills during AgentManager execute_task lifecycle.

DO NOT:

* Add real skills yet.
* Modify AgentManager yet.
* Add multi-agent behaviour yet.

---

# Future Skills

After SkillRegistry is stable:

## RepositorySkill

Purpose:
Give agents controlled repository access.

Examples:

* Read file.
* Search code.
* Find symbols.
* Find references.
* Inspect structure.

---

## GraphifySkill

Purpose:
Give agents architectural awareness.

Examples:

* Dependency lookup.
* Call graph queries.
* Component relationships.
* Impact analysis.

---

These should become the foundation for future AI employees.

---

# AI Employee Strategy

Do not add new AI employees until the skill layer exists.

Reason:

New agents without shared skills will duplicate functionality.

Correct order:

1. SkillRegistry
2. Core Skills
3. AgentManager Skill Integration
4. Multi-Agent Delegation
5. Specialist Employees

Future employees:

* Cline — AI Workforce Liaison
* Forge — Software Engineer
* Continue — Research / Knowledge Engineer
* Inspector — Code Review / Quality
* Tester — Testing Specialist
* Librarian — Knowledge Maintenance
* Architect — System Design

---

## Cline Orchestration Integration

Completed:

* Added dedicated `Cline` role in `app/roles.py`.
* Routed `Cline` to `settings.LLAMA_MODEL` in `app/router.py`.
* Created `app/skills/cline_skill.py` with orchestration and agent-summary helpers.
* Wired Cline skill registration into `AgentManager` in `app/agents/agent_manager.py`.
* Added convenience helpers: `register_cline_agent()` and `perform_cline_orchestration()`.
* Added API endpoint `POST /cline/orchestrate` in `app/main.py`.
* Added Cline API integration test in `app/test_cline_api.py`.
* Logged Cline orchestration events with shared `app.logger`.

Next:

* Add Cline orchestration workflow persistence and history tracing.
* Add Cline role to AI employee onboarding docs.
* Extend Cline skill to consume task metadata and team skill profiles.

---

# Current Recommended Next Atomic Tasks

## Atomic Task 1

Replace:

```
app/skills/skill_loader.py
```

with:

```
SkillRegistry
SkillDefinition
```

No AgentManager changes.

---

## Atomic Task 2

Create:

```
RepositorySkill
```

using the new registry.

---

# Current Session Handover

Status: COMPLETE

This repo is now ready for a new AI or engineer to continue without missing context.

Completed in this session:

* AgentManager skill and permission validation implemented.
* Obsidian vault integration added via `knowledge_sources.json` and local `obsidian-vault/`.
* Repository context loaded from known local repos and normalized for relative paths.
* `.gitignore` updated to keep cloned local repos out of the OmniForces repository.
* All changes committed and pushed to `main` on `origin`.

Next step for a new contributor:

1. Checkout `main`.
2. Review `docs/SESSION_RESUME.md` and `app/context/knowledge_provider.py`.
3. Continue with Atomic Task 1: replace `skill_loader.py` with `SkillRegistry` and `SkillDefinition`.
4. Use the local Obsidian vault and `knowledge_sources.json` for knowledge integration.

---

## Atomic Task 3

Create:

```
GraphifySkill
```

using the new registry.

---

## Atomic Task 4

Integrate skills into AgentManager.

Target:

```
AgentManager
       |
       v
SkillRegistry
       |
       v
Execute Skill
```

---

# Project Philosophy

OmniForces is moving toward an AI engineering operating system.

AI models are employees.

Skills are capabilities.

Knowledge systems are memory.

Graphify is architectural awareness.

AgentManager coordinates execution.

The goal is not many AI agents.

The goal is specialised AI employees sharing the same engineering environment.

---

# End State At Last Session

Repository:
OmniForces

Branch:
main

Tests:
48 passing

Working tree:
Clean

Current task:
Phase 5 — Skill Registry
