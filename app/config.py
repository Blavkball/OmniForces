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

    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

    MODEL = os.getenv("MODEL", "deepseek-r1:7b")

    API_KEY = os.getenv("OMNIFORCES_API_KEY", "")

    APP_NAME = "OmniForces"

    VERSION = "0.2.0"

    DEBUG = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()