import pytest
from pathlib import Path
from app.skills.repository_skill import RepositorySkill, get_repository_skill_definition
from app.skills.skill_loader import SkillRegistry


def test_repository_skill_definition():
    skill_def = get_repository_skill_definition()
    assert skill_def.name == "repository_skill"
    assert "repo:read" in skill_def.permissions

    registry = SkillRegistry()
    registry.register_skill(skill_def)
    assert registry.get_skill("repository_skill") == skill_def


def test_read_file(tmp_path):
    test_file = tmp_path / "sample.py"
    test_file.write_text("print('hello')", encoding="utf-8")

    repo_skill = RepositorySkill(root_dir=str(tmp_path))
    content = repo_skill.read_file("sample.py")
    assert content == "print('hello')"


def test_path_traversal_prevention(tmp_path):
    repo_skill = RepositorySkill(root_dir=str(tmp_path))
    with pytest.raises(ValueError, match="Access denied"):
        repo_skill.read_file("../outside.txt")


def test_search_code(tmp_path):
    (tmp_path / "a.py").write_text("def target(): pass", encoding="utf-8")
    (tmp_path / "b.py").write_text("x = 10", encoding="utf-8")

    repo_skill = RepositorySkill(root_dir=str(tmp_path))
    results = repo_skill.search_code("target")
    assert len(results) == 1
    assert results[0]["file"] == "a.py"
    assert results[0]["line"] == 1


def test_inspect_structure(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "file.py").write_text("pass", encoding="utf-8")

    repo_skill = RepositorySkill(root_dir=str(tmp_path))
    structure = repo_skill.inspect_structure()
    assert "sub" in structure or "sub/file.py" in str(structure)