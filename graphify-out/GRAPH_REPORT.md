# Graph Report - .  (2026-07-31)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 157 nodes · 317 edges · 17 communities (16 shown, 1 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 37 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0f94e8fc`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_ate_integration.py
- AtomicTaskEngine
- main.py
- agent_manager.py
- AgentManager
- SupervisorControl
- OllamaClient
- Human Readable Name

## God Nodes (most connected - your core abstractions)
1. `AtomicTaskEngine` - 37 edges
2. `AtomicTask` - 26 edges
3. `AgentManager` - 25 edges
4. `SupervisorControl` - 20 edges
5. `TaskEngineError` - 20 edges
6. `AgentManagerError` - 15 edges
7. `TaskStatus` - 14 edges
8. `SupervisorControlError` - 13 edges
9. `SkillLoader` - 11 edges
10. `_FakeOllamaClient` - 11 edges

## Surprising Connections (you probably didn't know these)
- `AgentManagerError` --uses--> `OllamaClient`  [INFERRED]
  app/agents/agent_manager.py → app/ollama.py
- `AgentManagerError` --uses--> `SupervisorControl`  [INFERRED]
  app/agents/agent_manager.py → app/supervisor/control.py
- `AgentManagerError` --uses--> `AtomicTask`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py
- `AgentManagerError` --uses--> `AtomicTaskEngine`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py
- `AgentManagerError` --uses--> `TaskEngineError`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Human Readable Label** — src_auth_session [EXTRACTED|INFERRED 0.75]

## Communities (17 total, 1 thin omitted)

### Community 0 - "test_ate_integration.py"
Cohesion: 0.11
Nodes (26): Exception, Raised when a Supervisor decision is invalid or out of order., SupervisorControlError, ExecutionEvent, _now(), RiskLevel, TaskStatus, _build_system() (+18 more)

### Community 1 - "AtomicTaskEngine"
Cohesion: 0.22
Nodes (9): AtomicTask, AtomicTaskEngine, Exception, Creates, tracks, and closes Atomic Tasks per ATOMIC_TASK_ENGINE.md. ATE does…, Agent Manager status updates during execution that do not change ATE's task…, Resolves a task sitting in Waiting For Human Decision. Approved moves the task…, A task is never orphaned if it has an owner and is either still progressing…, Raised on invalid task creation or an illegal state transition. (+1 more)

### Community 2 - "main.py"
Cohesion: 0.13
Nodes (15): ask_ai(), health(), home(), models(), post, choose_model(), ModelRouter, OmniForces Model Router Purpose: Centralised model selection for AI Employees.… (+7 more)

### Community 3 - "agent_manager.py"
Cohesion: 0.14
Nodes (8): AgentManagerError, Exception, Raised when Agent Manager cannot accept or process a task as given., Accepts a task from ATE. Validates it carries the required fields and is in an…, get_role_context(), Returns the full system-context string for a role: shared Engineering…, Loads skills for AI agents when required., SkillLoader

### Community 4 - "AgentManager"
Cohesion: 0.16
Nodes (8): AgentManager, Builds the task-content portion of the prompt from the task's own fields. Role…, Runs a task that is already in Executing (per accept_task) through the real…, Level 1 status update — does not change ATE's task status., Task result available — submits for review. ATE moves the task to Review, not…, Task cannot proceed. Routed through ATE and Supervisor per AGENT_MANAGER.md's…, Confirms an agent's registered limit satisfies a required permission level…, Coordinates AI agents. Never receives a task directly from Supervisor — every…

### Community 5 - "SupervisorControl"
Cohesion: 0.13
Nodes (7): Records the outcome of an actual human decision on a task sitting in Waiting…, Handles a task that has reached Supervisor Review after a failure. `decision`…, Entry point when Agent Manager reports a task cannot proceed. Moves the task…, Control and decision coordination layer. Holds no task state of its own — task…, Reviews an Assigned task and decides whether it can proceed automatically or…, Evaluates a task against the Human Approval Model. Returns (requires_human:…, SupervisorControl

### Community 6 - "OllamaClient"
Cohesion: 0.16
Nodes (8): OmniForces Configuration Loads application configuration from the environment.…, Application configuration., Settings, OmniForces Logger Provides a shared logger for all application modules., AIResponse, OllamaClient, Provider interface for Ollama. Responsibilities: - Connect to Ollama. - Send…, Generate a response using the supplied model. If no model is supplied, the…

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AtomicTaskEngine` connect `AtomicTaskEngine` to `test_ate_integration.py`, `agent_manager.py`, `AgentManager`, `SupervisorControl`, `OllamaClient`?**
  _High betweenness centrality (0.205) - this node is a cross-community bridge._
- **Why does `AgentManager` connect `AgentManager` to `test_ate_integration.py`, `AtomicTaskEngine`, `agent_manager.py`, `SupervisorControl`, `OllamaClient`?**
  _High betweenness centrality (0.194) - this node is a cross-community bridge._
- **Why does `choose_model()` connect `main.py` to `agent_manager.py`, `AgentManager`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `AtomicTaskEngine` (e.g. with `AgentManager` and `AgentManagerError`) actually correct?**
  _`AtomicTaskEngine` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `AtomicTask` (e.g. with `AgentManager` and `AgentManagerError`) actually correct?**
  _`AtomicTask` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `AgentManager` (e.g. with `OllamaClient` and `SkillLoader`) actually correct?**
  _`AgentManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `SupervisorControl` (e.g. with `AgentManager` and `AgentManagerError`) actually correct?**
  _`SupervisorControl` has 7 INFERRED edges - model-reasoned connections that need verification._