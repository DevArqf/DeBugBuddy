import click
from rich.console import Console
from rich.prompt import Confirm
from ...storage.history import HistoryManager
from ...tui.runner import should_use_tui

console = Console()

@click.command()
@click.option('--clear', is_flag=True, help='Clear history')
@click.option('--stats', is_flag=True, help='Show statistics')
@click.option('--search', type=str, help='Search history')
def history(clear, stats, search):
    history_mgr = HistoryManager()

    if clear:
        if Confirm.ask("Clear all history?"):
            history_mgr.clear()
            console.print("[green]History cleared[/green]")
        return

    if stats:
        stats_data = history_mgr.get_stats()
        if should_use_tui():
            from ...tui.views import run_history_stats_view
            run_history_stats_view(stats_data)
            return
        console.print("\n[bold green]Error Statistics[/bold green]\n")
        console.print(f"Total errors: {stats_data['total']}\n")

        console.print("[cyan]By Type:[/cyan]")
        for typ, count in sorted(stats_data['by_type'].items(), key=lambda x: x[1], reverse=True):
            console.print(f"  - {typ}: {count}")

        console.print("\n[cyan]By Language:[/cyan]")
        for lang, count in sorted(stats_data['by_language'].items(), key=lambda x: x[1], reverse=True):
            console.print(f"  - {lang}: {count}")

        if stats_data.get('by_file'):
            console.print("\n[cyan]Top Files:[/cyan]")
            for file, count in stats_data['by_file'].items():
                console.print(f"  - {file}: {count}")

        if stats_data.get('recent_days'):
            console.print("\n[cyan]Last 7 Days:[/cyan]")
            for day, count in stats_data['recent_days']:
                console.print(f"  - {day}: {count}")
        return

    if search:
        results = history_mgr.search(search)
        if not results:
            console.print(f"[yellow]No history found for '{search}'[/yellow]")
            return
        if should_use_tui():
            from ...tui.views import run_history_entries_view
            run_history_entries_view(results, f"Search: {search}")
            return

        console.print(f"\n[bold green]Search Results for '{search}':[/bold green]\n")
        for entry in results:
            console.print(f"[dim]{entry['timestamp']}[/dim]")
            console.print(f"[red]{entry['error_type']}[/red]: {entry['message']}")
            if entry['file']:
                console.print(f"[dim]File: {entry['file']}, Line {entry['line']}[/dim]")
            console.print(f"Fix: {entry['simple']}")
            console.print()
        return

    recent = history_mgr.get_recent()
    if not recent:
        console.print("[yellow]No history yet[/yellow]")
        return
    if should_use_tui():
        from ...tui.views import run_history_entries_view
        run_history_entries_view(recent, "Recent errors")
        return

    console.print("\n[bold green]Recent Errors[/bold green]\n")
    for entry in recent:
        console.print(f"[dim]{entry['timestamp']}[/dim]")
        console.print(f"[red]{entry['error_type']}[/red]: {entry['message']}")
        if entry['file']:
            console.print(f"[dim]File: {entry['file']}, Line {entry['line']}[/dim]")
        console.print(f"Fix: {entry['simple']}")
        console.print()
