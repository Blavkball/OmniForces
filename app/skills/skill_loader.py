from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any


@dataclass
class SkillDefinition:
    """
    Defines a skill capability, its execution entry point, metadata, and permissions.
    """
    name: str
    description: str
    entry_point: Optional[Callable[..., Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    enabled: bool = True

    def validate(self) -> bool:
        """
        Validates that the skill definition has required fields.
        """
        if not self.name or not isinstance(self.name, str):
            return False
        if not self.description or not isinstance(self.description, str):
            return False
        return True


class SkillRegistry:
    """
    Registry for managing, retrieving, and validating agent skills.
    """

    def __init__(self):
        self._skills: Dict[str, SkillDefinition] = {}

    def register_skill(self, skill: SkillDefinition) -> None:
        """
        Registers a SkillDefinition into the registry.
        """
        if not isinstance(skill, SkillDefinition):
            raise TypeError("Must register a valid SkillDefinition instance.")
        if not skill.validate():
            raise ValueError(f"Invalid SkillDefinition provided for '{skill.name}'.")
        
        self._skills[skill.name] = skill

    def get_skill(self, name: str) -> Optional[SkillDefinition]:
        """
        Retrieves a skill by name.
        """
        return self._skills.get(name)

    def list_skills(self, enabled_only: bool = True) -> Dict[str, SkillDefinition]:
        """
        Lists all registered skills, optionally filtering by enabled status.
        """
        if enabled_only:
            return {k: v for k, v in self._skills.items() if v.enabled}
        return dict(self._skills)

    def enable_skill(self, name: str) -> bool:
        """
        Enables a skill by name.
        """
        skill = self._skills.get(name)
        if skill:
            skill.enabled = True
            return True
        return False

    def disable_skill(self, name: str) -> bool:
        """
        Disables a skill by name.
        """
        skill = self._skills.get(name)
        if skill:
            skill.enabled = False
            return True
        return False

    def validate_skill(self, name: str) -> bool:
        """
        Validates whether a registered skill is valid and enabled.
        """
        skill = self._skills.get(name)
        if not skill:
            return False
        return skill.enabled and skill.validate()


class SkillLoader(SkillRegistry):
    """
    Legacy compatibility wrapper bridging SkillLoader to SkillRegistry.
    """

    @property
    def available_skills(self) -> Dict[str, str]:
        return {k: v.description for k, v in self._skills.items()}

    def register_skill(self, name_or_skill: Any, description: Optional[str] = None) -> None:
        if isinstance(name_or_skill, SkillDefinition):
            super().register_skill(name_or_skill)
        elif isinstance(name_or_skill, str) and description is not None:
            skill = SkillDefinition(name=name_or_skill, description=description)
            super().register_skill(skill)
        else:
            raise TypeError("Invalid arguments for register_skill.")

    def load_skill(self, name: str) -> Optional[str]:
        skill = self.get_skill(name)
        return skill.description if skill else None

    def list_skills(self, enabled_only: bool = True) -> Dict[str, Any]:
        """
        Overridden to support legacy dictionary return structure {name: description}.
        """
        return {k: v.description for k, v in self._skills.items() if not enabled_only or v.enabled}