"""
OmniForces
Graphify Context Reader

Reads Graphify output and exposes repository knowledge
to OmniForces components.

Source:
E:/OmniForces/graphify-out
"""

import json
from pathlib import Path


class GraphifyContextError(Exception):
    """Raised when Graphify context cannot be loaded."""
    pass


class GraphifyContext:
    """
    Provides access to Graphify generated knowledge.

    Reads:
    - graph.json
    - manifest.json
    - GRAPH_REPORT.md

    Provides:
    - repository graph access
    - node lookup
    - relationship lookup
    """

    def __init__(self, graphify_path: str = "graphify-out"):
        self.path = Path(graphify_path)

    def _load_json(self, filename: str):
        file_path = self.path / filename

        if not file_path.exists():
            raise GraphifyContextError(
                f"Missing Graphify file: {file_path}"
            )

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _get_nodes(self):
        graph = self.get_graph()
        return graph.get("nodes", [])

    def _get_links(self):
        graph = self.get_graph()
        return graph.get("links", [])

    def get_graph(self):
        """Return complete Graphify graph."""
        return self._load_json("graph.json")

    def get_manifest(self):
        """Return Graphify repository manifest."""
        return self._load_json("manifest.json")

    def get_report(self):
        """Return Graphify markdown report."""
        file_path = self.path / "GRAPH_REPORT.md"

        if not file_path.exists():
            raise GraphifyContextError(
                f"Missing Graphify report: {file_path}"
            )

        return file_path.read_text(encoding="utf-8")

    def find_nodes(self, label: str):
        """
        Find nodes matching an exact Graphify label.
        """

        return [
            node
            for node in self._get_nodes()
            if node.get("label") == label
        ]

    def find_related(self, label: str):
        """
        Find Graphify relationships connected to a node.
        """

        nodes = self.find_nodes(label)

        if not nodes:
            return []

        node_ids = {
            node.get("id")
            for node in nodes
        }

        return [
            link
            for link in self._get_links()
            if (
                link.get("source") in node_ids
                or link.get("target") in node_ids
            )
        ]