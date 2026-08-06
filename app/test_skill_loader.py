# ============================================
# OmniForces
# Skill Loader Tests
# ============================================

import pytest

from app.skills.skill_loader import SkillDefinition, SkillLoader, SkillRegistry


def test_skill_loader_initialises():

    loader = SkillLoader()

    assert loader.available_skills == {}


def test_register_skill():

    loader = SkillLoader()

    loader.register_skill(
        "coding",
        "Software development capability"
    )

    assert loader.available_skills == {
        "coding": "Software development capability"
    }


def test_register_duplicate_skill_raises():

    loader = SkillLoader()
    loader.register_skill(
        "coding",
        "Software development capability"
    )

    with pytest.raises(ValueError, match="already registered"):
        loader.register_skill(
            "coding",
            "Duplicate capability"
        )


def test_skill_definition_metadata_and_serialization():

    skill = SkillDefinition(
        name="repo_inspect",
        description="Inspect repository structure",
        permissions=["repo:read"],
        metadata={"version": "1.0"}
    )

    assert skill.validate()
    assert skill.serialize()["permissions"] == ["repo:read"]
    assert skill.serialize()["metadata"]["version"] == "1.0"
    assert skill.serialize()["has_entry_point"] is False


def test_instantiate_skill_entry_point():

    def dummy_skill(x, y=1):
        return x + y

    registry = SkillRegistry()
    registry.register_skill(
        SkillDefinition(
            name="adder",
            description="Adds two values",
            entry_point=dummy_skill,
            permissions=["math:execute"]
        )
    )

    result = registry.instantiate_skill("adder", 2, y=3)
    assert result == 5


def test_load_skill():

    loader = SkillLoader()

    loader.register_skill(
        "coding",
        "Software development capability"
    )

    assert (
        loader.load_skill("coding")
        ==
        "Software development capability"
    )


def test_load_unknown_skill():

    loader = SkillLoader()

    assert loader.load_skill("unknown") is None


def test_list_skills():

    loader = SkillLoader()

    loader.register_skill(
        "coding",
        "Software development capability"
    )

    loader.register_skill(
        "documentation",
        "Documentation maintenance capability"
    )

    skills = loader.list_skills()

    assert skills == {
        "coding": "Software development capability",
        "documentation": "Documentation maintenance capability",
    }