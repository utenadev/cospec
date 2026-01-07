from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from cospec.core.config import CospecConfig, ToolConfig
from cospec.main import app

runner = CliRunner()


class TestAgentCommands:
    """Test suite for agent management commands."""

    def test_agent_list_shows_agents(self) -> None:
        """Test agent list command shows registered agents."""
        result = runner.invoke(app, ["agent", "list"])

        assert result.exit_code == 0
        assert "Registered AI-Agents" in result.stdout
        assert "qwen" in result.stdout
        assert "opencode" in result.stdout

    def test_agent_add_success(self, tmp_path: Path) -> None:
        """Test adding a new AI-Agent successfully."""
        with patch("cospec.main.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="Usage: mycli [prompt] --help", stderr="", returncode=0)

            result = runner.invoke(app, ["agent", "add", "mycli", "--command", "mycli"])

            assert result.exit_code == 0
            assert "Success!" in result.stdout
            assert "mycli" in result.stdout

    def test_agent_add_command_not_found(self) -> None:
        """Test adding an AI-Agent with a non-existent command."""
        with patch("cospec.main.subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("Command not found")

            result = runner.invoke(app, ["agent", "add", "nonexistent", "--command", "nonexistent"])

            assert result.exit_code == 1
            assert "Error:" in result.stdout
            assert "not found" in result.stdout

    def test_config_save_and_load(self, tmp_path: Path) -> None:
        """Test that configuration can be saved and loaded correctly."""
        config_path = tmp_path / ".cospec" / "config.json"

        config = CospecConfig()
        config.tools["custom_tool"] = ToolConfig(command="custom", args=["arg1", "{prompt}"])
        config.save_to_file(config_path)

        loaded_config = CospecConfig.load_config(config_path)

        assert "custom_tool" in loaded_config.tools
        assert loaded_config.tools["custom_tool"].command == "custom"
        assert loaded_config.tools["custom_tool"].args == ["arg1", "{prompt}"]
