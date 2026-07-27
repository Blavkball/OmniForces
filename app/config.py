"""
OmniForces Configuration

Loads application configuration from the environment.
All modules should import settings from this file.
"""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application configuration."""

    # Application
    APP_NAME = "OmniForces"
    VERSION = "0.2.0"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # API
    API_KEY = os.getenv("OMNIFORCES_API_KEY", "")

    # Ollama
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

    # DEFAULT_MODEL is the primary key. MODEL is retained for backwards
    # compatibility and used as a fallback source if DEFAULT_MODEL is
    # not set directly — covers .env files still using the older key.
    DEFAULT_MODEL = os.getenv(
        "DEFAULT_MODEL",
        os.getenv("MODEL", "llama3.2:latest"),
    )
    LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama3.2:latest")
    CODING_MODEL = os.getenv("CODING_MODEL", "qwen3.6:latest")
    ARCHITECTURE_MODEL = os.getenv(
        "ARCHITECTURE_MODEL",
        "deepseek-r1:latest",
    )

    # Backwards compatibility
    MODEL = os.getenv("MODEL", "deepseek-r1:latest")


settings = Settings()