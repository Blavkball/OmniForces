# Graph Report - OmniForces  (2026-08-02)

## Corpus Check
- 36 files · ~8,428 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 277 nodes · 471 edges · 24 communities (20 shown, 4 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 37 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b2eb3992`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- agent_manager.py
- AtomicTaskEngine
- main.py
- AgentManager
- RepositoryContext
- GraphifyContext
- AIKnowledgeContext
- test_memory.py
- KnowledgeProvider
- ObsidianContext
- OllamaClient
- Exception
- _build_system
- SkillLoader
- test_supervisor.py

## God Nodes (most connected - your core abstractions)
1. `AtomicTaskEngine` - 37 edges
2. `AtomicTask` - 26 edges
3. `AgentManager` - 25 edges
4. `TaskEngineError` - 20 edges
5. `SupervisorControl` - 19 edges
6. `KnowledgeProvider` - 16 edges
7. `AgentManagerError` - 15 edges
8. `TaskStatus` - 14 edges
9. `ObsidianContext` - 13 edges
10. `SupervisorControlError` - 13 edges

## Surprising Connections (you probably didn't know these)
- `AgentManagerError` --uses--> `OllamaClient`  [INFERRED]
  app/agents/agent_manager.py → app/ollama.py
- `AgentManagerError` --uses--> `SkillLoader`  [INFERRED]
  app/agents/agent_manager.py → app/skills/skill_loader.py
- `AgentManagerError` --uses--> `AtomicTask`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py
- `AgentManagerError` --uses--> `AtomicTaskEngine`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py
- `AgentManagerError` --uses--> `TaskEngineError`  [INFERRED]
  app/agents/agent_manager.py → app/tasks/atomic_task_engine.py

## Import Cycles
- None detected.

## Communities (24 total, 4 thin omitted)

### Community 0 - "agent_manager.py"
Cohesion: 0.09
Nodes (24): AgentManagerError, Exception, Raised when Agent Manager cannot accept or process a task as given., Exception, Records the outcome of an actual human decision on a task sitting in Waiting…, Handles a task that has reached Supervisor Review after a failure. `decision`…, Entry point when Agent Manager reports a task cannot proceed. Moves the task…, Raised when a Supervisor decision is invalid or out of order. (+16 more)

### Community 1 - "AtomicTaskEngine"
Cohesion: 0.22
Nodes (9): AtomicTask, AtomicTaskEngine, Exception, Creates, tracks, and closes Atomic Tasks per ATOMIC_TASK_ENGINE.md. ATE does…, Agent Manager status updates during execution that do not change ATE's task…, Resolves a task sitting in Waiting For Human Decision. Approved moves the task…, A task is never orphaned if it has an owner and is either still progressing…, Raised on invalid task creation or an illegal state transition. (+1 more)

### Community 2 - "main.py"
Cohesion: 0.13
Nodes (15): ask_ai(), health(), home(), models(), post, choose_model(), ModelRouter, OmniForces Model Router Purpose: Centralised model selection for AI Employees.… (+7 more)

### Community 3 - "AgentManager"
Cohesion: 0.11
Nodes (11): AgentManager, Builds the task-content portion of the prompt from the task's own fields. Role…, Runs a task that is already in Executing (per accept_task) through the real…, Level 1 status update — does not change ATE's task status., Task result available — submits for review. ATE moves the task to Review, not…, Task cannot proceed. Routed through ATE and Supervisor per AGENT_MANAGER.md's…, Confirms an agent's registered limit satisfies a required permission level…, Coordinates AI agents. Never receives a task directly from Supervisor — every… (+3 more)

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
Nodes (19): ContextBuilder, OmniForces Context Builder Creates structured AI employee context., Build complete context package., KnowledgeProvider, OmniForces Knowledge Provider Central knowledge access layer. Provides: -…, Return a single Obsidian note. Args: filename: Markdown filename. Returns: str:…, Unified knowledge search. Returns knowledge collected from every available…, Central access point for all knowledge sources used by OmniForces. (+11 more)

### Community 18 - "ObsidianContext"
Cohesion: 0.12
Nodes (18): KnowledgeProviderError, Raised when the Knowledge Provider encounters an error., ObsidianContext, ObsidianContextError, OmniForces Obsidian Context Provider Reads the human knowledge vault…, Raised when Obsidian vault cannot be loaded., Provides access to the Obsidian vault., Check vault availability. (+10 more)

### Community 19 - "OllamaClient"
Cohesion: 0.18
Nodes (8): OmniForces Configuration Loads application configuration from the environment.…, Application configuration., Settings, OmniForces Logger Provides a shared logger for all application modules., AIResponse, OllamaClient, Provider interface for Ollama. Responsibilities: - Connect to Ollama. - Send…, Generate a response using the supplied model. If no model is supplied, the…

### Community 21 - "_build_system"
Cohesion: 0.17
Nodes (12): _build_system(), A high-risk task with an irreversible-action flag must stop for a real human…, Execution fails -> Agent Manager reports blocked -> routed through Supervisor…, Execution fails -> escalated -> Supervisor decides cancel, with full…, One shared AtomicTaskEngine, one AgentManager holding one SupervisorControl —…, Sanity sweep: every task created across a full run must resolve to a defined…, Human/Supervisor request -> Atomic Task Engine (approval, task state) -> Agent…, test_failure_escalation_cancel_path() (+4 more)

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AtomicTaskEngine` connect `AtomicTaskEngine` to `agent_manager.py`, `AgentManager`, `_build_system`, `SkillLoader`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `AgentManager` connect `AgentManager` to `agent_manager.py`, `AtomicTaskEngine`, `OllamaClient`, `_build_system`, `SkillLoader`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
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