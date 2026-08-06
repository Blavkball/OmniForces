"""
OmniForces
Obsidian Context Provider

Reads the human knowledge vault (Obsidian).

Source:
obsidian-vault

Responsibilities:
- List available notes
- Read individual notes
- Provide human knowledge to Knowledge Provider

Vault structure:
Flat — all notes sit directly in the vault root.
No subfolders in use.
"""

from pathlib import Path

from app.config import settings


class ObsidianContextError(Exception):
    """Raised when Obsidian vault cannot be loaded."""
    pass


class ObsidianContext:
    """
    Provides access to the Obsidian vault.
    """

    def __init__(self, path=None):
        if path:
            self.path = Path(path)
        elif getattr(settings, "OBSIDIAN_VAULT_PATH", None):
            self.path = Path(settings.OBSIDIAN_VAULT_PATH)
        else:
            self.path = Path("obsidian-vault")

    def exists(self):
        """
        Check vault availability.
        """
        return self.path.exists()

    def list_notes(self):
        """
        Return all markdown note filenames in the vault.
        """

        if not self.exists():
            raise ObsidianContextError(
                f"Missing Obsidian vault: {self.path}"
            )

        return [
            item.name
            for item in self.path.glob("*.md")
        ]

    def read_note(self, filename):
        """
        Read a single note from the vault root.
        """

        file_path = self.path / filename

        if not file_path.exists():
            raise ObsidianContextError(
                f"Missing note: {file_path}"
            )

        return file_path.read_text(
            encoding="utf-8"
        )

    def get_all_notes(self):
        """
        Read every note in the vault.

        Returns a dict of filename -> content.
        """

        notes = {}

        for filename in self.list_notes():
            notes[filename] = self.read_note(filename)

        return notes