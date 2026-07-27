"""
OmniForces
Model Router

Purpose:
Centralised model selection for AI Employees.

Responsibilities:
- Select the appropriate model for an AI Employee.
- Hide model selection from OllamaClient.
- Provide a single routing interface.

The router does not communicate with Ollama.
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