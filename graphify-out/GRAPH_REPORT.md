# Graph Report - OmniForces  (2026-08-02)

## Corpus Check
- 36 files · ~8,337 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 271 nodes · 462 edges · 21 communities (19 shown, 2 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 37 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `49fc239d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_ate_integration.py
- AtomicTaskEngine
- main.py
- AgentManager
- RepositoryContext
- GraphifyContext
- AIKnowledgeContext
- test_memory.py
- KnowledgeProvider
- ObsidianContext
- SupervisorControl
- Exception

## God Nodes (most connected - your core abstractions)
1. `AtomicTaskEngine` - 37 edges
2. `AtomicTask` - 26 edges
3. `AgentManager` - 25 edges
4. `TaskEngineError` - 20 edges
5. `SupervisorControl` - 19 edges
6. `AgentManagerError` - 15 edges
7. `TaskStatus` - 14 edges
8. `ObsidianContext` - 13 edges
9. `KnowledgeProvider` - 13 edges
10. `SupervisorControlError` - 13 edges

## Surprising Connections (you probably didn't know these)
- `AgentManagerError` --uses--> `SupervisorControl`  [INFERRED]
  app/agents/agent_manager.py → app/supervisor/control.py
- `AgentManagerError` --uses--> `AtomicTask`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py
- `AgentManagerError` --uses--> `AtomicTaskEngine`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py
- `AgentManagerError` --uses--> `TaskEngineError`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py
- `AgentManagerError` --uses--> `TaskStatus`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py

## Import Cycles
- None detected.

## Communities (21 total, 2 thin omitted)

### Community 0 - "test_ate_integration.py"
Cohesion: 0.09
Nodes (27): Exception, Raised when a Supervisor decision is invalid or out of order., SupervisorControlError, ExecutionEvent, _now(), RiskLevel, TaskStatus, _build_system() (+19 more)

### Community 1 - "AtomicTaskEngine"
Cohesion: 0.22
Nodes (9): AtomicTask, AtomicTaskEngine, Exception, Creates, tracks, and closes Atomic Tasks per ATOMIC_TASK_ENGINE.md. ATE does…, Agent Manager status updates during execution that do not change ATE's task…, Resolves a task sitting in Waiting For Human Decision. Approved moves the task…, A task is never orphaned if it has an owner and is either still progressing…, Raised on invalid task creation or an illegal state transition. (+1 more)

### Community 2 - "main.py"
Cohesion: 0.10
Nodes (18): OmniForces Configuration Loads application configuration from the environment.…, Application configuration., Settings, ask_ai(), health(), home(), models(), post (+10 more)

### Community 3 - "AgentManager"
Cohesion: 0.07
Nodes (21): AgentManager, AgentManagerError, Exception, Builds the task-content portion of the prompt from the task's own fields. Role…, Runs a task that is already in Executing (per accept_task) through the real…, Level 1 status update — does not change ATE's task status., Task result available — submits for review. ATE moves the task to Review, not…, Task cannot proceed. Routed through ATE and Supervisor per AGENT_MANAGER.md's… (+13 more)

### Community 4 - "RepositoryContext"
Cohesion: 0.15
Nodes (10): Exception, OmniForces Repository Context Provider Provides access to connected KingC…, Raised when repository context cannot be loaded., Provides repository awareness for OmniForces., Return registered repositories., Return a specific repository path., Check repository availability., Return repositories currently available. (+2 more)

### Community 5 - "GraphifyContext"
Cohesion: 0.14
Nodes (11): GraphifyContext, GraphifyContextError, Exception, OmniForces Graphify Context Reader Reads Graphify output and exposes repository…, Raised when Graphify context cannot be loaded., Provides access to Graphify generated knowledge. Reads: - graph.json -…, Return complete Graphify graph., Return Graphify repository manifest. (+3 more)

### Community 6 - "AIKnowledgeContext"
Cohesion: 0.15
Nodes (10): AIKnowledgeContext, AIKnowledgeContextError, Exception, OmniForces AI Knowledge Context Provider Reads the central KingC Software…, Raised when AI Knowledge cannot be loaded., Provides access to AI_Knowledge., Check AI_Knowledge availability., Read a markdown document from AI_Knowledge root. (+2 more)

### Community 16 - "KnowledgeProvider"
Cohesion: 0.08
Nodes (18): ContextBuilder, OmniForces Context Builder Creates structured AI employee context., Build complete context package., KnowledgeProvider, KnowledgeProviderError, OmniForces Knowledge Provider Central knowledge access layer. Provides: -…, Unified knowledge search., Return repository path. (+10 more)

### Community 18 - "ObsidianContext"
Cohesion: 0.14
Nodes (15): ObsidianContext, ObsidianContextError, OmniForces Obsidian Context Provider Reads the human knowledge vault…, Raised when Obsidian vault cannot be loaded., Provides access to the Obsidian vault., Check vault availability., Return all markdown note filenames in the vault., Read a single note from the vault root. (+7 more)

### Community 19 - "SupervisorControl"
Cohesion: 0.14
Nodes (7): Records the outcome of an actual human decision on a task sitting in Waiting…, Handles a task that has reached Supervisor Review after a failure. `decision`…, Entry point when Agent Manager reports a task cannot proceed. Moves the task…, Control and decision coordination layer. Holds no task state of its own — task…, Reviews an Assigned task and decides whether it can proceed automatically or…, Evaluates a task against the Human Approval Model. Returns (requires_human:…, SupervisorControl

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AtomicTaskEngine` connect `AtomicTaskEngine` to `test_ate_integration.py`, `SupervisorControl`, `AgentManager`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `AgentManager` connect `AgentManager` to `test_ate_integration.py`, `AtomicTaskEngine`, `SupervisorControl`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `AtomicTaskEngine` (e.g. with `AgentManager` and `AgentManagerError`) actually correct?**
  _`AtomicTaskEngine` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `AtomicTask` (e.g. with `AgentManager` and `AgentManagerError`) actually correct?**
  _`AtomicTask` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `AgentManager` (e.g. with `OllamaClient` and `SkillLoader`) actually correct?**
  _`AgentManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TaskEngineError` (e.g. with `AgentManager` and `AgentManagerError`) actually correct?**
  _`TaskEngineError` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `SupervisorControl` (e.g. with `AgentManager` and `AgentManagerError`) actually correct?**
  _`SupervisorControl` has 7 INFERRED edges - model-reasoned connections that need verification._