from typing import Any, Callable, Dict, Optional, Type

from cospec.core.config import CospecConfig
from cospec.core.interfaces import LLMInterface

ConnectorRegistryType = Dict[str, Callable[[CospecConfig], LLMInterface]]


class Container:
    _instance: Optional["Container"] = None
    _factories: Dict[Type, Callable[..., Any]]
    _instances: Dict[Type, Any]
    _LLM_connectors: ConnectorRegistryType

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Container, cls).__new__(cls)
            cls._instance._factories = {}
            cls._instance._instances = {}
            cls._instance._LLM_connectors = {}
        return cls._instance

    def register_factory(self, interface: Type, factory: Callable[..., Any]) -> None:
        """Register a factory for a specific interface."""
        self._factories[interface] = factory

    def register_singleton(self, interface: Type, instance: Any) -> None:
        """Register a singleton instance for a specific interface."""
        self._instances[interface] = instance

    def register_connector(self, tool_name: str, connector: Callable[[CospecConfig], LLMInterface]) -> None:
        """Register an LLM connector factory for a specific tool."""
        self._LLM_connectors[tool_name] = connector

    def resolve(self, interface: Type) -> Any:
        """Resolve an instance for a specific interface."""
        if interface in self._instances:
            return self._instances[interface]

        if interface in self._factories:
            factory = self._factories[interface]
            instance = factory()
            if factory.__name__.endswith("_singleton"):
                self._instances[interface] = instance
            return instance

        raise ValueError(f"No factory or instance registered for {interface}")

    def resolve_connector(self, tool_name: str, config: CospecConfig) -> LLMInterface:
        """Resolve an LLM connector instance for a specific tool."""
        if tool_name not in self._LLM_connectors:
            raise ValueError(f"No connector registered for tool '{tool_name}'")
        return self._LLM_connectors[tool_name](config)

    def get_registered_connectors(self) -> list[str]:
        """Get a list of registered connector names."""
        return list(self._LLM_connectors.keys())

    def reset(self) -> None:
        """Reset the container (primarily for testing)."""
        self._factories.clear()
        self._instances.clear()
        self._LLM_connectors.clear()
