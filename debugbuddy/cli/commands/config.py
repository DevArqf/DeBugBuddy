import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from ...storage.config import ConfigManager

console = Console()

@click.command()
@click.argument('key', required=False)
@click.argument('value', required=False)
@click.option('--show', is_flag=True)
@click.option('--reset', is_flag=True)
def config(key, value, show, reset):
    config_mgr = ConfigManager()
    # Implement as in current config command