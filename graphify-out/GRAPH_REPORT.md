# Graph Report - OmniForces  (2026-08-02)

## Corpus Check
- 36 files · ~8,040 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 273 nodes · 437 edges · 25 communities (21 shown, 4 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 23 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c745c302`
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
- OllamaClient
- Exception
- SupervisorControl
- SkillLoader
- context_builder.py
- Exception

## God Nodes (most connected - your core abstractions)
1. `AtomicTaskEngine` - 33 edges
2. `AtomicTask` - 22 edges
3. `AgentManager` - 18 edges
4. `TaskEngineError` - 17 edges
5. `KnowledgeProvider` - 16 edges
6. `SupervisorControl` - 15 edges
7. `ObsidianContext` - 13 edges
8. `SupervisorControlError` - 13 edges
9. `GraphifyContext` - 11 edges
10. `TaskStatus` - 11 edges

## Surprising Connections (you probably didn't know these)
- `_FakeOllamaClient` --uses--> `AgentManagerError`  [INFERRED]
  app/test_ate_integration.py → app/agents/agent_manager.py
- `_FakeOllamaResponse` --uses--> `AgentManagerError`  [INFERRED]
  app/test_ate_integration.py → app/agents/agent_manager.py
- `_FakeOllamaClient` --uses--> `AgentManager`  [INFERRED]
  app/test_ate_integration.py → app/agents/agent_manager.py
- `_FakeOllamaResponse` --uses--> `AgentManager`  [INFERRED]
  app/test_ate_integration.py → app/agents/agent_manager.py
- `SupervisorControlError` --uses--> `AtomicTask`  [INFERRED]
  app/supervisor/control.py → app/tasks/atomic_task_engine.py

## Import Cycles
- None detected.

## Communities (25 total, 4 thin omitted)

### Community 0 - "test_ate_integration.py"
Cohesion: 0.09
Nodes (27): Exception, Raised when a Supervisor decision is invalid or out of order., SupervisorControlError, ExecutionEvent, _now(), RiskLevel, TaskStatus, _build_system() (+19 more)

### Community 1 - "AtomicTaskEngine"
Cohesion: 0.22
Nodes (9): AtomicTask, AtomicTaskEngine, Exception, Creates, tracks, and closes Atomic Tasks per ATOMIC_TASK_ENGINE.md. ATE does…, Agent Manager status updates during execution that do not change ATE's task…, Resolves a task sitting in Waiting For Human Decision. Approved moves the task…, A task is never orphaned if it has an owner and is either still progressing…, Raised on invalid task creation or an illegal state transition. (+1 more)

### Community 2 - "main.py"
Cohesion: 0.13
Nodes (15): ask_ai(), health(), home(), models(), post, choose_model(), ModelRouter, OmniForces Model Router Purpose: Centralised model selection for AI Employees.… (+7 more)

### Community 3 - "AgentManager"
Cohesion: 0.12
Nodes (9): AgentManager, AgentManagerError, Raised when Agent Manager cannot accept or process a task., Coordinates AI agents. Agent Manager: - does not create tasks - does not…, get_role_context(), Returns the full system-context string for a role: shared Engineering…, AtomicTask, AtomicTaskEngine (+1 more)

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
Cohesion: 0.10
Nodes (16): KnowledgeProvider, OmniForces Knowledge Provider Central knowledge access layer. Provides: -…, Return a single Obsidian note. Args: filename: Markdown filename. Returns: str:…, Unified knowledge search. Returns knowledge collected from every available…, Central access point for all knowledge sources used by OmniForces., Return the path to a repository by name., Search Graphify code knowledge., Search Graphify relationships. (+8 more)

### Community 18 - "ObsidianContext"
Cohesion: 0.12
Nodes (18): KnowledgeProviderError, Raised when the Knowledge Provider encounters an error., ObsidianContext, ObsidianContextError, OmniForces Obsidian Context Provider Reads the human knowledge vault…, Raised when Obsidian vault cannot be loaded., Provides access to the Obsidian vault., Check vault availability. (+10 more)

### Community 19 - "OllamaClient"
Cohesion: 0.18
Nodes (8): OmniForces Configuration Loads application configuration from the environment.…, Application configuration., Settings, OmniForces Logger Provides a shared logger for all application modules., AIResponse, OllamaClient, Provider interface for Ollama. Responsibilities: - Connect to Ollama. - Send…, Generate a response using the supplied model. If no model is supplied, the…

### Community 21 - "SupervisorControl"
Cohesion: 0.14
Nodes (7): Records the outcome of an actual human decision on a task sitting in Waiting…, Handles a task that has reached Supervisor Review after a failure. `decision`…, Entry point when Agent Manager reports a task cannot proceed. Moves the task…, Control and decision coordination layer. Holds no task state of its own — task…, Reviews an Assigned task and decides whether it can proceed automatically or…, Evaluates a task against the Human Approval Model. Returns (requires_human:…, SupervisorControl

### Community 23 - "context_builder.py"
Cohesion: 0.33
Nodes (3): ContextBuilder, OmniForces Context Builder Creates structured AI employee context., Build complete context package.

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AgentManagerError` connect `AgentManager` to `test_ate_integration.py`, `ObsidianContext`?**
  _High betweenness centrality (0.444) - this node is a cross-community bridge._
- **Why does `KnowledgeProviderError` connect `ObsidianContext` to `KnowledgeProvider`?**
  _High betweenness centrality (0.349) - this node is a cross-community bridge._
- **Why does `AtomicTaskEngine` connect `AtomicTaskEngine` to `test_ate_integration.py`, `SupervisorControl`?**
  _High betweenness centrality (0.166) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `AtomicTaskEngine` (e.g. with `SupervisorControl` and `SupervisorControlError`) actually correct?**
  _`AtomicTaskEngine` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `AtomicTask` (e.g. with `SupervisorControl` and `SupervisorControlError`) actually correct?**
  _`AtomicTask` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `AgentManager` (e.g. with `_FakeOllamaClient` and `_FakeOllamaResponse`) actually correct?**
  _`AgentManager` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `TaskEngineError` (e.g. with `SupervisorControl` and `SupervisorControlError`) actually correct?**
  _`TaskEngineError` has 2 INFERRED edges - model-reasoned connections that need verification._