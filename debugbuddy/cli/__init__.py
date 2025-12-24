import click
from rich.console import Console
from .commands.explain import explain
from .commands.watch import watch
from .commands.history import history
from .commands.search import search
from .commands.config import config
from .commands.predict import predict
from .commands.train import train
from .commands.github import github

console = Console()

@click.group()
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        console.print("\n[bold green]🐛 DeBugBuddy - Your terminal's debugging companion[/bold green]")
        console.print("Version v0.3.2\n")
        console.print("Use 'dbug --help' for available commands\n")

main.add_command(explain)
main.add_command(watch)
main.add_command(history)
main.add_command(search)
main.add_command(config)
main.add_command(predict)
main.add_command(train)
main.add_command(github)

if __name__ == "__main__":
    main()