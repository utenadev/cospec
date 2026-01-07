"""Interface definitions for external dependencies to reduce coupling."""

import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional


class CLIInterface(ABC):
    """Interface for CLI framework abstraction."""

    @abstractmethod
    def command(self, name: Optional[str] = None, **kwargs) -> callable:  # type: ignore
        """Decorator for defining CLI commands."""
        pass

    @abstractmethod
    def run(self) -> None:
        """Run the CLI application."""
        pass


class ConsoleInterface(ABC):
    """Interface for console output abstraction."""

    @abstractmethod
    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to console with formatting."""
        pass

    @abstractmethod
    def error(self, *args: Any, **kwargs: Any) -> None:
        """Print error message to console."""
        pass


class FilesystemInterface(ABC):
    """Interface for filesystem operations."""

    @abstractmethod
    def read_text(self, path: Path, encoding: str = "utf-8") -> str:
        """Read text from file."""
        pass

    @abstractmethod
    def write_text(self, path: Path, content: str, encoding: str = "utf-8") -> None:
        """Write text to file."""
        pass

    @abstractmethod
    def exists(self, path: Path) -> bool:
        """Check if path exists."""
        pass

    @abstractmethod
    def glob(self, path: Path, pattern: str) -> List[Path]:
        """Glob files matching pattern."""
        pass


class ProcessInterface(ABC):
    """Interface for external process execution."""

    @abstractmethod
    def run(self, command: List[str], cwd: Optional[str] = None, **kwargs: Any) -> subprocess.CompletedProcess:
        """Run external command."""
        pass


class ConfigInterface(ABC):
    """Interface for configuration management."""

    @abstractmethod
    def load_from_file(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file."""
        pass

    @abstractmethod
    def save_to_file(self, config_path: Optional[str] = None) -> None:
        """Save configuration to file."""
        pass
