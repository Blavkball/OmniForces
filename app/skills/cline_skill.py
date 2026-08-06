from typing import Any, Dict, List, Optional

from app.skills.skill_loader import SkillDefinition


class ClineSkill:
    """
    Simple AI workforce orchestration skill.
    """

    def __init__(self, agent_manager: Optional[Any] = None):
        self.agent_manager = agent_manager

    def orchestrate_task(self, task_description: str, team: List[str]) -> str:
        """
        Returns a high-level orchestration plan for a task and team.
        """
        team_list = ", ".join(team) if team else "no assigned agents"
        return (
            f"Orchestrating task: {task_description}. "
            f"Team: {team_list}. "
            "Ensure each agent has a clear role and knowledge handoff."
        )

    def summarize_agents(self, agent_profiles: List[Dict[str, Any]]) -> str:
        """
        Summarize the current AI employee team for coordination.
        """
        summary = []
        for profile in agent_profiles:
            name = profile.get("name", "unknown")
            role = profile.get("role", "unspecified")
            skills = profile.get("skills", [])
            summary.append(f"{name} ({role}) with skills {skills}")
        return " | ".join(summary)


def get_cline_skill_definition() -> SkillDefinition:
    """
    Factory function returning the SkillDefinition for Cline orchestration.
    """
    return SkillDefinition(
        name="cline_orchestration",
        description="Orchestrates AI workforce activity, task handoff, and continuity across roles.",
        entry_point=ClineSkill,
        permissions=["ai:orchestrate"],
        metadata={"version": "1.0", "role": "Cline"},
    )
