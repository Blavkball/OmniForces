from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import json
import os

from app.skills.skill_loader import SkillDefinition, SkillRegistry


@dataclass
class GraphifySkill:
    """
    GraphifySkill provides read-only access to Graphify's architectural graph.

    This class includes adapter methods expected by tests:
    - get_graph_summary()
    - get_node_dependencies(name)
    - query_graph(query)
    """
    registry: Optional[SkillRegistry] = None
    graph_path: str = "graphify/graph.json"
    graph: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        # Register skill in provided registry (if any) using the registry-friendly API.
        if self.registry is not None:
            definition = get_graphify_skill_definition()
            # prefer entry_point so consumers can create instances if desired
            self.registry.register_skill(definition)

        # attempt to load graph if present
        self.load_graph()

    # -----------------------------
    # Graph loading
    # -----------------------------
    def load_graph(self) -> None:
        if not os.path.exists(self.graph_path):
            self.graph = None
            return

        with open(self.graph_path, "r", encoding="utf-8") as f:
            self.graph = json.load(f)

    # -----------------------------
    # Public skill execution entry
    # -----------------------------
    def execute(self, action: str, **kwargs: Any) -> Any:
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
    # Adapter methods (tests expect these)
    # -----------------------------
    def get_graph_summary(self) -> Dict[str, Any]:
        """
        Returns a small summary dict:
          { "total_nodes": int, "total_edges": int, "available": bool }
        """
        if self.graph is None:
            self.load_graph()
        if not self.graph:
            return {"total_nodes": 0, "total_edges": 0, "available": False}
        nodes = self.graph.get("nodes", {})
        # nodes may be list or dict depending on generator; handle both
        total_nodes = len(nodes) if isinstance(nodes, dict) else len(nodes)
        edges = self.graph.get("links") or self.graph.get("edges") or []
        total_edges = len(edges)
        return {"total_nodes": total_nodes, "total_edges": total_edges, "available": True}

    def get_node_dependencies(self, name: str) -> List[str]:
        """
        Return a list of node ids that the named node depends on (targets).
        """
        if self.graph is None:
            self.load_graph()
        if not self.graph:
            return []
        edges = self.graph.get("links") or self.graph.get("edges") or []
        deps = [link.get("target") for link in edges if link.get("source") == name]
        return deps

    def query_graph(self, query: str) -> List[Dict[str, Any]]:
        """
        Return list of node dicts containing query in name/id.
        Normalize nodes into dicts with at least 'id' and 'name' when possible.
        """
        if self.graph is None:
            self.load_graph()
        if not self.graph:
            return []
        nodes = self.graph.get("nodes", {})
        results = []
        if isinstance(nodes, dict):
            iterable = nodes.items()
            for node_id, node in iterable:
                name = node.get("name") if isinstance(node, dict) else str(node)
                if query.lower() in str(node_id).lower() or (name and query.lower() in name.lower()):
                    results.append({"id": node_id, "name": name})
        else:
            # nodes is a list of dicts
            for node in nodes:
                node_id = node.get("id") or node.get("name")
                name = node.get("name") or node_id
                if node_id and query.lower() in str(node_id).lower() or (name and query.lower() in name.lower()):
                    results.append({"id": node_id, "name": name})
        return results

    # -----------------------------
    # Lower level ops reused by execute()
    # -----------------------------
    def get_node(self, name: str) -> Optional[Dict[str, Any]]:
        if not name or not self.graph:
            return None
        nodes = self.graph.get("nodes", {})
        if isinstance(nodes, dict):
            return nodes.get(name)
        for n in nodes:
            if n.get("id") == name or n.get("name") == name:
                return n
        return None

    def get_edges(self, name: str) -> List[Dict[str, Any]]:
        if not name or not self.graph:
            return []
        edges = self.graph.get("links") or self.graph.get("edges") or []
        return [e for e in edges if e.get("source") == name or e.get("target") == name]

    def search_nodes(self, query: str) -> List[str]:
        if not query or not self.graph:
            return []
        nodes = self.graph.get("nodes", {})
        results = []
        if isinstance(nodes, dict):
            for nid, n in nodes.items():
                name = n.get("name") if isinstance(n, dict) else str(n)
                if query.lower() in nid.lower() or (name and query.lower() in name.lower()):
                    results.append(nid)
        else:
            for n in nodes:
                nid = n.get("id") or n.get("name")
                if nid and query.lower() in str(nid).lower():
                    results.append(nid)
        return results

    def dependencies(self, name: str) -> Dict[str, Any]:
        return {"node": name, "edges": self.get_edges(name), "exists": self.get_node(name) is not None}


def get_graphify_skill_definition() -> SkillDefinition:
    """
    Factory to return a SkillDefinition for tests and registry registration.
    Test expects:
      - name == 'graphify_skill'
      - 'graphify:read' in permissions
    """
    return SkillDefinition(
        name="graphify_skill",
        description="Provides read access to Graphify architectural graph.",
        permissions=["graphify:read"],
        metadata={"version": "1.0"},
        # prefer entry_point so callers can instantiate if desired
        entry_point=GraphifySkill,
    )