"""
OmniForces
Model Router

Purpose:
Centralised model selection for AI Employees.

Responsibilities:
- Select the appropriate model.
- Hide model selection from OllamaClient.
- Provide a stable routing interface.

The router never communicates with Ollama.
It only returns the model to use.
"""

from typing import Optional

from app.config import settings


class ModelRouter:
    """
    Routes AI Employees to the appropriate local model.
    """

    ROLE_MODEL_MAP = {
        "Senior Technical Lead": settings.ARCHITECTURE_MODEL,
        "Software Architect": settings.ARCHITECTURE_MODEL,
        "Senior Software Engineer": settings.CODING_MODEL,
        "QA Engineer": settings.CODING_MODEL,
        "Documentation Engineer": settings.LLAMA_MODEL,
        "Knowledge Engineer": settings.LLAMA_MODEL,
        "Cline": settings.LLAMA_MODEL,
        "Research Engineer": settings.ARCHITECTURE_MODEL,
    }

    def get_model(self, role: str) -> str:
        """
        Return the preferred model for an AI Employee.
        Unknown roles fall back to the default model.
        """
        return self.ROLE_MODEL_MAP.get(
            role,
            settings.DEFAULT_MODEL,
        )

    def route(
        self,
        role: str = None,
        prompt: str = None,
    ) -> str:
        """
        Stable routing interface.

        Version 1:
        - Routes by AI Employee role.
        - Prompt is accepted for future routing logic but is
          intentionally unused in this version.

        Future versions may consider:
        - task type
        - prompt complexity
        - model availability
        - permissions
        """
        return self.get_model(role or "")


# Backwards-compatible module-level function. AgentManager.execute_task()
# previously called this with prompt only, no role — AtomicTask now carries
# a role field (added to atomic_task_engine.py, commit 3ea67bb). This shim
# now passes role through to ModelRouter.route(), giving real role-based
# routing. Still safe for any caller that only passes prompt: role defaults
# to None and falls through to the default-model path exactly as before.
_default_router = ModelRouter()


def choose_model(role: Optional[str] = None, prompt: Optional[str] = None) -> str:
    return _default_router.route(role=role, prompt=prompt)