import json
import pytest
from app.skills.graphify_skill import GraphifySkill, get_graphify_skill_definition
from app.skills.skill_loader import SkillRegistry


def test_graphify_skill_definition():
    skill_def = get_graphify_skill_definition()
    assert skill_def.name == "graphify_skill"
    assert "graphify:read" in skill_def.permissions

    registry = SkillRegistry()
    registry.register_skill(skill_def)
    assert registry.get_skill("graphify_skill") == skill_def


def test_graphify_skill_operations(tmp_path):
    graph_data = {
        "nodes": [
            {"id": "AgentManager", "name": "AgentManager"},
            {"id": "SkillRegistry", "name": "SkillRegistry"}
        ],
        "links": [
            {"source": "AgentManager", "target": "SkillRegistry"}
        ]
    }
    graph_file = tmp_path / "graph.json"
    graph_file.write_text(json.dumps(graph_data), encoding="utf-8")

    skill = GraphifySkill(graph_path=str(graph_file))
    
    summary = skill.get_graph_summary()
    assert summary["total_nodes"] == 2
    assert summary["total_edges"] == 1
    assert summary["available"] is True

    deps = skill.get_node_dependencies("AgentManager")
    assert deps == ["SkillRegistry"]

    results = skill.query_graph("Skill")
    assert len(results) == 1
    assert results[0]["id"] == "SkillRegistry"