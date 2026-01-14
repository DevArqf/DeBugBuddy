import click
from rich.console import Console
from ...monitoring.watcher import ErrorWatcher
from ...storage.config import ConfigManager
from ...tui.runner import should_use_tui

console = Console()

@click.command()
@click.argument('path', type=click.Path(exists=True), required=False)
def watch(path):
    config_mgr = ConfigManager()

    path = path or '.'

    if should_use_tui():
        from ...tui.watch import run_watch_view
        run_watch_view(path)
        return

    console.print(f"\n[bold green]Watching for errors in: {path}[/bold green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")

    watcher = ErrorWatcher(path)
    watcher.start()
