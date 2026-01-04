import os
import pytest
from pathlib import Path
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from cospec.main import app

runner = CliRunner()

@pytest.fixture
def mock_subprocess():
    with patch("subprocess.run") as mock:
        mock_return = MagicMock()
        mock_return.stdout = "# Review Report\n\nNo issues found."
        mock_return.returncode = 0
        mock.return_value = mock_return
        yield mock

def test_review_creates_report(tmp_path: Path, mock_subprocess) -> None:
    """
    Test that 'cospec review' collects context, runs the tool (mocked), and saves a report.
    """
    # Setup a dummy project structure
    with runner.isolated_filesystem(temp_dir=tmp_path):
        os.makedirs("docs")
        with open("docs/SPEC.md", "w") as f:
            f.write("Spec content")
        os.makedirs("src/cospec")
        with open("src/cospec/main.py", "w") as f:
            f.write("print('hello')")
        
        # Run review
        result = runner.invoke(app, ["review", "--tool", "qwen"])
        
        # Check execution success
        assert result.exit_code == 0
        assert "Reviewing project..." in result.stdout
        
        # Check if subprocess was called
        assert mock_subprocess.called
        
        # Check report generation
        reports = list(Path("docs").glob("review_*.md"))
        assert len(reports) > 0, "Review report was not created"
        
        content = reports[0].read_text()
        assert "# Review Report" in content
