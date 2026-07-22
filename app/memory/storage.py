# ============================================
# OmniForces
# Memory Storage
# ============================================

import json
from pathlib import Path


class MemoryStorage:
    """
    Handles saving and loading memory files.
    """

    def __init__(self, base_path="memory"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, filename: str, data: dict):
        filepath = self.base_path / filename

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self, filename: str) -> dict:
        filepath = self.base_path / filename

        if not filepath.exists():
            return {}

        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)

    def exists(self, filename: str) -> bool:
        return (self.base_path / filename).exists()

    def delete(self, filename: str):
        filepath = self.base_path / filename

        if filepath.exists():
            filepath.unlink()