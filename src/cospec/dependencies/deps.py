from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

from cospec.core.interfaces import (
    AnalyzerInterface,
    ConfigInterface,
    ExceptionHandlerInterface,
    FormatterInterface,
    LoggerInterface,
    TemplateRendererInterface,
)


@dataclass
class BaseDeps:
    """Base dependency container for component initialization.

    This class provides a standardized way to inject dependencies
    into components and agents, following the Dependency Injection pattern.
    """

    logger: LoggerInterface
    config: ConfigInterface
    exception_handler: ExceptionHandlerInterface
    analyzer: Optional[AnalyzerInterface] = None
    formatter: Optional[FormatterInterface] = None
    template_renderer: Optional[TemplateRendererInterface] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    _initialized: bool = field(default=False, init=False, repr=False)

    def __post_init__(self):
        """Initialize the dependency container."""
        self._validate_dependencies()
        self._initialized = True

    def _validate_dependencies(self) -> None:
        """Validate that required dependencies are provided."""
        required = {
            "logger": self.logger,
            "config": self.config,
            "exception_handler": self.exception_handler,
        }

        for name, dep in required.items():
            if dep is None:
                raise ValueError(f"Required dependency '{name}' is None")

    @classmethod
    def create(
        cls,
        logger: LoggerInterface,
        config: ConfigInterface,
        exception_handler_factory: Optional[Callable[[LoggerInterface], ExceptionHandlerInterface]] = None,
        analyzer: Optional[AnalyzerInterface] = None,
        formatter: Optional[FormatterInterface] = None,
        template_renderer: Optional[TemplateRendererInterface] = None,
        **kwargs: Any,
    ) -> "BaseDeps":
        """Create BaseDeps instance with optional factory for exception handler.

        Args:
            logger: Logger interface instance
            config: Config interface instance
            exception_handler_factory: Factory to create exception handler (receives logger)
            analyzer: Optional analyzer interface
            formatter: Optional formatter interface
            template_renderer: Optional template renderer interface
            **kwargs: Additional dependencies to store in extra

        Returns:
            BaseDeps instance
        """
        if exception_handler_factory:
            exception_handler = exception_handler_factory(logger)
        else:
            # Default exception handler
            from cospec.core.adapters import GenericExceptionHandler

            exception_handler = GenericExceptionHandler(logger)

        return cls(
            logger=logger,
            config=config,
            exception_handler=exception_handler,
            analyzer=analyzer,
            formatter=formatter,
            template_renderer=template_renderer,
            extra=kwargs,
        )

    def get_extra(self, key: str, default: Any = None) -> Any:
        """Get an extra dependency by key."""
        return self.extra.get(key, default)

    def set_extra(self, key: str, value: Any) -> None:
        """Set an extra dependency."""
        self.extra[key] = value

    def update_extras(self, updates: Dict[str, Any]) -> None:
        """Update multiple extra dependencies."""
        self.extra.update(updates)

    def ensure_deps_initialized(self) -> None:
        """Ensure dependencies are initialized (no-op if already initialized)."""
        if not self._initialized:
            self.__post_init__()


class CoreDeps(BaseDeps):
    """Core dependencies for fundamental components."""

    analyzer: AnalyzerInterface
    formatter: FormatterInterface
    template_renderer: TemplateRendererInterface

    def __post_init__(self):
        """Initialize core dependencies."""
        super().__post_init__()
        self._validate_core_dependencies()

    def _validate_core_dependencies(self) -> None:
        """Validate that core dependencies are provided."""
        required = {
            "analyzer": self.analyzer,
            "formatter": self.formatter,
            "template_renderer": self.template_renderer,
        }

        for name, dep in required.items():
            if dep is None:
                raise ValueError(f"Core dependency '{name}' is None")


class AgentDeps(BaseDeps):
    """Agent-specific dependencies."""

    analyzer: AnalyzerInterface
    template_renderer: TemplateRendererInterface

    def __post_init__(self):
        """Initialize agent dependencies."""
        super().__post_init__()
        self._validate_agent_dependencies()

    def _validate_agent_dependencies(self) -> None:
        """Validate that agent dependencies are provided."""
        required = {
            "analyzer": self.analyzer,
            "template_renderer": self.template_renderer,
        }

        for name, dep in required.items():
            if dep is None:
                raise ValueError(f"Agent dependency '{name}' is None")
