"""Custom exceptions for cospec application."""

from typing import Optional


class CospecError(Exception):
    """Base exception for cospec application."""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error


class ConfigurationError(CospecError):
    """Raised when configuration is invalid or missing."""

    pass


class ToolExecutionError(CospecError):
    """Raised when external tool execution fails."""

    pass


class PromptTemplateError(CospecError):
    """Raised when prompt template is missing or invalid."""

    pass


class SpecNotFoundError(CospecError):
    """Raised when SPEC.md file is not found."""

    pass


class InvalidToolError(CospecError):
    """Raised when AI-Agent tool is not configured or invalid."""

    pass
