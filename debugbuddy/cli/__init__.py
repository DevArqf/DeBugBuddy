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

def get_version():
    try:
        from debugbuddy.__version__ import __version__
        return __version__
    except ImportError:
        try:
            from debugbuddy import __version__
            return __version__
        except (ImportError, AttributeError):
            return "0.3.2"

@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, help='Show version')
@click.pass_context
def main(ctx, version):
    """DeBugBuddy - Your terminal's debugging companion"""
    
    if version:
        version_num = get_version()
        console.print(f"\n[bold green]DeBugBuddy[/bold green] v{version_num}")
        console.print("[dim]Your terminal's debugging companion[/dim]\n")
        return
    
    if ctx.invoked_subcommand is None:
        version_num = get_version()
        console.print(f"\n[bold green]DeBugBuddy - Your terminal's debugging companion[/bold green]")
        console.print(f"Version v{version_num}\n")
        console.print("Usage: [cyan]dbug [COMMAND] [OPTIONS][/cyan]\n")
        console.print("Commands:")
        console.print("  [cyan]explain[/cyan]     Explain an error message")
        console.print("  [cyan]predict[/cyan]     Predict errors in a file")
        console.print("  [cyan]watch[/cyan]       Watch files for errors")
        console.print("  [cyan]history[/cyan]     View error history")
        console.print("  [cyan]train[/cyan]       Train custom patterns or ML models")
        console.print("  [cyan]search[/cyan]      Search error patterns")
        console.print("  [cyan]config[/cyan]      Manage configuration")
        console.print("  [cyan]github[/cyan]      GitHub integration")
        console.print("\nOptions:")
        console.print("  [cyan]--version, -v[/cyan]  Show version")
        console.print("  [cyan]--help, -h[/cyan]     Show this message")
        console.print("\nExamples:")
        console.print('  [dim]dbug explain "NameError: name \'x\' is not defined"[/dim]')
        console.print('  [dim]dbug predict script.py[/dim]')
        console.print('  [dim]dbug train --ml[/dim]')
        console.print()

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