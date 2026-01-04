from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import json

class ToolConfig(BaseModel):
    command: str
    args: List[str]

class CospecConfig(BaseSettings):
    default_tool: str = "qwen"
    language: str = "ja"
    tools: Dict[str, ToolConfig] = Field(default_factory=lambda: {
        "qwen": ToolConfig(command="qwen", args=["{prompt}"]),
        "opencode": ToolConfig(command="opencode", args=["run", "{prompt}"])
    })
    
    model_config = SettingsConfigDict(env_prefix="cospec_")

def load_config(config_path: Optional[Path] = None) -> CospecConfig:
    # Logic to load from file could be added here, currently just returns defaults/env vars
    # For MVP, we can assume defaults are fine or override via environment
    return CospecConfig()
