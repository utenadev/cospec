import datetime
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from cospec.agents.hearer import HearerAgent
from cospec.agents.reviewer import ReviewerAgent
from cospec.agents.test_generator import TestGeneratorAgent
from cospec.core.config import CospecConfig, ToolConfig


def _analyze_help_output(help_output: str, command: str) -> list[str]:
    """
    Analyze command help output to infer prompt argument structure.

    Returns a list of args for ToolConfig.
    """
    args = []

    if "[prompt]" in help_output or "<prompt>" in help_output or "[PROMPT]" in help_output:
        if "-p" in help_output or "-p, --prompt" in help_output:
            args.append("-p")
        args.append("{prompt}")
    elif "[message]" in help_output or "<message>" in help_output:
        args.append("{prompt}")
    else:
        args.append("{prompt}")

    return args


app = typer.Typer(help="cospec: Collaborative Specification CLI", no_args_is_help=True)
agent_app = typer.Typer(help="Manage AI-Agent configurations", no_args_is_help=True)
app.add_typer(agent_app, name="agent")
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

    console.print("\n[bold green]✅ Required Reading for AI Agents[/bold green]")
    console.print("Before starting any development work in this project, read these 3 guides:")
    console.print("1. [bold].rules/OverviewDesignThinking.md[/bold] - Design philosophy (Why)")
    console.print("2. [bold].rules/OverviewBasicRule.md[/bold] - Practice workflows (How)")
    console.print("3. [bold].rules/OverviewCodingTestingThinking.md[/bold] - Coding principles (What)")
    console.print("\n[italic]These are the sole references for all development decisions.[/italic]")


@app.command()
def status() -> None:
    """
    Show project status and next actions.
    """
    console.print("[bold blue]cospec status[/bold blue]")
    console.print("Current Phase: [green]Inception[/green]")
    console.print("\nNext Action: Update SPEC.md or run 'cospec hear'")


@app.command()
def review(tool: Optional[str] = typer.Option(None, help="Tool to use (qwen, opencode)")) -> None:
    """
    Review codebase against documentation using an AI agent.
    """
    console.print("[bold blue]Reviewing project...[/bold blue]")

    try:
        # 1. Load Config
        config = CospecConfig.load_config()

        # 2. Determine tools to use
        if tool:
            tools_to_use = [tool]
        else:
            tools_to_use = config.select_review_tools()
            if len(tools_to_use) > 1:
                console.print(f"[yellow]Using {len(tools_to_use)} different tools for diverse review[/yellow]")
            else:
                console.print("[yellow]Only 1 tool available for review[/yellow]")

        # 3. Run reviews
        reports = []
        for tool_name in tools_to_use:
            console.print(f"Running {tool_name} (Language: {config.language})...")
            agent = ReviewerAgent(config, tool_name=tool_name)
            report_content = agent.review_project()

            date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = Path(f"docs/review_{date_str}_{tool_name}.md")
            report_path.write_text(report_content, encoding="utf-8")
            reports.append((tool_name, report_path))
            console.print(f"[green]Review with {tool_name} complete![/green] Report saved to: {report_path}\n")

        # 4. Summary
        console.print("[bold blue]Review Summary:[/bold blue]")
        for tool_name, report_path in reports:
            console.print(f"  • {tool_name}: {report_path}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1) from e


@app.command()
def hear(output: Optional[Path] = None) -> None:
    """
    Generate a mission prompt for an AI agent to conduct a hearing.

    This command outputs a system prompt that you can feed to an AI agent (like Gemini, Claude).
    The agent will then interactively help you clarify ambiguous requirements in SPEC.md
    by reading the file and asking you questions with options (Pros/Cons).
    """
    console.print("[bold blue]Generating mission prompt for AI Agent...[/bold blue]")

    try:
        # 1. Load Config
        config = CospecConfig.load_config()

        # 2. Initialize Agent (Tool name is irrelevant for prompt generation)
        agent = HearerAgent(config)

        # 3. Generate Prompt
        prompt = agent.create_mission_prompt()

        if prompt.startswith("Error:"):
            console.print(f"[red]{prompt}[/red]")
            raise typer.Exit(code=1)

        # 4. Output Result
        if output:
            output.write_text(prompt, encoding="utf-8")
            console.print(f"[green]Mission prompt saved to:[/green] {output}")
        else:
            console.print("\n[bold]--- Mission Prompt (Copy & Paste to AI Agent) ---[/bold]\n")
            print(prompt)
            console.print("\n[bold]--------------------------------------------------[/bold]")
            console.print("[italic]Tip: Paste this prompt to your AI assistant to start the hearing session.[/italic]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1) from e


@app.command()
def test_gen(tool: Optional[str] = None, output: Optional[Path] = None, validate: bool = False) -> None:
    """
    Generate test cases from specifications (Test-Driven Generation).
    """
    console.print("[bold blue]Generating test cases from specifications...[/bold blue]")

    try:
        # 1. Load Config
        config = CospecConfig.load_config()

        # 2. Select tool
        tool_name = tool or config.select_tool_for_development()

        # 3. Initialize Agent
        agent = TestGeneratorAgent(config, tool_name=tool_name)

        console.print(f"Running {agent.tool_name} (Language: {config.language})...")

        # 2. Generate Tests
        result = agent.generate_tests(output_dir=output if output else Path("tests/generated/"))

        if result["status"] == "error":
            console.print(f"[red]Error:[/red] {result['message']}")
            raise typer.Exit(code=1)

        # 3. Display Results
        console.print("[green]Test generation complete![/green]")
        console.print(result["message"])

        # 4. Display generated scenarios
        if result["scenarios"]:
            console.print(f"\n[bold]Generated {len(result['scenarios'])} test scenarios:[/bold]")
            for i, scenario in enumerate(result["scenarios"], 1):
                console.print(f"  {i}. [{scenario['priority']}] {scenario['description']}")

        # 5. Display generated test files
        if result["test_files"]:
            console.print(f"\n[bold]Generated {len(result['test_files'])} test files:[/bold]")
            for filename in result["test_files"].keys():
                console.print(f"  • {filename}")

        # 6. Validate generated files if requested
        if validate and result["test_files"]:
            console.print("\n[bold]Validating generated test files...[/bold]")
            for filename, content in result["test_files"].items():
                if "import pytest" in content and "def test_" in content:
                    console.print(f"  ✓ {filename} - Valid pytest format")
                else:
                    console.print(f"  ✗ {filename} - Invalid format")

        # 7. Save results summary
        if output:
            summary_file = output / "test_generation_summary.txt"
            summary_content = f"""Test Generation Summary
Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Scenarios: {len(result["scenarios"])}
Test Files: {len(result["test_files"])}
Output Directory: {result["output_dir"]}

Scenarios:
{chr(10).join([f"- [{s['priority']}] {s['description']}" for s in result["scenarios"]])}
"""
            summary_file.write_text(summary_content, encoding="utf-8")
            console.print(f"\n[green]Summary saved to:[/green] {summary_file}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1) from e


@agent_app.command()
def add(
    name: str,
    command: str = typer.Option(..., help="Command name to execute"),
    help_flag: str = typer.Option("--help", help="Help flag to use for analysis"),
) -> None:
    """
    Add a new AI-Agent configuration.

    Analyzes the command's help output to infer prompt argument structure.
    """
    console.print(f"[bold blue]Adding AI-Agent '{name}'...[/bold blue]")

    try:
        config = CospecConfig.load_config()

        if name in config.tools:
            console.print(f"[yellow]Warning:[/yellow] Agent '{name}' already exists. Overwriting...")

        console.print(f"Analyzing command: {command} {help_flag}")

        try:
            result = subprocess.run([command, help_flag], capture_output=True, text=True, check=True)
            help_output = result.stdout + result.stderr
        except subprocess.CalledProcessError as e:
            help_output = e.stdout + e.stderr
            if not help_output:
                console.print(f"[red]Error:[/red] Command '{command}' failed to execute or has no --help option")
                raise typer.Exit(code=1) from None
        except FileNotFoundError:
            console.print(f"[red]Error:[/red] Command '{command}' not found in PATH")
            raise typer.Exit(code=1) from None

        console.print("[green]Command help output analyzed successfully[/green]")

        args = _analyze_help_output(help_output, command)
        console.print(f"Inferred args: {args}")

        tool_config = ToolConfig(command=command, args=args)
        config.tools[name] = tool_config
        config.save_to_file()

        console.print(f"[green]Success![/green] AI-Agent '{name}' added to configuration")

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1) from e


@agent_app.command(name="list")
def list_agents() -> None:
    """
    List all registered AI-Agents.
    """
    try:
        config = CospecConfig.load_config()
        console.print("[bold blue]Registered AI-Agents:[/bold blue]\n")

        for name, tool_config in config.tools.items():
            console.print(f"[bold]{name}[/bold]")
            console.print(f"  Command: {tool_config.command}")
            console.print(f"  Args: {' '.join(tool_config.args)}")
            console.print()

        if not config.tools:
            console.print("[yellow]No AI-Agents registered[/yellow]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1) from e


@agent_app.command()
def test(name: str) -> None:
    """
    Test a registered AI-Agent with a simple prompt.
    """
    console.print(f"[bold blue]Testing AI-Agent '{name}'...[/bold blue]")

    try:
        config = CospecConfig.load_config()

        if name not in config.tools:
            console.print(f"[red]Error:[/red] Agent '{name}' not found")
            console.print("Use 'cospec agent list' to see available agents")
            raise typer.Exit(code=1)

        tool_config = config.tools[name]
        console.print(f"Running: {tool_config.command} {' '.join(tool_config.args)}")

        test_prompt = "Hello! This is a test prompt."

        cmd_args = [tool_config.command]
        for arg in tool_config.args:
            if "{prompt}" in arg:
                cmd_args.append(arg.replace("{prompt}", test_prompt))
            else:
                cmd_args.append(arg)

        try:
            result = subprocess.run(cmd_args, capture_output=True, text=True, check=True)
            console.print("[green]Success![/green] Agent responded:")
            console.print(result.stdout)
            if result.stderr:
                console.print(f"[yellow]Warnings:[/yellow] {result.stderr}")
        except subprocess.CalledProcessError as e:
            console.print("[red]Error:[/red] Agent execution failed")
            console.print(f"Output: {e.stdout}")
            console.print(f"Error: {e.stderr}")
            raise typer.Exit(code=1) from None
        except FileNotFoundError:
            console.print(f"[red]Error:[/red] Command '{tool_config.command}' not found in PATH")
            raise typer.Exit(code=1) from None

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
