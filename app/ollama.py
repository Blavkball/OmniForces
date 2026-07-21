import requests

from app.config import settings
from app.logger import logger
from app.models import AIResponse


class OllamaClient:

    def __init__(self):
        self.url = settings.OLLAMA_URL
        self.model = settings.MODEL

    def generate(self, prompt: str) -> AIResponse:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

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
                model=data.get("model", self.model),
                response=data.get("response", ""),
                thinking=data.get("thinking"),
                done=data.get("done", False),
            )

        except Exception as error:
            logger.error(f"Ollama request failed: {error}")
            raise