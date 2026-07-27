import time

import requests

from app.config import settings
from app.logger import logger
from app.models import AIResponse


# Retry tuning - read from settings if defined there, otherwise use these
# defaults. Not requiring config.py changes to function.
_MAX_RETRIES = getattr(settings, "OLLAMA_MAX_RETRIES", 3)
_BACKOFF_BASE_SECONDS = getattr(settings, "OLLAMA_BACKOFF_BASE_SECONDS", 2)
_REQUEST_TIMEOUT = getattr(settings, "OLLAMA_TIMEOUT_SECONDS", 120)

# Errors considered transient - worth retrying. Anything else (HTTP 4xx,
# malformed payload, etc.) is treated as permanent and fails immediately.
_TRANSIENT_ERRORS = (
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
)


class OllamaClient:
    """
    Provider interface for Ollama.

    Responsibilities:
    - Connect to Ollama.
    - Send prompts.
    - Return AIResponse.
    - Retry transient failures (connection refused, timeout) with
      exponential backoff before giving up. Permanent failures
      (bad request, model not found, malformed response) are not
      retried - they fail on the first attempt.

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
        Retries transient failures up to _MAX_RETRIES times with
        exponential backoff (_BACKOFF_BASE_SECONDS * 2^attempt).
        Raises immediately on non-transient failures.
        """

        selected_model = model or self.default_model

        payload = {
            "model": selected_model,
            "prompt": prompt,
            "stream": False,
        }

        if system:
            payload["system"] = system

        last_error = None

        for attempt in range(_MAX_RETRIES + 1):
            try:
                response = requests.post(
                    self.url,
                    json=payload,
                    timeout=_REQUEST_TIMEOUT,
                )

                response.raise_for_status()

                data = response.json()

                logger.info(
                    f"Ollama request completed successfully "
                    f"(attempt {attempt + 1}/{_MAX_RETRIES + 1})."
                )

                return AIResponse(
                    model=data.get("model", selected_model),
                    response=data.get("response", ""),
                    thinking=data.get("thinking"),
                    done=data.get("done", False),
                )

            except _TRANSIENT_ERRORS as error:
                last_error = error
                if attempt < _MAX_RETRIES:
                    wait = _BACKOFF_BASE_SECONDS * (2 ** attempt)
                    logger.warning(
                        f"Ollama request failed (transient, attempt "
                        f"{attempt + 1}/{_MAX_RETRIES + 1}): {error}. "
                        f"Retrying in {wait}s."
                    )
                    time.sleep(wait)
                else:
                    logger.error(
                        f"Ollama request failed after {_MAX_RETRIES + 1} "
                        f"attempts: {error}"
                    )
                    raise

            except Exception as error:
                logger.error(f"Ollama request failed (non-retryable): {error}")
                raise

        raise last_error