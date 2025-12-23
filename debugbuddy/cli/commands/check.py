import click
from rich.console import Console
from rich.table import Table
from debugbuddy.core.parsers import ErrorParser
from debugbuddy.core.explainer import ErrorExplainer
from debugbuddy.monitoring.checker import SimpleChecker
from debugbuddy.storage.config import ConfigManager

console = Console()

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def check(file_path):
    config_mgr = ConfigManager()
    parser = ErrorParser()
    explainer = ErrorExplainer()

    all_errors = _detect_all_errors(file_path) 

    if not all_errors:
        console.print("[green]No errors found![/green]")
        return

    table = Table()