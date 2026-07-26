import requests

from app.config import settings
from app.logger import logger
from app.models import AIResponse


class OllamaClient:
    def __init__(self):
        self.url = settings.OLLAMA_URL
        self.model = settings.MODEL

    def generate(self, prompt: str, model: str = None, system: str = None) -> AIResponse:
        """
        model: overrides the configured default for this call — used by
        router.choose_model to route simple prompts to a lighter model.
        system: optional system/role context, sent as Ollama's separate
        `system` field rather than concatenated into the prompt.
        """
        payload = {
            "model": model or self.model,
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
                model=data.get("model", model or self.model),
                response=data.get("response", ""),
                thinking=data.get("thinking"),
                done=data.get("done", False),
            )
        except Exception as error:
            logger.error(f"Ollama request failed: {error}")
            raise