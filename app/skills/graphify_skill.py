from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import json
import os

from app.skills.skill_loader import SkillDefinition, SkillRegistry


@dataclass
class GraphifySkill:
    """
    GraphifySkill provides read-only access to Graphify's architectural graph.

    Capabilities:
    - Load Graphify JSON
    - Query nodes
    - Query edges
    - Search components
    - Inspect dependencies
    """

    registry: SkillRegistry
    graph_path: str = "graphify/graph.json"
    graph: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """
        Register this skill with the SkillRegistry.
        """
        definition = SkillDefinition(
            name="graphify",
            description="Provides read-only access to Graphify architectural graph.",
            permissions=["read"],
            metadata={"version": "1.0"},
            execute=self.execute
        )
        self.registry.register_skill(definition)

        # Load graph immediately if available
        self.load_graph()

    # -----------------------------
    # Graph loading
    # -----------------------------
    def load_graph(self) -> None:
        """
        Load Graphify JSON from disk.
        """
        if not os.path.exists(self.graph_path):
            self.graph = None
            return

        with open(self.graph_path, "r", encoding="utf-8") as f:
            self.graph = json.load(f)

    # -----------------------------
    # Public skill execution entry
    # -----------------------------
    def execute(self, action: str, **kwargs: Any) -> Any:
        """
        Execute a Graphify action.

        Supported actions:
        - get_node(name)
        - get_edges(name)
        - search_nodes(query)
        - dependencies(name)
        """
        if self.graph is None:
            self.load_graph()

        if action == "get_node":
            return self.get_node(kwargs.get("name"))

        if action == "get_edges":
            return self.get_edges(kwargs.get("name"))

        if action == "search_nodes":
            return self.search_nodes(kwargs.get("query"))

        if action == "dependencies":
            return self.dependencies(kwargs.get("name"))

        raise ValueError(f"Unknown Graphify action: {action}")

    # -----------------------------
    # Graph operations
    # -----------------------------
    def get_node(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Return a node by name.
        """
        if not name or "nodes" not in self.graph:
            return None

        return self.graph["nodes"].get(name)

    def get_edges(self, name: str) -> List[Dict[str, Any]]:
        """
        Return edges for a given node.
        """
        if not name or "edges" not in self.graph:
            return []

        return [
            edge for edge in self.graph["edges"]
            if edge.get("source") == name or edge.get("target") == name
        ]

    def search_nodes(self, query: str) -> List[str]:
        """
        Search for nodes containing the query string.
        """
        if not query or "nodes" not in self.graph:
            return []

        query_lower = query.lower()
        return [
            name for name in self.graph["nodes"].keys()
            if query_lower in name.lower()
        ]

    def dependencies(self, name: str) -> Dict[str, Any]:
        """
        Return dependency information for a node.
        """
        return {
            "node": name,
            "edges": self.get_edges(name),
            "exists": self.get_node(name) is not None,
        }
