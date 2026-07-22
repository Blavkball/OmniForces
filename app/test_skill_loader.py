# ============================================
# OmniForces
# Skill Loader Test
# ============================================

from skills.skill_loader import SkillLoader


loader = SkillLoader()

loader.register_skill(
    "coding",
    "Software development capability"
)

loader.register_skill(
    "documentation",
    "Documentation maintenance capability"
)


print(loader.list_skills())

print(loader.load_skill("coding"))

print("Skill loader test complete")