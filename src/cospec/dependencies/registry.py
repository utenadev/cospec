from typing import Callable, Dict, Optional

from cospec.core.config import CospecConfig
from cospec.core.interfaces import ConfigInterface, LLMInterface


class Registry:
    _registered_components: Dict[str, Callable] = {}
    _registered_connectors: Dict[str, Callable[[CospecConfig], LLMInterface]] = {}
    _registered_configs: Dict[str, Callable[[], ConfigInterface]] = {}

    @classmethod
    def register_component(cls, name: str, factory: Callable) -> None:
        """Register a component factory."""
        cls._registered_components[name] = factory

    @classmethod
    def get_component(cls, name: str) -> Optional[Callable]:
        """Get a registered component factory."""
        return cls._registered_components.get(name)

    @classmethod
    def register_connector(cls, tool_name: str, connector: Callable[[CospecConfig], LLMInterface]) -> None:
        """Register an LLM connector."""
        cls._registered_connectors[tool_name] = connector

    @classmethod
    def get_connector(cls, tool_name: str) -> Optional[Callable[[CospecConfig], LLMInterface]]:
        """Get a registered connector."""
        return cls._registered_connectors.get(tool_name)

    @classmethod
    def get_registered_connectors(cls) -> list[str]:
        """Get list of registered connector names."""
        return list(cls._registered_connectors.keys())

    @classmethod
    def register_config(cls, config_name: str, config_factory: Callable[[], ConfigInterface]) -> None:
        """Register a configuration factory."""
        cls._registered_configs[config_name] = config_factory

    @classmethod
    def get_config(cls, config_name: str) -> Optional[Callable[[], ConfigInterface]]:
        """Get a registered configuration factory."""
        return cls._registered_configs.get(config_name)

    @classmethod
    def reset(cls) -> None:
        """Reset registry (for testing)."""
        cls._registered_components.clear()
        cls._registered_connectors.clear()
        cls._registered_configs.clear()
