import typer
from rich.console import Console
from pathlib import Path

app = typer.Typer(help="cospec: Collaborative Specification CLI")
console = Console()

@app.command()
def init() -> None:
    """
    Initialize a new cospec project with the recommended structure.
    """
    console.print("[bold blue]Initializing cospec project...[/bold blue]")

    # 1. Create docs directory
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # 2. Define templates (Minimal content for now)
    files = {
        "docs/SPEC.md": "# SPEC: Project Name\n\n## 1. Overview\n\n## 2. Requirements\n",
        "docs/OverviewDesignThinking.md": "# Overview: Design Thinking\n\n- Codebase as Context\n- Consistency First\n",
        "Taskfile.yml": "version: '3'\n\ntasks:\n  setup:\n    cmds:\n      - echo 'Setup'\n",
        ".gitignore": "venv/\n__pycache__/\n.env\n",
    }

    created_count = 0
    skipped_count = 0

    for path_str, content in files.items():
        path = Path(path_str)
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            console.print(f"[green]Created[/green]: {path}")
            created_count += 1
        else:
            console.print(f"[yellow]Skipped[/yellow]: {path} (already exists)")
            skipped_count += 1

    console.print(f"\n[bold]Done![/bold] Created {created_count} files, skipped {skipped_count} files.")

@app.command()
def status() -> None:
    """
    Show project status and next actions.
    """
    console.print("[bold blue]cospec status[/bold blue]")
    console.print("Current Phase: [green]Inception[/green]")
    console.print("\nNext Action: Update SPEC.md or run 'cospec hear'")

if __name__ == "__main__":
    app()

