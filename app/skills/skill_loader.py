# ============================================
# OmniForces
# Skill Loader Foundation
# ============================================


class SkillLoader:
    """
    Loads skills for AI agents when required.
    """

    def __init__(self):
        self.available_skills = {}

    def register_skill(self, name, description):
        self.available_skills[name] = description

    def load_skill(self, name):
        return self.available_skills.get(name)

    def list_skills(self):
        return self.available_skills