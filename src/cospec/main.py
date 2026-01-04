import typer
from rich.console import Console
from pathlib import Path
import datetime
from cospec.core.config import load_config
from cospec.agents.reviewer import ReviewerAgent

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
    
    # 2. Define templates
    overview_design = """# Overview: Design Thinking

## 1. Codebase as Context
Documentation is the ground truth.

## 2. Consistency First
Eliminate discrepancies between docs and code before implementation.

## 3. Decision Support
AI provides options with Pros/Cons to support human decision-making.
"""

    overview_coding = """# Overview: Coding & Testing

## 1. Coding Standards: "Guardrails for AI"
- **Strong Typing**: Use Pydantic/Types everywhere. Avoid Any.
- **Self-Documenting**: Write Docstrings before implementation.

## 2. Testing Strategy: "Test-Driven Generation (TDG)"
1. **Scaffold**: Agree on test scenarios.
2. **Test Generation**: Write failing tests (Red) first.
3. **Implementation**: Write code to pass tests (Green).
4. **Refactoring**: Clean up code.
- **Mocking**: Mock all external I/O.
"""

    spec_template = """# SPEC: Project Name

## 1. Overview
Describe the project purpose and goals.

## 2. Requirements
List functional requirements.
"""

    taskfile_template = """version: '3'

tasks:
  setup:
    desc: Setup environment
    cmds:
      - echo 'Setup complete'

  test:
    desc: Run tests
    cmds:
      - echo 'Running tests...'"""

    files = {
        "docs/SPEC.md": spec_template,
        "docs/OverviewDesignThinking.md": overview_design,
        "docs/OverviewCodingTestingThinking.md": overview_coding,
        "Taskfile.yml": taskfile_template,
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

@app.command()
def review(tool: str = typer.Option(None, help="Tool to use (qwen, opencode)")) -> None:
    """
    Review the codebase against the documentation using an AI agent.
    """
    console.print("[bold blue]Reviewing project...[/bold blue]")
    
    try:
        # 1. Load Config & Initialize Agent
        config = load_config()
        agent = ReviewerAgent(config, tool_name=tool)
        
        console.print(f"Running {agent.tool_name} (Language: {config.language})...")
        
        # 2. Run Review
        report_content = agent.review_project()
        
        # 3. Save Report
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(f"docs/review_{date_str}_{agent.tool_name}.md")
        report_path.write_text(report_content, encoding="utf-8")
        
        console.print(f"[green]Review complete![/green] Report saved to: {report_path}")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()