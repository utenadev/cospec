import subprocess
from typing import Optional

from cospec.core.config import CospecConfig, ToolConfig


class BaseAgent:
    def __init__(self, config: CospecConfig, tool_name: Optional[str] = None):
        self.config = config
        self.tool_name = tool_name or config.default_tool

        if self.tool_name not in config.tools:
            raise ValueError(f"Tool '{self.tool_name}' not configured.")

        self.tool_config: ToolConfig = config.tools[self.tool_name]

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
        full_prompt = self._build_prompt(prompt)

        import os
        import tempfile

        cmd_args = [self.tool_config.command]

        has_file_placeholder = any("{file}" in arg for arg in self.tool_config.args)
        has_prompt_placeholder = any("{prompt}" in arg for arg in self.tool_config.args)

        temp_file = None

        if has_file_placeholder and "{prompt}" in str(self.tool_config.args):
            with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", suffix=".txt") as f:
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
                with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", suffix=".txt") as f:
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

        try:
            result = subprocess.run(cmd_args, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running tool {self.tool_name}: {e.stderr}"
            raise RuntimeError(error_msg) from e
        finally:
            if temp_file:
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass
