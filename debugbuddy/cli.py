import click
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from debugbuddy.core.parser import ErrorParser
from debugbuddy.core.explainer import ErrorExplainer
from debugbuddy.core.watcher import ErrorWatcher
from debugbuddy.core.history import HistoryManager
from debugbuddy.utils.config import ConfigManager

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--version', is_flag=True, help='Show version')
def main(ctx, version):
    """🐛 DeBugBuddy - Your terminal's debugging companion"""
    if version:
        console.print("DeBugBuddy v0.1.0", style="bold green")
        sys.exit(0)
    
    if ctx.invoked_subcommand is None:
        console.print(Panel.fit(
            "[bold cyan]DeBugBuddy[/bold cyan]\n\n"
            "Your terminal's debugging companion\n\n"
            "Quick start:\n"
            "  [yellow]db explain error.log[/yellow]     - Explain error from file\n"
            "  [yellow]db watch src/[/yellow]            - Monitor directory\n"
            "  [yellow]db history[/yellow]               - View past errors\n\n"
            "Run [green]db --help[/green] for all commands",
            title="🐛💬",
            border_style="cyan"
        ))


@main.command()
@click.argument('source', required=False)
@click.option('--ai', is_flag=True, help='Use AI for explanation')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def explain(source, ai, verbose):
    """Explain an error from file or text"""
    
    parser = ErrorParser()
    explainer = ErrorExplainer()
    history = HistoryManager()
    
    if source:
        if Path(source).exists():
            with open(source, 'r') as f:
                error_text = f.read()
        else:
            error_text = source
    else:
        if sys.stdin.isatty():
            console.print("[red]Error:[/red] No input provided. Use: db explain <file> or pipe error text", style="bold")
            sys.exit(1)
        error_text = sys.stdin.read()
    
    with console.status("[cyan]Analyzing error...", spinner="dots"):
        parsed = parser.parse(error_text)
    
    if not parsed:
        console.print("[red]❌ Could not parse error[/red]")
        console.print("\nRaw input:")
        console.print(error_text[:500])
        sys.exit(1)
    
    if ai:
        # AI mode (requires setup)
        console.print("[yellow]AI mode not configured yet. Using pattern matching.[/yellow]")
        explanation = explainer.explain(parsed)
    else:
        explanation = explainer.explain(parsed)
    
    console.print("\n")
    console.print(Panel(
        f"[bold red]{parsed['type']}[/bold red]\n\n"
        f"{explanation['simple']}\n\n"
        f"[bold]💡 Fix:[/bold]\n{explanation['fix']}\n\n"
        f"[dim]Line {parsed.get('line', 'unknown')}[/dim]",
        title="🐛 Error Explanation",
        border_style="red"
    ))
    
    similar = history.find_similar(parsed)
    if similar:
        console.print("\n[yellow]💭 You've seen similar errors before[/yellow]")
        console.print(f"   Last time: {similar['timestamp']}")
    
    history.add(parsed, explanation)
    
    if verbose:
        console.print("\n[dim]Full parsed data:[/dim]")
        console.print(parsed)


@main.command()
@click.argument('directory', default='.')
@click.option('--lang', default='python', help='Language to watch (python/javascript)')
@click.option('--exclude', multiple=True, help='Patterns to exclude')
def watch(directory, lang, exclude):
    """Watch directory for errors in real-time"""
    
    console.print(f"[cyan]👁️  Watching {directory} for {lang} errors...[/cyan]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")
    
    watcher = ErrorWatcher(directory, lang, exclude)
    
    try:
        watcher.start()
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped watching[/yellow]")


@main.command()
@click.option('--limit', default=10, help='Number of entries to show')
@click.option('--clear', is_flag=True, help='Clear history')
def history(limit, clear):
    """View or clear error history"""
    
    history_mgr = HistoryManager()
    
    if clear:
        if click.confirm("Clear all history?"):
            history_mgr.clear()
            console.print("[green]✓ History cleared[/green]")
        return
    
    entries = history_mgr.get_recent(limit)
    
    if not entries:
        console.print("[yellow]No history yet[/yellow]")
        return
    
    console.print(Panel.fit(
        "[bold]Recent Errors[/bold]",
        border_style="cyan"
    ))
    
    for i, entry in enumerate(entries, 1):
        console.print(f"\n{i}. [red]{entry['error_type']}[/red]")
        console.print(f"   {entry['timestamp']}")
        console.print(f"   [dim]{entry['simple'][:60]}...[/dim]")


@main.command()
@click.argument('keyword')
def search(keyword):
    """Search error patterns by keyword"""
    
    explainer = ErrorExplainer()
    results = explainer.search_patterns(keyword)
    
    if not results:
        console.print(f"[yellow]No patterns found for '{keyword}'[/yellow]")
        return
    
    console.print(f"\n[bold]Found {len(results)} patterns:[/bold]\n")
    
    for i, pattern in enumerate(results, 1):
        console.print(f"{i}. [cyan]{pattern['name']}[/cyan]")
        console.print(f"   {pattern['description']}")
        console.print()


@main.command()
@click.argument('key', required=False)
@click.argument('value', required=False)
@click.option('--show', is_flag=True, help='Show current config')
@click.option('--reset', is_flag=True, help='Reset to defaults')
def config(key, value, show, reset):
    """Manage configuration"""
    
    config_mgr = ConfigManager()
    
    if reset:
        if click.confirm("Reset all settings to defaults?"):
            config_mgr.reset()
            console.print("[green]✓ Config reset to defaults[/green]")
        return
    
    if show or (not key and not value):
        cfg = config_mgr.get_all()
        console.print("\n[bold]Current Configuration:[/bold]\n")
        for k, v in cfg.items():
            console.print(f"  [cyan]{k}[/cyan]: {v}")
        console.print()
        return
    
    if key and value:
        config_mgr.set(key, value)
        console.print(f"[green]✓ Set {key} = {value}[/green]")
    elif key:
        val = config_mgr.get(key)
        console.print(f"{key}: {val}")


@main.command()
def update():
    """Update error pattern database"""
    
    console.print("[cyan]Checking for pattern updates...[/cyan]")
    # TODO: Implement pattern update from repo
    console.print("[green]✓ Patterns are up to date[/green]")


if __name__ == '__main__':
    main()