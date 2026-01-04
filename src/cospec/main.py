import typer
from rich.console import Console
from pathlib import Path
import subprocess
import datetime
from cospec.core.analyzer import ProjectAnalyzer
from cospec.core.config import load_config

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

@app.command()
def review(tool: str = typer.Option(None, help="Tool to use (qwen, opencode)")) -> None:
    """
    Review the codebase against the documentation using an AI agent.
    """
    console.print("[bold blue]Reviewing project...[/bold blue]")
    
    # 1. Load Config & Select Tool
    config = load_config()
    tool_name = tool or config.default_tool
    if tool_name not in config.tools:
        console.print(f"[red]Error: Tool '{tool_name}' not configured.[/red]")
        raise typer.Exit(code=1)
    
    tool_config = config.tools[tool_name]
    
    # 2. Gather Context
    analyzer = ProjectAnalyzer()
    context = analyzer.collect_context()
    
    system_prompt = (
        "You are a strict code reviewer. Compare the documentation and code provided below.\n"
        "Identify inconsistencies, missing features, and guideline violations.\n"
        "Output a Markdown report.\n\n"
        "--- Context ---\n"
    )
    full_prompt = system_prompt + context
    
    # 3. Construct Command
    # Replace {prompt} in args
    cmd_args = [tool_config.command]
    for arg in tool_config.args:
        if "{prompt}" in arg:
            cmd_args.append(arg.replace("{prompt}", full_prompt))
        else:
            cmd_args.append(arg)
            
    # 4. Execute Tool
    console.print(f"Running {tool_name}...")
    try:
        result = subprocess.run(cmd_args, capture_output=True, text=True, check=True)
        report_content = result.stdout
        
        # 5. Save Report
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(f"docs/review_{date_str}_{tool_name}.md")
        report_path.write_text(report_content, encoding="utf-8")
        
        console.print(f"[green]Review complete![/green] Report saved to: {report_path}")
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error running tool:[/red] {e.stderr}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

