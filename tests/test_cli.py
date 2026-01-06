from typer.testing import CliRunner
from unittest.mock import patch
from cospec.main import app
from cospec.core.config import CospecConfig, ToolConfig

runner = CliRunner()

def test_hear_command_success():
    """
    Test the 'hear' command for successful prompt generation.
    """
    mock_config = CospecConfig(
        default_tool="mock_tool",
        dev_tool="mock_tool",
        language="en",
        tools={"mock_tool": ToolConfig(command="mock_command", args=[])}
    )

    with patch('cospec.main.load_config', return_value=mock_config):
        with patch('cospec.main.HearerAgent.create_mission_prompt', return_value="Mocked Mission Prompt"):
            result = runner.invoke(app, ["hear"])
            assert result.exit_code == 0
            assert "Mocked Mission Prompt" in result.stdout
            assert "Generating mission prompt for AI Agent..." in result.stdout

def test_hear_command_error():
    """
    Test the 'hear' command when prompt generation fails.
    """
    mock_config = CospecConfig(
        default_tool="mock_tool",
        dev_tool="mock_tool",
        language="en",
        tools={"mock_tool": ToolConfig(command="mock_command", args=[])}
    )

    with patch('cospec.main.load_config', return_value=mock_config):
        with patch('cospec.main.HearerAgent.create_mission_prompt', return_value="Error: Something went wrong"):
            result = runner.invoke(app, ["hear"])
            assert result.exit_code == 1
            assert "Error: Something went wrong" in result.stdout
