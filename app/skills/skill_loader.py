from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class SkillDefinition:
    """
    Core definition for a skill in the OmniForces ecosystem.

    A skill is a named capability with metadata, permissions,
    and an optional execution entry point (entry_point). An
    `execute` field is retained for backwards compatibility.
    """
    name: str
    description: str
    enabled: bool = True
    permissions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    entry_point: Optional[Callable[..., Any]] = None  # factory/class used to create a runnable instance
    execute: Optional[Callable[..., Any]] = None  # backwards-compatible direct callable

    def validate(self) -> None:
        """Validate that the skill definition is structurally sound."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Skill name must be a non-empty string")

        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("Skill description must be a non-empty string")

        if self.entry_point is not None and not callable(self.entry_point):
            raise ValueError("entry_point must be callable if provided")

        if self.execute is not None and not callable(self.execute):
            raise ValueError("execute must be callable if provided")

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

    # Registration
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

    # Query
    def get_skill(self, name: str) -> Optional[SkillDefinition]:
        """Retrieve a skill definition by name."""
        return self._skills.get(name)

    def list_skills(self) -> List[SkillDefinition]:
        """Return all registered skills."""
        return list(self._skills.values())

    # Enable / disable
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

    # Validation helpers used by AgentManager
    def validate_skill(self, name: str) -> bool:
        """
        Return True if the named skill exists and is enabled.
        This mirrors AgentManager's expected boolean check.
        """
        skill = self._skills.get(name)
        return bool(skill and skill.enabled)

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

    # Execution entry point
    def execute_skill(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Execute a registered skill by name.

        Behavior:
        - If the skill exposes an `entry_point`, call it and return the result.
          (Caller may pass agent_manager=self etc.)
        - Else if the skill exposes a direct `execute` callable, call it.
        - Else raise an error.
        """
        skill = self._skills.get(name)
        if skill is None:
            raise KeyError(f"Skill '{name}' is not registered")

        if not skill.enabled:
            raise RuntimeError(f"Skill '{name}' is disabled")

        # Prefer entry_point to match AgentManager expectations
        if skill.entry_point is not None:
            if not callable(skill.entry_point):
                raise RuntimeError(f"Skill '{name}' entry_point is not callable")
            return skill.entry_point(*args, **kwargs)

        if skill.execute is not None:
            if not callable(skill.execute):
                raise RuntimeError(f"Skill '{name}' execute attribute is not callable")
            return skill.execute(*args, **kwargs)

        raise RuntimeError(f"Skill '{name}' has no execution entry point")
