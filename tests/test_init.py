import os
from pathlib import Path
from typer.testing import CliRunner
from cospec.main import app

runner = CliRunner()

def test_init_creates_files(tmp_path: Path) -> None:
    """
    Test that 'cospec init' creates the expected directory structure and files.
    """
    # Change current working directory to tmp_path for the test
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["init"])
        
        assert result.exit_code == 0
        assert "Initializing cospec project..." in result.stdout
        
        # Check docs exist
        assert os.path.exists("docs")
        assert os.path.exists("docs/SPEC.md")
        assert os.path.exists("docs/OverviewDesignThinking.md")
        
        # Check Taskfile and gitignore exist
        assert os.path.exists("Taskfile.yml")
        assert os.path.exists(".gitignore")

def test_init_skips_existing(tmp_path: Path) -> None:
    """
    Test that 'cospec init' does not overwrite existing files without confirmation (or just skips/warns for now).
    """
    with runner.isolated_filesystem(temp_dir=tmp_path):
        os.makedirs("docs")
        with open("docs/SPEC.md", "w") as f:
            f.write("Existing content")
            
        result = runner.invoke(app, ["init"])
        
        assert result.exit_code == 0
        # Should imply it didn't crash, and maybe warned. 
        # For MVP, just checking it doesn't crash is enough, 
        # but logically we'll check if content remains "Existing content" if we implement skip logic,
        # or changes if we implement overwrite. 
        # For now, let's just ensure it runs.
        
        with open("docs/SPEC.md", "r") as f:
            content = f.read()
        assert content == "Existing content" # Assuming we implement a check to not overwrite
