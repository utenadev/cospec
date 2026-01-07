from typing import Optional

from cospec.agents.base import BaseAgent
from cospec.agents.hearer import HearerAgent
from cospec.agents.reviewer import ReviewerAgent
from cospec.agents.test_generator import TestGeneratorAgent
from cospec.core.adapters import (
    ConsoleLogger,
    FileConfig,
    GenericExceptionHandler,
    ProjectAnalyzer,
    RichFormatter,
    YamlTemplateRenderer,
)
from cospec.core.config import CospecConfig
from cospec.core.interfaces import (
    AnalyzerInterface,
    ConfigInterface,
    ExceptionHandlerInterface,
    FormatterInterface,
    LoggerInterface,
    TemplateRendererInterface,
)
from cospec.dependencies.container import Container


class Factories:
    """Factory methods for creating component instances."""

    @staticmethod
    def create_config_singleton(config: CospecConfig) -> ConfigInterface:
        """Create a singleton configuration instance."""
        return FileConfig(config)

    @staticmethod
    def create_logger_singleton() -> LoggerInterface:
        """Create a singleton logger instance."""
        return ConsoleLogger()

    @staticmethod
    def create_formatter() -> FormatterInterface:
        """Create a formatter instance."""
        return RichFormatter()

    @staticmethod
    def create_exception_handler(logger: Optional[LoggerInterface] = None) -> ExceptionHandlerInterface:
        """Create an exception handler instance."""
        if logger is None:
            logger = Container().resolve(LoggerInterface)
        return GenericExceptionHandler(logger)

    @staticmethod
    def create_template_renderer() -> TemplateRendererInterface:
        """Create a template renderer instance."""
        return YamlTemplateRenderer()

    @staticmethod
    def create_analyzer(config: Optional[ConfigInterface] = None) -> AnalyzerInterface:
        """Create a project analyzer instance."""
        if config is None:
            config = Container().resolve(ConfigInterface)
        return ProjectAnalyzer(config)

    @staticmethod
    def create_base_agent(config: CospecConfig, tool_name: Optional[str] = None) -> BaseAgent:
        """Create a base agent instance."""
        return BaseAgent(config, tool_name)

    @staticmethod
    def create_reviewer_agent(config: CospecConfig, tool_name: Optional[str] = None) -> ReviewerAgent:
        """Create a reviewer agent instance."""
        return ReviewerAgent(config, tool_name)

    @staticmethod
    def create_hearer_agent(config: CospecConfig, tool_name: Optional[str] = None) -> HearerAgent:
        """Create a hearer agent instance."""
        return HearerAgent(config, tool_name)

    @staticmethod
    def create_test_generator_agent(config: CospecConfig, tool_name: Optional[str] = None) -> TestGeneratorAgent:
        """Create a test generator agent instance."""
        return TestGeneratorAgent(config, tool_name)

    @staticmethod
    def register_core_components(container: Container, config: CospecConfig) -> None:
        """Register all core components in the container."""
        container.register_singleton(ConfigInterface, Factories.create_config_singleton(config))
        container.register_singleton(LoggerInterface, Factories.create_logger_singleton())
        container.register_factory(FormatterInterface, Factories.create_formatter)
        container.register_factory(TemplateRendererInterface, Factories.create_template_renderer)
        container.register_factory(AnalyzerInterface, Factories.create_analyzer)

    @staticmethod
    def register_agent_components(container: Container, config: CospecConfig) -> None:
        """Register agent components in the container."""

        def _create_base_agent(tool_name: Optional[str] = None) -> BaseAgent:
            return Factories.create_base_agent(config, tool_name)

        def _create_reviewer(tool_name: Optional[str] = None) -> ReviewerAgent:
            return Factories.create_reviewer_agent(config, tool_name)

        def _create_hearer(tool_name: Optional[str] = None) -> HearerAgent:
            return Factories.create_hearer_agent(config, tool_name)

        def _create_test_gen(tool_name: Optional[str] = None) -> TestGeneratorAgent:
            return Factories.create_test_generator_agent(config, tool_name)

        container.register_factory(BaseAgent, _create_base_agent)
        container.register_factory(ReviewerAgent, _create_reviewer)
        container.register_factory(HearerAgent, _create_hearer)
        container.register_factory(TestGeneratorAgent, _create_test_gen)
