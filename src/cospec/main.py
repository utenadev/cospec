import typer
from rich.console import Console

app = typer.Typer(help="cospec: Collaborative Specification CLI")
console = Console()

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

