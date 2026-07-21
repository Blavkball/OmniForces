"""
OmniForces Logger

Provides a shared logger for all application modules.
"""

import logging
from pathlib import Path

# Ensure the logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "omniforces.log"

# Create shared logger
logger = logging.getLogger("OmniForces")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers if imported multiple times
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File output
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)