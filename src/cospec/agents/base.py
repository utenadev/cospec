import os
import tempfile
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from cospec.core.adapters import SubprocessManager
from cospec.core.config import CospecConfig, ToolConfig
from cospec.core.exceptions import ToolExecutionError
from cospec.core.interfaces import ExceptionHandlerInterface, LoggerInterface

if TYPE_CHECKING:
    from cospec.dependencies.deps import BaseDeps


class BaseAgent:
    def __init__(self, config: CospecConfig, tool_name: Optional[str] = None, deps: Optional["BaseDeps"] = None):
        """Initialize BaseAgent with DI support.

        Args:
            config: CospecConfig instance
            tool_name: Optional tool name (defaults to config.default_tool)
            deps: Optional dependency container for DI
        """
        self.config = config
        self.tool_name = tool_name or config.default_tool

        if self.tool_name not in config.tools:
            raise ValueError(f"Tool '{self.tool_name}' not configured.")

        self.tool_config: ToolConfig = config.tools[self.tool_name]

        # DI support - initialize from deps if provided
        self._deps = deps
        self.logger: Optional[LoggerInterface] = None
        self.exception_handler: Optional[ExceptionHandlerInterface] = None

        if deps:
            self.logger = deps.logger
            self.exception_handler = deps.exception_handler

    def _build_prompt(self, base_prompt: str) -> str:
        """
        Appends language instruction to the prompt.
        """
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

            # Re-raise with enhanced error message
            error_msg = f"Error running tool {self.tool_name}: "
            if e.original_error and hasattr(e.original_error, "stderr"):
                error_msg += e.original_error.stderr
            raise ToolExecutionError(error_msg, original_error=e.original_error) from e

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

    def get_dependencies(self) -> Optional["BaseDeps"]:
        """Get the dependency container for this agent."""
        return self._deps
