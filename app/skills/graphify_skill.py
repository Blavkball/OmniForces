import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.skills.skill_loader import SkillDefinition


class GraphifySkill:
    """
    Skill providing architectural awareness by reading Graphify outputs.
    """

    def __init__(self, graph_path: Optional[str] = None):
        if graph_path:
            self.graph_file = Path(graph_path)
        else:
            self.graph_file = Path.cwd() / "graphify-out" / "graph.json"

    def _load_graph(self) -> Dict[str, Any]:
        if not self.graph_file.exists():
            return {}
        try:
            return json.loads(self.graph_file.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def get_graph_summary(self) -> Dict[str, Any]:
        """
        Returns basic summary statistics of the architectural graph.
        """
        data = self._load_graph()
        nodes = data.get("nodes", [])
        edges = data.get("links", data.get("edges", []))
        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "available": bool(data)
        }

    def get_node_dependencies(self, node_name: str) -> List[str]:
        """
        Retrieves names of connected target nodes/dependencies for a specified node.
        """
        data = self._load_graph()
        edges = data.get("links", data.get("edges", []))
        dependencies = []
        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")
            if source == node_name and target:
                dependencies.append(str(target))
        return sorted(list(set(dependencies)))

    def query_graph(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches nodes matching the query string by ID, label, or name.
        """
        data = self._load_graph()
        nodes = data.get("nodes", [])
        results = []
        query_lower = query.lower()
        for node in nodes:
            node_id = str(node.get("id", ""))
            node_name = str(node.get("name", node.get("label", "")))
            if query_lower in node_id.lower() or query_lower in node_name.lower():
                results.append(node)
        return results


def get_graphify_skill_definition() -> SkillDefinition:
    """
    Factory function returning the SkillDefinition for GraphifySkill.
    """
    return SkillDefinition(
        name="graphify_skill",
        description="Provides architectural awareness by querying Graphify dependencies, call graphs, and component relationships.",
        entry_point=GraphifySkill,
        permissions=["graphify:read"],
        metadata={"version": "1.0"}
    )