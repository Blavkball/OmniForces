# Graph Report - OmniForces  (2026-08-01)

## Corpus Check
- 33 files · ~7,985 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 232 nodes · 419 edges · 18 communities
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 41 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7b5dfe76`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SupervisorControl
- AtomicTaskEngine
- main.py
- AgentManager
- KnowledgeProvider
- GraphifyContext
- AIKnowledgeContext
- test_ate_integration.py

## God Nodes (most connected - your core abstractions)
1. `AtomicTaskEngine` - 37 edges
2. `AtomicTask` - 26 edges
3. `AgentManager` - 25 edges
4. `SupervisorControl` - 20 edges
5. `TaskEngineError` - 20 edges
6. `GraphifyContext` - 15 edges
7. `AgentManagerError` - 15 edges
8. `KnowledgeProvider` - 14 edges
9. `TaskStatus` - 14 edges
10. `SupervisorControlError` - 13 edges

## Surprising Connections (you probably didn't know these)
- `KnowledgeProvider` --uses--> `GraphifyContext`  [INFERRED]
  app/context/knowledge_provider.py → app/context/graphify_context.py
- `KnowledgeProviderError` --uses--> `GraphifyContext`  [INFERRED]
  app/context/knowledge_provider.py → app/context/graphify_context.py
- `AgentManagerError` --uses--> `SupervisorControl`  [INFERRED]
  app/agents/agent_manager.py → app/supervisor/control.py
- `AgentManagerError` --uses--> `AtomicTask`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py
- `AgentManagerError` --uses--> `AtomicTaskEngine`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py

## Import Cycles
- None detected.

## Communities (18 total, 0 thin omitted)

### Community 0 - "SupervisorControl"
Cohesion: 0.09
Nodes (19): Exception, Records the outcome of an actual human decision on a task sitting in Waiting…, Handles a task that has reached Supervisor Review after a failure. `decision`…, Entry point when Agent Manager reports a task cannot proceed. Moves the task…, Raised when a Supervisor decision is invalid or out of order., Control and decision coordination layer. Holds no task state of its own — task…, Reviews an Assigned task and decides whether it can proceed automatically or…, Evaluates a task against the Human Approval Model. Returns (requires_human:… (+11 more)

### Community 1 - "AtomicTaskEngine"
Cohesion: 0.22
Nodes (9): AtomicTask, AtomicTaskEngine, Exception, Creates, tracks, and closes Atomic Tasks per ATOMIC_TASK_ENGINE.md. ATE does…, Agent Manager status updates during execution that do not change ATE's task…, Resolves a task sitting in Waiting For Human Decision. Approved moves the task…, A task is never orphaned if it has an owner and is either still progressing…, Raised on invalid task creation or an illegal state transition. (+1 more)

### Community 2 - "main.py"
Cohesion: 0.10
Nodes (18): OmniForces Configuration Loads application configuration from the environment.…, Application configuration., Settings, ask_ai(), health(), home(), models(), post (+10 more)

### Community 3 - "AgentManager"
Cohesion: 0.07
Nodes (21): AgentManager, AgentManagerError, Exception, Builds the task-content portion of the prompt from the task's own fields. Role…, Runs a task that is already in Executing (per accept_task) through the real…, Level 1 status update — does not change ATE's task status., Task result available — submits for review. ATE moves the task to Review, not…, Task cannot proceed. Routed through ATE and Supervisor per AGENT_MANAGER.md's… (+13 more)

### Community 4 - "KnowledgeProvider"
Cohesion: 0.07
Nodes (24): KnowledgeProvider, KnowledgeProviderError, Exception, OmniForces Knowledge Provider Central access point for repository knowledge.…, Provides unified knowledge access. Future sources: - Obsidian - Memory - RAG -…, Return repository location., Search code knowledge through Graphify., Find relationships around a code object. (+16 more)

### Community 5 - "GraphifyContext"
Cohesion: 0.14
Nodes (11): GraphifyContext, GraphifyContextError, Exception, OmniForces Graphify Context Reader Reads Graphify output and exposes repository…, Raised when Graphify context cannot be loaded., Provides access to Graphify generated knowledge. Reads: - graph.json -…, Return complete Graphify graph., Return Graphify repository manifest. (+3 more)

### Community 6 - "AIKnowledgeContext"
Cohesion: 0.15
Nodes (10): AIKnowledgeContext, AIKnowledgeContextError, Exception, OmniForces AI Knowledge Context Provider Reads the central KingC Software…, Raised when AI Knowledge cannot be loaded., Provides access to AI_Knowledge., Check AI_Knowledge availability., Read a markdown document from AI_Knowledge root. (+2 more)

### Community 16 - "test_ate_integration.py"
Cohesion: 0.18
Nodes (14): _build_system(), A high-risk task with an irreversible-action flag must stop for a real human…, Execution fails -> Agent Manager reports blocked -> routed through Supervisor…, Execution fails -> escalated -> Supervisor decides cancel, with full…, One shared AtomicTaskEngine, one AgentManager holding one SupervisorControl —…, Sanity sweep: every task created across a full run must resolve to a defined…, Phase 3 exists to make two things true: (1) a task's role selects a non-default…, Human/Supervisor request -> Atomic Task Engine (approval, task state) -> Agent… (+6 more)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AtomicTaskEngine` connect `AtomicTaskEngine` to `SupervisorControl`, `test_ate_integration.py`, `AgentManager`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `AgentManager` connect `AgentManager` to `SupervisorControl`, `AtomicTaskEngine`, `test_ate_integration.py`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `choose_model()` connect `main.py` to `AgentManager`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `AtomicTaskEngine` (e.g. with `AgentManager` and `AgentManagerError`) actually correct?**
  _`AtomicTaskEngine` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `AtomicTask` (e.g. with `AgentManager` and `AgentManagerError`) actually correct?**
  _`AtomicTask` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `AgentManager` (e.g. with `OllamaClient` and `SkillLoader`) actually correct?**
  _`AgentManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `SupervisorControl` (e.g. with `AgentManager` and `AgentManagerError`) actually correct?**
  _`SupervisorControl` has 7 INFERRED edges - model-reasoned connections that need verification._