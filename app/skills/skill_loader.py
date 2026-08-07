from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class SkillDefinition:
    """
    Core definition for a skill in the OmniForces ecosystem.

    A skill is a named capability with metadata, permissions,
    and an optional execution entry point.
    """

    name: str
    description: str
    enabled: bool = True
    permissions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    execute: Optional[Callable[..., Any]] = None

    def validate(self) -> None:
        """Validate that the skill definition is structurally sound."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Skill name must be a non-empty string")

        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("Skill description must be a non-empty string")

    def is_enabled(self) -> bool:
        """Check whether the skill is enabled."""
        return self.enabled


@dataclass
class SkillRegistry:
    """
    Registry for all skills known to the AgentManager and wider system.

    Responsibilities:
    - Register skills
    - Store and retrieve skill metadata
    - Enable/disable skills
    - Validate required skills for a task
    - Provide an execution entry point for registered skills
    """

    _skills: Dict[str, SkillDefinition] = field(default_factory=dict)

    def register_skill(self, skill: SkillDefinition) -> None:
        """Register a fully defined skill."""
        skill.validate()
        self._skills[skill.name] = skill

    def register_simple_skill(self, name: str, description: str) -> None:
        """
        Backwards-compatible helper that mirrors the old SkillLoader API.
        Creates a minimal SkillDefinition and registers it.
        """
        skill = SkillDefinition(name=name, description=description)
        self.register_skill(skill)

    def get_skill(self, name: str) -> Optional[SkillDefinition]:
        """Retrieve a skill definition by name."""
        return self._skills.get(name)

    def list_skills(self) -> List[SkillDefinition]:
        """Return all registered skills."""
        return list(self._skills.values())

    def enable_skill(self, name: str) -> None:
        """Enable a previously registered skill."""
        skill = self._skills.get(name)
        if skill is None:
            raise KeyError(f"Skill '{name}' is not registered")
        skill.enabled = True

    def disable_skill(self, name: str) -> None:
        """Disable a previously registered skill."""
        skill = self._skills.get(name)
        if skill is None:
            raise KeyError(f"Skill '{name}' is not registered")
        skill.enabled = False

    def validate_required_skills(self, required_skill_names: List[str]) -> None:
        """
        Validate that all required skills for a task are present and enabled.
        Raises ValueError if any required skills are missing or disabled.
        """
        missing = []
        disabled = []

        for name in required_skill_names:
            skill = self._skills.get(name)
            if skill is None:
                missing.append(name)
            elif not skill.enabled:
                disabled.append(name)

        if missing or disabled:
            parts = []
            if missing:
                parts.append(f"Missing skills: {', '.join(missing)}")
            if disabled:
                parts.append(f"Disabled skills: {', '.join(disabled)}")
            raise ValueError("; ".join(parts))

    def execute_skill(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Execute a registered skill by name.
        This is the generic execution entry point for the registry.
        """
        skill = self._skills.get(name)
        if skill is None:
            raise KeyError(f"Skill '{name}' is not registered")

        if not skill.enabled:
            raise RuntimeError(f"Skill '{name}' is disabled")

        if skill.execute is None:
            raise RuntimeError(f"Skill '{name}' has no execution entry point")

        return skill.execute(*args, **kwargs)
