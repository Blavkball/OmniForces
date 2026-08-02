# ============================================
# OmniForces
# Skill Loader Tests
# ============================================

from app.skills.skill_loader import SkillLoader


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