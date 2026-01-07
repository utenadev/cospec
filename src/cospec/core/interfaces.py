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


# === Exception Handling and Logging Interfaces ===


class LoggerInterface(ABC):
    """Interface for logging operations."""

    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        pass

    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        pass

    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        pass

    @abstractmethod
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message."""
        pass


class ExceptionHandlerInterface(ABC):
    """Interface for exception handling strategies."""

    @abstractmethod
    def handle(
        self, exception: Exception, context: Optional[Dict[str, Any]] = None, error_code: Optional[str] = None
    ) -> None:
        """Handle an exception with optional context.

        Args:
            exception: The exception to handle
            context: Optional context information
            error_code: Optional error code for categorization
        """
        pass

    @abstractmethod
    def wrap_with_context(
        self, exception: Exception, context: Optional[Dict[str, Any]] = None, error_code: Optional[str] = None
    ) -> Exception:
        """Wrap exception with additional context.

        Args:
            exception: The exception to wrap
            context: Optional context information
            error_code: Optional error code for categorization

        Returns:
            Exception: Wrapped exception with context
        """
        pass


class LLMInterface(ABC):
    """Interface for LLM interactions."""

    @abstractmethod
    def query(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Execute a query against the LLM.

        Args:
            prompt: The prompt to send to the LLM
            context: Optional context information

        Returns:
            LLM response as string
        """
        pass

    @abstractmethod
    def validate_response(self, response: str) -> bool:
        """Validate LLM response format.

        Args:
            response: The LLM response to validate

        Returns:
            True if response is valid, False otherwise
        """
        pass


# === Agent Component Interfaces ===


class AnalyzerInterface(ABC):
    """Interface for project analysis."""

    @abstractmethod
    def analyze_project(self, project_path: Optional[str] = None) -> Dict[str, Any]:
        """Analyze project structure and collect context.

        Args:
            project_path: Optional path to project root

        Returns:
            Dictionary containing project analysis results
        """
        pass

    @abstractmethod
    def get_context_summary(self) -> str:
        """Get human-readable summary of project context.

        Returns:
            Formatted context summary string
        """
        pass


class FormatterInterface(ABC):
    """Interface for output formatting."""

    @abstractmethod
    def format_output(self, data: Any, format_type: Optional[str] = None) -> str:
        """Format output data.

        Args:
            data: Data to format
            format_type: Optional format specification (e.g., 'json', 'yaml', 'markdown')

        Returns:
            Formatted string
        """
        pass


class TemplateRendererInterface(ABC):
    """Interface for template rendering."""

    @abstractmethod
    def render(self, template_string: str, context: Dict[str, Any]) -> str:
        """Render template with context.

        Args:
            template_string: Template string to render
            context: Context data for rendering

        Returns:
            Rendered template string
        """
        pass

    @abstractmethod
    def render_from_file(self, template_path: str, context: Dict[str, Any]) -> str:
        """Render template from file with context.

        Args:
            template_path: Path to template file
            context: Context data for rendering

        Returns:
            Rendered template string
        """
        pass
