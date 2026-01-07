from unittest.mock import patch

from typer.testing import CliRunner

from cospec.core.config import CospecConfig, ToolConfig
from cospec.main import app

runner = CliRunner()


def test_hear_command_success():
    """
    Test the 'hear' command for successful prompt generation.
    """
    mock_config = CospecConfig(
        default_tool="mock_tool",
        dev_tool="mock_tool",
        language="en",
        tools={"mock_tool": ToolConfig(command="mock_command", args=[])},
    )

    with patch("cospec.main.CospecConfig.load_config", return_value=mock_config):
        with patch("cospec.main.HearerAgent.create_mission_prompt", return_value="Mocked Mission Prompt"):
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
        tools={"mock_tool": ToolConfig(command="mock_command", args=[])},
    )

    with patch("cospec.main.CospecConfig.load_config", return_value=mock_config):
        with patch("cospec.main.HearerAgent.create_mission_prompt", return_value="Error: Something went wrong"):
            result = runner.invoke(app, ["hear"])
            assert result.exit_code == 1
            assert "Error: Something went wrong" in result.stdout


def test_hear_command_output_file():
    """
    Test the 'hear' command with the --output option.
    """
    mock_config = CospecConfig(
        default_tool="mock_tool",
        dev_tool="mock_tool",
        language="en",
        tools={"mock_tool": ToolConfig(command="mock_command", args=[])},
    )

    with patch("cospec.main.CospecConfig.load_config", return_value=mock_config):
        with patch("cospec.main.HearerAgent.create_mission_prompt", return_value="Mocked Mission Prompt"):
            with patch("pathlib.Path.write_text") as mock_write_text:
                result = runner.invoke(app, ["hear", "--output", "test.txt"])
                assert result.exit_code == 0
                mock_write_text.assert_called_once_with("Mocked Mission Prompt", encoding="utf-8")
                assert "Mission prompt saved to:" in result.stdout
                assert "test.txt" in result.stdout


def test_hear_command_general_exception():
    """
    Test the 'hear' command's general exception handling.
    """
    with patch("cospec.main.CospecConfig.load_config", side_effect=Exception("General Error")):
        result = runner.invoke(app, ["hear"])
        assert result.exit_code == 1
        assert "Error: General Error" in result.stdout
