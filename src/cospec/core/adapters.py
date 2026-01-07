"""Concrete implementations of external dependency interfaces."""

import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
from rich.console import Console

from cospec.core.config import CospecConfig
from cospec.core.interfaces import (
    AnalyzerInterface,
    ConfigInterface,
    ConsoleInterface,
    ExceptionHandlerInterface,
    FilesystemInterface,
    FormatterInterface,
    LoggerInterface,
    ProcessInterface,
    TemplateRendererInterface,
)


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


# ==== Logger Implementation ====


class ConsoleLogger(LoggerInterface):
    """Logger implementation using Rich console."""

    def __init__(self):
        self.console = Console()

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.console.print(f"[cyan]DEBUG:[/cyan] {message}", **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self.console.print(f"[green]INFO:[/green] {message}", **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.console.print(f"[yellow]WARNING:[/yellow] {message}", **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self.console.print(f"[red]ERROR:[/red] {message}", **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """Log critical message."""
        self.console.print(f"[bold red]CRITICAL:[/bold red] {message}", **kwargs)


# ==== Exception Handler Implementation ====


class GenericExceptionHandler(ExceptionHandlerInterface):
    """Generic exception handler with logging and error wrapping."""

    def __init__(self, logger: LoggerInterface):
        self.logger = logger

    def handle(
        self, exception: Exception, context: Optional[Dict[str, Any]] = None, error_code: Optional[str] = None
    ) -> None:
        """Handle exception with logging."""
        error_code = error_code or exception.__class__.__name__
        context = context or {}

        self.logger.error(f"[{error_code}] {str(exception)}", extra={"context": context, "error_code": error_code})

    def wrap_with_context(
        self, exception: Exception, context: Optional[Dict[str, Any]] = None, error_code: Optional[str] = None
    ) -> Exception:
        """Wrap exception with context."""
        from cospec.core.exceptions import CospecError

        if isinstance(exception, CospecError):
            return exception

        error_code = error_code or exception.__class__.__name__
        context = context or {}

        wrapped = CospecError(message=f"[{error_code}] {str(exception)}", original_error=exception)

        wrapped._context = context
        wrapped._error_code = error_code

        return wrapped


# ==== Formatter Implementation ====


class RichFormatter(FormatterInterface):
    """Formatter using Rich for styled output."""

    def __init__(self):
        self.console = Console()

    def format_output(self, data: Any, format_type: Optional[str] = None) -> str:
        """Format output based on type."""
        if format_type == "json":
            import json

            return json.dumps(data, indent=2, default=str)
        elif format_type == "yaml":
            import yaml

            return yaml.dump(data, default_flow_style=False)
        else:
            return str(data)


# ==== Template Renderer Implementation ====


class YamlTemplateRenderer(TemplateRendererInterface):
    """Template renderer that supports basic YAML-style variable substitution."""

    def render(self, template_string: str, context: Dict[str, Any]) -> str:
        """Render template string with context."""
        result = template_string
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            result = result.replace(placeholder, str(value))
        return result

    def render_from_file(self, template_path: str, context: Dict[str, Any]) -> str:
        """Render template from file."""
        path = Path(template_path)
        if not path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")

        template_content = path.read_text(encoding="utf-8")
        return self.render(template_content, context)


# ==== Analyzer Implementation ====


class ProjectAnalyzer(AnalyzerInterface):
    """Project analyzer for collecting context and structure."""

    def __init__(self, config: CospecConfig):
        self.config = config

    def analyze_project(self, project_path: Optional[str] = None) -> Dict[str, Any]:
        """Analyze project structure."""
        project_path = Path(project_path or Path.cwd())

        analysis = {
            "project_root": str(project_path),
            "spec_files": self._find_spec_files(project_path),
            "source_files": self._find_source_files(project_path),
            "test_files": self._find_test_files(project_path),
            "structure": self._analyze_structure(project_path),
        }

        return analysis

    def get_context_summary(self) -> str:
        """Get project context summary."""
        # Placeholder implementation
        return "Project context analysis ready."

    def _find_spec_files(self, path: Path) -> List[str]:
        """Find specification files."""
        spec_patterns = ["*.md", "docs/*.md", "spec/*.md"]
        found = []
        for pattern in spec_patterns:
            found.extend([str(p) for p in path.glob(pattern)])
        return found

    def _find_source_files(self, path: Path) -> List[str]:
        """Find source code files."""
        patterns = ["src/**/*.py", "*.py"]
        found = []
        for pattern in patterns:
            found.extend([str(p) for p in path.glob(pattern) if p.is_file()])
        return found

    def _find_test_files(self, path: Path) -> List[str]:
        """Find test files."""
        patterns = ["tests/**/*.py", "test/**/*.py"]
        found = []
        for pattern in patterns:
            found.extend([str(p) for p in path.glob(pattern) if p.is_file()])
        return found

    def _analyze_structure(self, path: Path) -> Dict[str, Any]:
        """Analyze project directory structure."""
        structure = {"directories": [], "key_files": []}

        for item in path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                structure["directories"].append(item.name)
            elif item.is_file() and item.suffix in [".py", ".md", ".yml", ".yaml", ".toml"]:
                structure["key_files"].append(item.name)

        return structure


# ==== Configuration Adapter ====


class FileConfig(ConfigInterface):
    """Configuration adapter that loads from file."""

    def __init__(self, config: CospecConfig):
        self.config = config

    def load_from_file(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file."""
        return {
            "default_tool": self.config.default_tool,
            "language": self.config.language,
            "tools": {name: tool.dict() for name, tool in self.config.tools.items()},
        }

    def save_to_file(self, config_path: Optional[str] = None) -> None:
        """Save configuration to file."""
        # Not implemented for now
        pass
