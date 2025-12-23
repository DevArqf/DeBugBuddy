import click
from .commands.explain import explain
from .commands.watch import watch
from .commands.check import check
from .commands.history import history
from .commands.search import search
from .commands.config import config
from .commands.predict import predict
from .commands.train import train
from .commands.github import github

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        from rich.console import Console
        console = Console()
        console.print("\n[bold green]DeBugBuddy - Your terminal's debugging companion[/bold green]")
        console.print("Version v0.3.2\n")
        ctx.invoke(explain)