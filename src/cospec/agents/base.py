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
        Executes the external tool with the given prompt.
        """
        full_prompt = self._build_prompt(prompt)
        
        cmd_args = [self.tool_config.command]
        for arg in self.tool_config.args:
            if "{prompt}" in arg:
                cmd_args.append(arg.replace("{prompt}", full_prompt))
            else:
                cmd_args.append(arg)
                
        try:
            result = subprocess.run(cmd_args, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = f"Error running tool {self.tool_name}: {e.stderr}"
            raise RuntimeError(error_msg)
