import json
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ToolConfig(BaseModel):
    command: str
    args: List[str]


class CospecConfig(BaseSettings):
    default_tool: str = "qwen"
    dev_tool: str = ""
    language: str = "ja"
    tools: Dict[str, ToolConfig] = Field(
        default_factory=lambda: {
            "qwen": ToolConfig(command="qwen", args=["{prompt}"]),
            "opencode": ToolConfig(command="opencode", args=["run", "{prompt}"]),
        }
    )

    model_config = SettingsConfigDict(env_prefix="cospec_", env_file=".env", env_file_encoding="utf-8")

    def save_to_file(self, path: Optional[Path] = None) -> None:
        """Save configuration to a JSON file."""
        if path is None:
            path = Path(".cospec/config.json")

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(mode="json"), f, indent=2, ensure_ascii=False)

    def select_tool_for_development(self) -> str:
        """Select AI-Agent for development commands (hear, test-gen)."""
        if self.dev_tool and self.dev_tool in self.tools:
            return self.dev_tool
        return self.default_tool

    def select_tool_for_review(self) -> str:
        """Select AI-Agent for review command (not= dev tool)."""
        other_tools = [name for name in self.tools.keys() if name != self.dev_tool]
        if other_tools:
            import random

            return random.choice(other_tools)
        return self.default_tool


def load_config(config_path: Optional[Path] = None) -> CospecConfig:
    """Load configuration from file or use defaults."""
    if config_path is None:
        config_path = Path(".cospec/config.json")

    config_dict = {}

    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config_dict = json.load(f)

    return CospecConfig(**config_dict)
