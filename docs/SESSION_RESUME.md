# OmniForces Session Resume

## Document

**Version:** 5.0
**Status:** Active
**Repository:** OmniForces
**Owner:** KingC Software
**Last synchronised commit:** `37b3f7c`

## Purpose

This document is the compact restart point for OmniForces.

It allows a new AI engineer or human engineer to continue development without reconstructing previous chat history.

Prefer this document and the repository source over previous conversations.

---

# Development Rules

For every Atomic Task:

1. Inspect the current repository state.
2. Understand dependencies before making changes.
3. Agree on the design.
4. Replace complete files rather than sending patches.
5. Human tests locally.
6. Commit working changes.
7. Push to GitHub.
8. Rebuild Graphify.
9. Commit Graphify updates.
10. Verify the repository is clean.
11. Move to the next Atomic Task.

Communication should remain:

* Short.
* Focused.
* No repeated decisions.
* Only surface historical information when it affects the current task.

---

# Current Architecture

```text
Supervisor
    |
    v
Atomic Task Engine
    |
    v
AgentManager
    |
    +--------------------+
    |                    |
    v                    v
ContextBuilder      SkillRegistry
    |                    |
    v                    +-- SkillDefinition
KnowledgeProvider       +-- RepositorySkill
    |                    +-- GraphifySkill
    +-- Repository       +-- Cline Skill
    +-- Graphify         +-- Skill execution
    +-- AI_Knowledge
    +-- Obsidian
    |
    v
Prompt Builder
    |
    v
Ollama

Knowledge Injection is complete.

Knowledge context currently uses hard caps rather than relevance ranking.

Future improvement:

RAG/vector search when required.
Phase 4 — Knowledge Injection

Status: COMPLETE

Completed:

AgentManager receives ContextBuilder.
AgentManager retrieves knowledge before execution.
Prompt builder includes relevant knowledge.
Obsidian knowledge is included.
Knowledge output is capped.
Phase 5 — Skill Registry / Skill Execution

Status: COMPLETE FOR CURRENT SCOPE

Current implementation flow:

SkillDefinition
        |
        v
SkillRegistry
        |
        +-- Metadata
        +-- Permissions
        +-- Validation
        +-- Enable / Disable
        +-- Execution
        |
        +----------------+----------------+
        |                |                |
        v                v                v
RepositorySkill    GraphifySkill    Cline Skill
        |
        v
AgentManager
        |
        v
AtomicTask
        |
        +-- skill_action
        +-- skill_args
        |
        v
Skill execution
Completed Atomic Tasks
Atomic Task 1 — Skill Registry Foundation

Status: COMPLETE

Completed:

SkillDefinition established as the skill metadata and execution definition.
SkillRegistry provides registration and retrieval.
Skill validation implemented.
Skill enable/disable handling implemented.
Skill execution support implemented.
Skill permissions represented in skill definitions.
SkillLoader retained as a backwards-compatible layer around the newer registry implementation.
Atomic Task 2 — RepositorySkill

Status: COMPLETE

Completed:

RepositorySkill added using the skill registry.
Controlled repository operations include:
Reading files.
Listing files.
Code search.
Repository access uses the repo:read permission.
Atomic Task 3 — GraphifySkill

Status: COMPLETE

Completed:

GraphifySkill added using the skill registry.
Graph operations include:
Graph summary.
Dependency lookup.
Node search.
Graph queries.
Graph access uses the graphify:read permission.
Atomic Task 4 — AgentManager Skill Integration

Status: COMPLETE

Completed:

AgentManager owns a SkillRegistry.
Agents can be assigned registered skills.
Required skills are validated before execution.
Required permissions are validated before execution.
Disabled skills cannot satisfy required permissions.
Skill execution is available through AgentManager.
Atomic Task 5 — Atomic Task Skill Execution

Status: COMPLETE

Completed:

AtomicTask supports skill_action.
AtomicTask supports skill_args.
AgentManager.execute_task() executes requested skill actions.
Skill arguments are forwarded.
Skill results are added to the execution prompt.
Skill execution failures block the task rather than silently continuing.

Latest implementation commit:

37b3f7c
Atomic Task 5: skill_action execution wired into execute_task
Backwards Compatibility

app/skills/skill_loader.py remains in the repository.

It acts as a compatibility layer around the newer SkillRegistry implementation.

Do not describe SkillLoader as deleted.

New development should target:

SkillDefinition
SkillRegistry

rather than introducing new dictionary-only skill handling.

Skill Permissions

Current permission examples include:

repo:read
graphify:read
repo:write

AgentManager validates the permissions available through an agent's assigned enabled skills before executing tasks that declare required permissions.

Cline Orchestration

Completed:

Dedicated Cline role added.
Cline routed to the configured Llama model.
cline_skill.py created.
Cline skill registered with AgentManager.
Cline agent registration helper added.
Cline orchestration helper added.
POST /cline/orchestrate API endpoint added.
Cline API integration test added.
Cline orchestration events logged.

Possible future work:

Workflow persistence.
History tracing.
AI employee onboarding integration.
Task metadata and team skill profiles.

These are future possibilities, not current commitments.

Test Status

Latest local test run:

67 passed, 1 warning in 3.07s

All tests passed.

The warning is a dependency deprecation involving Starlette's TestClient / httpx integration.

It does not currently cause test failure.

Record it as technical debt for future dependency maintenance.

Atomic Task 6 — Documentation & Knowledge Synchronisation

Status: COMPLETE

Purpose:

Synchronise this session resume with the actual repository so future AI sessions can restart from a compact and accurate source of truth.

Completed:

Updated Phase 5 status.
Recorded Atomic Tasks 1–5.
Documented SkillDefinition.
Documented SkillRegistry.
Documented RepositorySkill.
Documented GraphifySkill.
Documented AgentManager integration.
Documented skill_action.
Documented skill_args.
Documented actual skill execution.
Documented the backwards-compatible SkillLoader layer.
Updated architecture.
Updated test status.
Recorded latest known commit.
Verified the complete local test suite.
Next Development Task

Do not begin another feature automatically.

First inspect:

Skill execution edge cases.
Permission boundaries.
Atomic Task / skill result structure.
Graphify integration depth.
RepositorySkill integration depth.
Cline orchestration persistence.
AI employee skill profiles.

Then select one Atomic Task.

Do not combine multiple feature areas into one task.

Project Philosophy

OmniForces is becoming an AI engineering operating system.

AI models       = Employees
Skills          = Capabilities
Knowledge       = Memory
Graphify        = Architectural awareness
AgentManager    = Coordination
Atomic Tasks    = Controlled work units

The goal is not simply to create many AI agents.

The goal is to create specialised AI employees that share the same engineering environment.

Current Repository State

Repository:

OmniForces

Branch:

main

Latest known GitHub commit:

37b3f7c

Current milestone:

Phase 5 — Skill Registry / Skill Execution

Documentation:

Synchronised

Latest test result:

67 passed, 1 warning
Current Session Position

Atomic Task 6 is complete.

The next action is not another code change yet.

The next action is:

Inspect current implementation
        ↓
Identify the highest-value next improvement
        ↓
Agree Atomic Task
        ↓
Implement
        ↓
Test
        ↓
Commit
        ↓
Push
        ↓
Graphify
        ↓
Verify clean
End of Session Resume