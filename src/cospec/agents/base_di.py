"""Dependency Injection enabled BaseAgent with DI and non-DI constructor compatibility.

This module provides a DI-enabled BaseAgent that supports both traditional
constructor injection (config, tool_name) and DI-based initialization,
ensuring backward compatibility while enabling DI adoption.
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

from cospec.core.adapters import SubprocessManager
from cospec.core.config import CospecConfig, ToolConfig
from cospec.core.exceptions import CospecError, ToolExecutionError
from cospec.core.interfaces import (
    AnalyzerInterface,
    ExceptionHandlerInterface,
    LoggerInterface,
    TemplateRendererInterface,
)
from cospec.dependencies.deps import BaseDeps


class DIBaseAgent:
    """Base agent with dependency injection support.

    This class provides two initialization patterns:
    1. DI-based: Constructor injection with AgentDeps
    2. Traditional: Direct parameter injection with config and tool_name

    This ensures backward compatibility while enabling gradual DI adoption.
    """

    def __init__(
        self, config: Optional[CospecConfig] = None, tool_name: Optional[str] = None, deps: Optional[BaseDeps] = None
    ):
        """Initialize BaseAgent with DI or traditional approach.

        Args:
            config: CospecConfig instance (for traditional init)
            tool_name: Tool name to use (for traditional init)
            deps: Dependency container (for DI init)

        Note:
            Either (config) OR (deps with config in extra) must be provided.
            If both are provided, deps takes precedence for DI initialization.
        """
        if deps is not None:
            # DI-based initialization
            self._deps = deps
            if config is None:
                # Extract config from deps extra
                config = deps.get_extra("config")
                if config is None:
                    raise ValueError("AgentDeps must contain 'config' in extra when using DI")
        elif config is not None:
            # Traditional initialization - create minimal deps
            from cospec.core.adapters import ConsoleLogger, FileConfig, GenericExceptionHandler

            self._deps = BaseDeps(
                logger=ConsoleLogger(),  # Default logger
                config=FileConfig(config),
                exception_handler=GenericExceptionHandler(ConsoleLogger()),
            )
        else:
            raise ValueError("Either 'config' or 'deps' must be provided")

        self.config = config
        self.tool_name = tool_name or config.default_tool

        if self.tool_name not in config.tools:
            raise ValueError(f"Tool '{self.tool_name}' not configured.")

        self.tool_config: ToolConfig = config.tools[self.tool_name]

        # Initialize services from DI
        self.logger = self._resolve_service(LoggerInterface, "logger")
        self.exception_handler = self._resolve_service(ExceptionHandlerInterface, "exception_handler")
        self.analyzer = self._resolve_service(AnalyzerInterface, "analyzer")
        self.template_renderer = self._resolve_service(TemplateRendererInterface, "template_renderer")

    def _resolve_service(self, interface, attr_name: str):
        """Resolve service from DI or fallback to deps attribute."""
        # Try container first
        try:
            from cospec.dependencies import get_container

            container = get_container()
            return container.resolve(interface)
        except (RuntimeError, ValueError):
            pass

        # Fallback to deps attribute
        return getattr(self._deps, attr_name, None)

    def _build_prompt(self, base_prompt: str) -> str:
        """Appends language instruction to the prompt."""
        if self.logger:
            self.logger.debug(f"Building prompt with language: {self.config.language}")

        lang_instruction = ""
        if self.config.language == "ja":
            lang_instruction = "\n\nIMPORTANT: Please answer in Japanese."
        elif self.config.language == "en":
            lang_instruction = "\n\nIMPORTANT: Please answer in English."

        return base_prompt + lang_instruction

    def run_tool(self, prompt: str) -> str:
        """
        Executes external tool with the given prompt.
        Uses file-based approach for long prompts.
        """
        if self.logger:
            self.logger.info(f"Executing tool: {self.tool_name}")

        full_prompt = self._build_prompt(prompt)

        cmd_args = [self.tool_config.command]

        has_file_placeholder = any("{file}" in arg for arg in self.tool_config.args)
        has_prompt_placeholder = any("{prompt}" in arg for arg in self.tool_config.args)

        # Prepare local cache directory for temp files
        cache_dir = Path.cwd() / ".cospec" / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)

        temp_file = None
        execution_context = {"tool": self.tool_name, "command": self.tool_config.command}

        try:
            if has_file_placeholder and "{prompt}" in str(self.tool_config.args):
                with tempfile.NamedTemporaryFile(
                    mode="w", delete=False, encoding="utf-8", suffix=".txt", dir=cache_dir
                ) as f:
                    f.write(full_prompt)
                    temp_file = f.name

                for arg in self.tool_config.args:
                    if "{file}" in arg:
                        cmd_args.append(arg.replace("{file}", temp_file))
                    elif "{prompt}" in arg:
                        pass
                    else:
                        cmd_args.append(arg)

            elif has_prompt_placeholder:
                if len(full_prompt) > 8000:
                    with tempfile.NamedTemporaryFile(
                        mode="w", delete=False, encoding="utf-8", suffix=".txt", dir=cache_dir
                    ) as f:
                        f.write(full_prompt)
                        temp_file = f.name

                    cmd_args.append(f"@{temp_file}")
                else:
                    for arg in self.tool_config.args:
                        if "{prompt}" in arg:
                            cmd_args.append(arg.replace("{prompt}", full_prompt))
                        else:
                            cmd_args.append(arg)
            else:
                for arg in self.tool_config.args:
                    cmd_args.append(arg)

            process_manager = SubprocessManager()
            result = process_manager.run(cmd_args)

            if self.logger:
                self.logger.info("Tool execution completed successfully")

            return str(result.stdout)

        except ToolExecutionError as e:
            error_context = {
                "tool_name": self.tool_name,
                "command": " ".join(cmd_args),
                "full_prompt_length": len(full_prompt),
                **execution_context,
            }

            if self.exception_handler:
                self.exception_handler.handle(e, context=error_context, error_code="TOOL_EXECUTION_ERROR")

            # Re-raise the exception after handling
            raise

        except Exception as e:
            error_context = {"tool_name": self.tool_name, "command": " ".join(cmd_args), **execution_context}

            if self.exception_handler:
                wrapped_exception = self.exception_handler.wrap_with_context(
                    e, context=error_context, error_code="TOOL_EXECUTION_ERROR"
                )
                raise wrapped_exception from e
            else:
                raise

        finally:
            if temp_file:
                try:
                    os.unlink(temp_file)
                except Exception as cleanup_error:
                    if self.logger:
                        self.logger.warning(f"Failed to cleanup temp file: {cleanup_error}")

    def get_dependencies(self) -> BaseDeps:
        """Get the dependency container for this agent."""
        return self._deps

    def _execute_with_error_handling(self, func, *args, **kwargs):
        """Execute function with error handling and logging.

        This method provides centralized error handling for agent operations.
        """
        try:
            if self.logger:
                self.logger.debug(f"Executing: {func.__name__}")

            result = func(*args, **kwargs)

            if self.logger:
                self.logger.debug(f"Completed: {func.__name__}")

            return result

        except CospecError:
            raise  # Re-raise CospecErrors as they're already handled

        except Exception as e:
            error_context = {"function": func.__name__, "agent": self.__class__.__name__}

            if self.exception_handler:
                wrapped = self.exception_handler.wrap_with_context(
                    e, context=error_context, error_code=f"{self.__class__.__name__.upper()}_ERROR"
                )
                raise wrapped from e
            else:
                raise
