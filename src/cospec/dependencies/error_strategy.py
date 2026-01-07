"""Error strategy interfaces for implementing Liskov Substitution Principle.

This module provides structured error handling with clear separation
between core roles and use-case specific behaviors, enabling polymorphic
error handling across different components.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Protocol, runtime_checkable


@runtime_checkable
class ErrorContextProtocol(Protocol):
    """Protocol defining error context information."""

    error_code: str
    message: str
    original_error: Optional[Exception]
    context: Dict[str, Any]
    severity: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert error context to dictionary."""
        ...


class ErrorContext:
    """Structured error context for consistent error reporting.

    Implements ErrorContextProtocol and provides a standard way
    to capture and transport error information.
    """

    def __init__(
        self,
        error_code: str,
        message: str,
        original_error: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None,
        severity: str = "error",
    ):
        self.error_code = error_code
        self.message = message
        self.original_error = original_error
        self.context = context or {}
        self.severity = severity

    def to_dict(self) -> Dict[str, Any]:
        """Convert error context to dictionary."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "original_error": str(self.original_error) if self.original_error else None,
            "context": self.context,
            "severity": self.severity,
        }

    def __repr__(self) -> str:
        return f"ErrorContext(code={self.error_code}, severity={self.severity}, message={self.message})"


class ErrorStrategyInterface(ABC):
    """Interface for error handling strategies following Liskov Substitution Principle.

    This interface defines a contract for error handling with clear boundaries
    between different error types and use cases.
    """

    @abstractmethod
    def handle_error(self, error_context: ErrorContextProtocol) -> None:
        """Handle an error based on the provided context.

        Args:
            error_context: Structured context containing error information

        Raises:
            May re-raise the error or raise a different exception based on strategy
        """
        pass

    @abstractmethod
    def can_handle(self, error_context: ErrorContextProtocol) -> bool:
        """Check if this strategy can handle the given error context.

        Args:
            error_context: Error context to check

        Returns:
            True if this strategy can handle the error, False otherwise
        """
        pass


class BaseErrorHandler(ErrorStrategyInterface):
    """Base error handler implementing common error handling logic.

    This class provides the foundation for all error handlers,
    implementing the Liskov Substitution Principle by defining
    a common interface with shared behavior.
    """

    def __init__(self, logger: Optional[Any] = None):
        """Initialize base error handler.

        Args:
            logger: Optional logger instance for error logging
        """
        self.logger = logger

    def handle_error(self, error_context: ErrorContextProtocol) -> None:
        """Handle error with structured context."""
        if not self.can_handle(error_context):
            raise ValueError(f"Cannot handle error context: {error_context}")

        self._log_error(error_context)
        self._perform_handle(error_context)

    def can_handle(self, error_context: ErrorContextProtocol) -> bool:
        """Check if handler can handle the error context."""
        return True  # Base handler can handle all errors

    def _log_error(self, error_context: ErrorContextProtocol) -> None:
        """Log the error if logger is available."""
        if self.logger and hasattr(self.logger, "error"):
            self.logger.error(f"[{error_context.error_code}] {error_context.message}", extra=error_context.to_dict())

    @abstractmethod
    def _perform_handle(self, error_context: ErrorContextProtocol) -> None:
        """Perform actual error handling logic.

        Subclasses must implement this method to define specific
        error handling behavior.
        """
        pass


class RethrowErrorHandler(BaseErrorHandler):
    """Error handler that re-throws exceptions.

    This handler wraps the original error in a standardized exception
    and re-raises it for upstream handling.
    """

    def _perform_handle(self, error_context: ErrorContextProtocol) -> None:
        """Re-throw the error with standardized exception."""
        from cospec.core.exceptions import CospecError

        # Create a standardized exception
        exc = CospecError(
            message=f"[{error_context.error_code}] {error_context.message}", original_error=error_context.original_error
        )

        # Attach context information
        for key, value in error_context.context.items():
            setattr(exc, key, value)

        raise exc


class SuppressErrorHandler(BaseErrorHandler):
    """Error handler that suppresses errors.

    This handler logs the error but does not re-raise it,
    allowing execution to continue.
    """

    def _perform_handle(self, error_context: ErrorContextProtocol) -> None:
        """Suppress the error (no re-raise)."""
        # Error is already logged by base class
        pass


class RetryErrorHandler(BaseErrorHandler):
    """Error handler that implements retry logic.

    This handler can be used for transient errors that might
    succeed on retry.
    """

    def __init__(self, max_retries: int = 3, logger: Optional[Any] = None):
        """Initialize retry handler.

        Args:
            max_retries: Maximum number of retry attempts
            logger: Optional logger instance
        """
        super().__init__(logger)
        self.max_retries = max_retries

    def _perform_handle(self, error_context: ErrorContextProtocol) -> None:
        """Handle error with retry logic."""
        # In a real implementation, this would execute retry logic
        # For now, we'll just raise the error to indicate retry needed
        raise error_context.original_error or RuntimeError(error_context.message)


class CompoundErrorHandler(BaseErrorHandler):
    """Error handler that delegates to multiple handlers.

    This handler allows composition of different error handling
    strategies based on error type or context.
    """

    def __init__(
        self, handlers: Dict[str, ErrorStrategyInterface], default_handler: Optional[ErrorStrategyInterface] = None
    ):
        """Initialize compound handler.

        Args:
            handlers: Dictionary mapping error codes to handlers
            default_handler: Handler to use when no specific handler matches
        """
        super().__init__(logger=None)
        self.handlers = handlers
        self.default_handler = default_handler or RethrowErrorHandler()

    def handle_error(self, error_context: ErrorContextProtocol) -> None:
        """Delegate to appropriate handler based on error code."""
        handler = self.handlers.get(error_context.error_code, self.default_handler)
        handler.handle_error(error_context)

    def can_handle(self, error_context: ErrorContextProtocol) -> bool:
        """Check if any handler can handle the error."""
        handler = self.handlers.get(error_context.error_code, self.default_handler)
        return handler.can_handle(error_context)

    def _perform_handle(self, error_context: ErrorContextProtocol) -> None:
        """This method is not used in compound handler."""
        pass  # Delegation happens in handle_error


# Factory functions for creating error handlers
def create_basic_error_handler(logger: Optional[Any] = None) -> BaseErrorHandler:
    """Create a basic re-throw error handler."""
    return RethrowErrorHandler(logger)


def create_suppress_error_handler(logger: Optional[Any] = None) -> BaseErrorHandler:
    """Create a suppress error handler."""
    return SuppressErrorHandler(logger)


def create_retry_error_handler(max_retries: int = 3, logger: Optional[Any] = None) -> BaseErrorHandler:
    """Create a retry error handler."""
    return RetryErrorHandler(max_retries, logger)


def create_compound_error_handler(
    handlers: Dict[str, ErrorStrategyInterface],
    default_handler: Optional[ErrorStrategyInterface] = None,
    logger: Optional[Any] = None,
) -> CompoundErrorHandler:
    """Create a compound error handler with multiple strategies."""
    return CompoundErrorHandler(handlers, default_handler)
