"""
Dependency Injection module for cospec.

This module provides:
- Container: Singleton DI container for managing dependencies
- Registry: Component registration and discovery
- Factories: Factory methods for creating component instances
- BaseDeps: Base dependency container class
- init_di(): Function to initialize the DI system
"""

from cospec.core.config import CospecConfig
from cospec.dependencies.container import Container
from cospec.dependencies.deps import AgentDeps, BaseDeps, CoreDeps
from cospec.dependencies.factories import Factories
from cospec.dependencies.registry import Registry

__all__ = [
    "BaseDeps",
    "CoreDeps",
    "AgentDeps",
    "Container",
    "Registry",
    "Factories",
    "DependencyManager",
]


class DependencyManager:
    """Manages dependency injection initialization and access."""

    _initialized: bool = False
    _container: Container = Container()

    @classmethod
    def initialize(cls, config: CospecConfig) -> None:
        """Initialize the dependency injection system."""
        if cls._initialized:
            return

        # Register core components
        Factories.register_core_components(cls._container, config)

        # Register agent components
        Factories.register_agent_components(cls._container, config)

        cls._initialized = True

    @classmethod
    def get_container(cls) -> Container:
        """Get the dependency injection container."""
        if not cls._initialized:
            raise RuntimeError("Dependency injection system not initialized. Call initialize() first.")
        return cls._container

    @classmethod
    def resolve(cls, interface):
        """Resolve an instance for a specific interface."""
        return cls.get_container().resolve(interface)

    @classmethod
    def reset(cls) -> None:
        """Reset the dependency injection system (for testing)."""
        cls._container.reset()
        cls._initialized = False

    @classmethod
    def is_initialized(cls) -> bool:
        """Check if DI system is initialized."""
        return cls._initialized


# Convenience functions for easier access
def init_di(config: CospecConfig) -> None:
    """Initialize the dependency injection system."""
    DependencyManager.initialize(config)


def get_container() -> Container:
    """Get the dependency injection container."""
    return DependencyManager.get_container()


def resolve(interface):
    """Resolve an instance for a specific interface."""
    return DependencyManager.resolve(interface)


def reset_di() -> None:
    """Reset the dependency injection system (for testing)."""
    DependencyManager.reset()
