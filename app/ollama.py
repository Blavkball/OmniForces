import requests

from app.config import settings
from app.logger import logger
from app.models import AIResponse


class OllamaClient:
    """
    Provider interface for Ollama.

    Responsibilities:
    - Connect to Ollama.
    - Send prompts.
    - Return AIResponse.

    Model selection is handled by ModelRouter.
    """

    def __init__(self):
        self.url = settings.OLLAMA_URL
        self.default_model = settings.DEFAULT_MODEL

    def generate(
        self,
        prompt: str,
        model: str = None,
        system: str = None,
    ) -> AIResponse:
        """
        Generate a response using the supplied model.

        If no model is supplied, the configured default model is used.
        """

        selected_model = model or self.default_model

        payload = {
            "model": selected_model,
            "prompt": prompt,
            "stream": False,
        }

        if system:
            payload["system"] = system

        try:
            response = requests.post(
                self.url,
                json=payload,
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

            logger.info("Ollama request completed successfully.")

            return AIResponse(
                model=data.get("model", selected_model),
                response=data.get("response", ""),
                thinking=data.get("thinking"),
                done=data.get("done", False),
            )

        except Exception as error:
            logger.error(f"Ollama request failed: {error}")
            raise