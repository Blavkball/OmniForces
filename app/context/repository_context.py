"""
OmniForces
Repository Context Provider

Provides access to connected KingC Software repositories.

Responsibilities:
- Locate repositories
- Read repository knowledge
- Connect Graphify context
- Provide a unified knowledge interface

Repositories remain independent.
This layer only connects them.
"""

from pathlib import Path


class RepositoryContextError(Exception):
    """Raised when repository context cannot be loaded."""
    pass


class RepositoryContext:
    """
    Provides repository awareness for OmniForces.
    """

    DEFAULT_REPOSITORIES = {
        "AI_Knowledge": Path("E:/AI_Knowledge"),
        "AI_Workstation": Path("E:/AI_Workstation"),
        "OmniForces": Path("E:/OmniForces"),
        "BlackBall": Path("E:/Pool-League-Manager"),
    }

    def __init__(self, repositories=None):
        self.repositories = (
            repositories
            if repositories
            else self.DEFAULT_REPOSITORIES
        )

    def get_repositories(self):
        """
        Return registered repositories.
        """
        return self.repositories

    def get_repository(self, name: str):
        """
        Return a specific repository path.
        """
        repository = self.repositories.get(name)

        if repository is None:
            raise RepositoryContextError(
                f"Unknown repository: {name}"
            )

        return repository

    def exists(self, name: str) -> bool:
        """
        Check repository availability.
        """
        return self.get_repository(name).exists()

    def list_available(self):
        """
        Return repositories currently available.
        """
        return {
            name: path
            for name, path in self.repositories.items()
            if path.exists()
        }