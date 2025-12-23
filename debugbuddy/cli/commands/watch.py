import click
from debugbuddy.monitoring.watcher import ErrorWatcher

@click.command()
@click.argument('path', type=click.Path(exists=True), required=False)
def watch(path):
    watcher = ErrorWatcher(path or '.')
    watcher.start()