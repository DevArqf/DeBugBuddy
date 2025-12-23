import click
import sys
from rich.console import Console
from rich.panel import Panel
from debugbuddy.core.parsers import ErrorParser
from debugbuddy.integrations.ai import get_provider
from debugbuddy.storage.config import ConfigManager
from debugbuddy.storage.history import HistoryManager
from debugbuddy.core.explainer import ErrorExplainer

console = Console()

@click.command()
@click.argument('error_input', required=False)
@click.option('--file', '-f', is_flag=True, help='Treat input as file path')
@click.option('--ai', is_flag=True, help='Use AI for explanation')
@click.option('--language', '-l', type=str, help='Specify language')
def explain(error_input, file, ai, language):
    config_mgr = ConfigManager()
    parser = ErrorParser()
    explainer = ErrorExplainer()
    history = HistoryManager()

    if not error_input:
        error_input = sys.stdin.read().strip()

    if file:
        with open(error_input, 'r') as f:
            error_text = f.read().strip()
    else:
        error_text = error_input

    parsed = parser.parse(error_text, language=language)

    if not parsed:
        console.print("[yellow]Couldn't parse the error[/yellow]")
        return

    explanation = explainer.explain(parsed)

    if ai:
        provider_name = config_mgr.get('ai_provider', 'openai')
        provider = get_provider(provider_name, config_mgr.get_all())
        if provider:
            ai_explain = provider.explain_error(error_text, parsed.get('language', 'code'))
            explanation['ai'] = ai_explain

    history.add(parsed, explanation)

    title = f"DeBugBuddy {parsed['type']}"
    content = f"Error: {explanation['simple']}\n\nFix:\n{explanation['fix']}"
    console.print(Panel(content, title=title, expand=False))

    similar = history.find_similar(parsed)
    if similar:
        console.print("\n[dim]Similar error seen before:[/dim]")
        console.print(f"[dim]{similar['timestamp']}: {similar['error_type']} - {similar['simple']}[/dim]")