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

from app.config import settings


class ModelRouter:
    """
    Routes AI Employees to the appropriate local model.
    """

    ROLE_MODEL_MAP = {
        "Documentation Engineer": settings.LLAMA_MODEL,
        "Senior Software Engineer": settings.CODING_MODEL,
        "Software Architect": settings.ARCHITECTURE_MODEL,
        "Research Engineer": settings.ARCHITECTURE_MODEL,
        "QA Engineer": settings.CODING_MODEL,
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
# currently calls this with prompt only, no role — AtomicTask does not
# yet carry a role field. Role-based routing through ModelRouter.route()
# is the correct long-term path once Phase 3 (AI Employee role context)
# adds that field to the task model. Until then, this returns the
# default-model path via ModelRouter, preserving current behavior.
_default_router = ModelRouter()


def choose_model(prompt: str = None) -> str:
    return _default_router.route(role=None, prompt=prompt)