"""Concrete implementations of external dependency interfaces."""

import subprocess
from pathlib import Path
from typing import Any, List, Optional

import typer
from rich.console import Console

from cospec.core.interfaces import ConsoleInterface, FilesystemInterface, ProcessInterface


class TyperCLI(typer.Typer):
    """Concrete implementation using typer for CLI operations."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def run(self) -> None:
        """Run the CLI application."""
        self()


class RichConsole(ConsoleInterface):
    """Concrete implementation using rich for console operations."""

    def __init__(self) -> None:
        self.console = Console()

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to console with formatting."""
        self.console.print(*args, **kwargs)

    def error(self, *args: Any, **kwargs: Any) -> None:
        """Print error message to console."""
        self.console.print(*args, style="red", **kwargs)


class StandardFilesystem(FilesystemInterface):
    """Concrete implementation for standard filesystem operations."""

    def read_text(self, path: Path, encoding: str = "utf-8") -> str:
        """Read text from file."""
        return path.read_text(encoding=encoding)

    def write_text(self, path: Path, content: str, encoding: str = "utf-8") -> None:
        """Write text to file."""
        path.write_text(content, encoding=encoding)

    def exists(self, path: Path) -> bool:
        """Check if path exists."""
        return path.exists()

    def glob(self, path: Path, pattern: str) -> List[Path]:
        """Glob files matching pattern."""
        return list(path.glob(pattern))


class SubprocessManager(ProcessInterface):
    """Concrete implementation using subprocess for external process execution."""

    def run(self, command: List[str], cwd: Optional[str] = None, **kwargs: Any) -> subprocess.CompletedProcess:
        """Run external command."""
        try:
            return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True, **kwargs)
        except subprocess.CalledProcessError as e:
            from cospec.core.exceptions import ToolExecutionError

            raise ToolExecutionError(f"Command failed: {' '.join(command)}", e) from e
