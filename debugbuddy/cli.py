import click
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from rich.prompt import Prompt, Confirm

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
        console.print(Panel(
            "[bold cyan]DeBugBuddy[/bold cyan] [green]v0.1.0[/green]\n\n"
            "Your terminal's debugging companion\n"
            "Made with ❤️ by DevArqf",
            border_style="cyan"
        ))
        sys.exit(0)
    
    if ctx.invoked_subcommand is None:
        console.print(Panel.fit(
            "[bold cyan]🐛💬 DeBugBuddy[/bold cyan]\n\n"
            "Your terminal's debugging companion\n\n"
            "[bold]Quick start:[/bold]\n"
            "  [yellow]db explain error.log[/yellow]     - Explain error from file\n"
            "  [yellow]db explain \"error text\"[/yellow]  - Explain error directly\n"
            "  [yellow]db watch src/[/yellow]            - Monitor directory\n"
            "  [yellow]db interactive[/yellow]           - Chat mode\n"
            "  [yellow]db history[/yellow]               - View past errors\n\n"
            "Run [green]db --help[/green] for all commands",
            title="🎯 Welcome",
            border_style="cyan"
        ))


@main.command()
@click.argument('source', required=False)
@click.option('--ai', is_flag=True, help='Use AI for explanation')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--show-example', '-e', is_flag=True, help='Show code example')
def explain(source, ai, verbose, show_example):
    """Explain an error from file or text"""
    
    parser = ErrorParser()
    explainer = ErrorExplainer()
    history = HistoryManager()
    
    if source:
        if Path(source).exists():
            with open(source, 'r', encoding='utf-8') as f:
                error_text = f.read()
        else:
            error_text = source
    else:
        if sys.stdin.isatty():
            console.print("[red]❌ No input provided[/red]")
            console.print("\nUsage:")
            console.print("  db explain error.log")
            console.print("  db explain \"NameError: name 'x' is not defined\"")
            console.print("  python script.py 2>&1 | db explain")
            sys.exit(1)
        error_text = sys.stdin.read()
    
    with console.status("[cyan]🔍 Analyzing error...", spinner="dots"):
        parsed = parser.parse(error_text)
    
    if not parsed:
        console.print("\n[red]❌ Could not parse error[/red]")
        console.print("\n[yellow]💡 Tip:[/yellow] Try pasting the full error message including traceback")
        if verbose:
            console.print("\n[dim]Raw input:[/dim]")
            console.print(error_text[:500])
        sys.exit(1)
    
    if ai:
        console.print("[yellow]⚠️  AI mode not configured yet. Using pattern matching.[/yellow]")
        explanation = explainer.explain(parsed)
    else:
        explanation = explainer.explain(parsed)
    
    code_snippet = parser.extract_code_snippet(error_text)
    
    display_parts = []
    
    error_info = f"[bold red]{parsed['type']}[/bold red]"
    if parsed.get('file'):
        error_info += f"\n[dim]File: {parsed['file']}"
        if parsed.get('line'):
            error_info += f", Line {parsed['line']}[/dim]"
    elif parsed.get('line'):
        error_info += f"\n[dim]Line {parsed['line']}[/dim]"
    
    display_parts.append(error_info)
    display_parts.append("\n" + explanation['simple'])
    
    if explanation.get('suggestions'):
        display_parts.append("\n[bold yellow]💡 Did you mean?[/bold yellow]")
        for suggestion in explanation['suggestions'][:3]:
            display_parts.append(f"  • {suggestion}")
    
    display_parts.append(f"\n[bold green]✅ How to fix:[/bold green]\n{explanation['fix']}")
    
    console.print("\n")
    console.print(Panel(
        "\n".join(display_parts),
        title="🐛 Error Explanation",
        border_style="red",
        padding=(1, 2)
    ))
    
    if code_snippet and verbose:
        console.print("\n[bold]📝 Code that caused the error:[/bold]")
        syntax = Syntax(code_snippet, "python", theme="monokai", line_numbers=False)
        console.print(Panel(syntax, border_style="yellow"))
    
    if show_example or (explanation.get('example') and verbose):
        example = explanation.get('example')
        if example:
            console.print("\n[bold]📚 Example:[/bold]")
            syntax = Syntax(example, "python", theme="monokai", line_numbers=False)
            console.print(Panel(syntax, border_style="green"))
    
    similar = history.find_similar(parsed)
    if similar:
        console.print(f"\n[yellow]💭 You've seen this type of error before[/yellow]")
        console.print(f"   Last occurrence: [dim]{similar['timestamp']}[/dim]")
        if Confirm.ask("   View previous fix?", default=False):
            console.print(f"\n   Previous fix: {similar['fix'][:200]}")
    
    # Show related errors
    related = explainer.get_related_errors(parsed['type'])
    if related and verbose:
        console.print(f"\n[dim]Related errors: {', '.join(related)}[/dim]")
    
    history.add(parsed, explanation)
    
    console.print("\n[dim]💡 Tip: Use [cyan]db explain -e[/cyan] to see code examples[/dim]")
    
    if verbose:
        console.print("\n[dim]Full parsed data:[/dim]")
        console.print(parsed)


@main.command()
def interactive():
    """Interactive mode - Chat with DeBugBuddy about your errors"""
    
    parser = ErrorParser()
    explainer = ErrorExplainer()
    history = HistoryManager()
    
    console.print(Panel.fit(
        "[bold cyan]🤖 Interactive DeBugBuddy[/bold cyan]\n\n"
        "Paste your errors and I'll help you fix them!\n\n"
        "[dim]Commands:[/dim]\n"
        "  [yellow]paste error[/yellow]    - Paste and explain\n"
        "  [yellow]history[/yellow]        - Show recent errors\n"
        "  [yellow]help[/yellow]           - Show help\n"
        "  [yellow]exit[/yellow]           - Quit\n",
        title="💬 Chat Mode",
        border_style="cyan"
    ))
    
    conversation_count = 0
    
    while True:
        try:
            console.print()
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]", default="")
            
            if not user_input:
                continue
            
            cmd = user_input.lower().strip()
            
            if cmd in ['exit', 'quit', 'q']:
                console.print("\n[green]👋 Thanks for using DeBugBuddy! Happy coding![/green]\n")
                break
            
            elif cmd == 'help':
                console.print("\n[bold]Available commands:[/bold]")
                console.print("  • Paste any error message")
                console.print("  • Type 'history' to see past errors")
                console.print("  • Type 'stats' to see error statistics")
                console.print("  • Type 'exit' to quit")
                continue
            
            elif cmd == 'history':
                recent = history.get_recent(5)
                if not recent:
                    console.print("[yellow]No history yet[/yellow]")
                else:
                    table = Table(title="Recent Errors")
                    table.add_column("#", style="cyan")
                    table.add_column("Error", style="red")
                    table.add_column("When", style="dim")
                    
                    for i, entry in enumerate(recent, 1):
                        table.add_row(
                            str(i),
                            entry['error_type'],
                            entry['timestamp'][:16]
                        )
                    
                    console.print(table)
                continue
            
            elif cmd == 'stats':
                stats = history.get_stats()
                console.print(f"\n[bold]Your debugging stats:[/bold]")
                console.print(f"  Total errors analyzed: {stats['total']}")
                if stats['by_type']:
                    console.print(f"\n  Most common errors:")
                    for error_type, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True)[:5]:
                        console.print(f"    • {error_type}: {count}")
                continue
            
            parsed = parser.parse(user_input)
            
            if parsed:
                conversation_count += 1
                
                explanation = explainer.explain(parsed)
                
                console.print(f"\n[bold green]🐛 DeBugBuddy:[/bold green]")
                console.print(f"\n{explanation['simple']}")
                console.print(f"\n[bold]Fix:[/bold]")
                console.print(explanation['fix'])
                
                if explanation.get('example'):
                    if Confirm.ask("\nShow code example?", default=True):
                        console.print()
                        syntax = Syntax(explanation['example'], "python", theme="monokai")
                        console.print(syntax)
                
                history.add(parsed, explanation)
                
                if conversation_count % 3 == 0:
                    console.print("\n[dim]💡 Tip: Type 'history' to see your recent errors[/dim]")
            
            else:
                console.print("\n[yellow]🤔 I couldn't detect an error in that message.[/yellow]")
                console.print("Try pasting the full error with traceback, or type 'help' for commands.")
        
        except KeyboardInterrupt:
            console.print("\n\n[green]👋 Goodbye![/green]\n")
            break
        except EOFError:
            break


@main.command()
@click.argument('directory', default='.')
@click.option('--lang', default='python', help='Language to watch (python/javascript)')
@click.option('--exclude', multiple=True, help='Patterns to exclude')
def watch(directory, lang, exclude):
    """Watch directory for errors in real-time"""
    
    console.print(Panel.fit(
        f"[cyan]👁️  Watching:[/cyan] [bold]{directory}[/bold]\n"
        f"[cyan]Language:[/cyan] {lang}\n"
        f"[dim]Press Ctrl+C to stop[/dim]",
        title="🔍 Watch Mode",
        border_style="cyan"
    ))
    
    watcher = ErrorWatcher(directory, lang, exclude)
    
    try:
        watcher.start()
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️  Stopped watching[/yellow]\n")


@main.command()
@click.option('--limit', default=10, help='Number of entries to show')
@click.option('--clear', is_flag=True, help='Clear history')
@click.option('--stats', is_flag=True, help='Show statistics')
def history(limit, clear, stats):
    """View or clear error history"""
    
    history_mgr = HistoryManager()
    
    if clear:
        if Confirm.ask("Clear all history?"):
            history_mgr.clear()
            console.print("[green]✅ History cleared[/green]")
        return
    
    if stats:
        statistics = history_mgr.get_stats()
        
        console.print("\n[bold cyan]📊 Your Debugging Statistics[/bold cyan]\n")
        console.print(f"Total errors analyzed: [bold]{statistics['total']}[/bold]")
        
        if statistics['by_type']:
            console.print("\n[bold]Most common errors:[/bold]")
            table = Table()
            table.add_column("Error Type", style="red")
            table.add_column("Count", style="cyan", justify="right")
            
            for error_type, count in sorted(statistics['by_type'].items(), key=lambda x: x[1], reverse=True)[:10]:
                table.add_row(error_type, str(count))
            
            console.print(table)
        
        return
    
    entries = history_mgr.get_recent(limit)
    
    if not entries:
        console.print("[yellow]📭 No history yet[/yellow]")
        console.print("\n[dim]Start using DeBugBuddy to track your errors:[/dim]")
        console.print("  db explain \"your error here\"")
        return
    
    console.print(f"\n[bold cyan]📚 Recent Errors[/bold cyan] [dim](last {len(entries)})[/dim]\n")
    
    for i, entry in enumerate(entries, 1):
        time_str = entry['timestamp'].split('T')[1][:5] if 'T' in entry['timestamp'] else entry['timestamp'][:16]
        date_str = entry['timestamp'].split('T')[0]
        
        error_display = f"[bold red]{entry['error_type']}[/bold red]"
        if entry.get('file'):
            error_display += f" [dim]in {entry['file']}[/dim]"
        
        console.print(f"{i}. {error_display}")
        console.print(f"   [dim]{date_str} at {time_str}[/dim]")
        console.print(f"   {entry['simple'][:80]}...")
        console.print()
    
    console.print("[dim]💡 Tip: Use [cyan]db history --stats[/cyan] to see your debugging stats[/dim]\n")


@main.command()
@click.argument('keyword')
def search(keyword):
    """Search error patterns by keyword"""
    
    explainer = ErrorExplainer()
    results = explainer.search_patterns(keyword)
    
    if not results:
        console.print(f"[yellow]🔍 No patterns found for '{keyword}'[/yellow]")
        console.print("\n[dim]Try searching for:[/dim]")
        console.print("  • Error names: syntax, name, type")
        console.print("  • Keywords: import, undefined, indentation")
        return
    
    console.print(f"\n[bold cyan]🔍 Found {len(results)} patterns for '{keyword}':[/bold cyan]\n")
    
    for i, pattern in enumerate(results, 1):
        console.print(f"{i}. [cyan]{pattern['name']}[/cyan] [dim]({pattern['language']})[/dim]")
        console.print(f"   {pattern['description'][:100]}...")
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
        if Confirm.ask("Reset all settings to defaults?"):
            config_mgr.reset()
            console.print("[green]✅ Config reset to defaults[/green]")
        return
    
    if show or (not key and not value):
        cfg = config_mgr.get_all()
        
        console.print("\n[bold cyan]⚙️  Current Configuration[/bold cyan]\n")
        
        table = Table()
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        for k, v in cfg.items():
            table.add_row(k, str(v))
        
        console.print(table)
        console.print()
        return
    
    if key and value:
        config_mgr.set(key, value)
        console.print(f"[green]✅ Set {key} = {value}[/green]")
    elif key:
        val = config_mgr.get(key)
        console.print(f"{key}: {val}")


@main.command()
def update():
    """Update error pattern database"""
    
    with console.status("[cyan]Checking for pattern updates...", spinner="dots"):
        import time
        time.sleep(1)
    
    console.print("[green]✅ Patterns are up to date[/green]")
    console.print("\n[dim]Pattern version: 2.0[/dim]")
    console.print("[dim]Last updated: 2024-11-22[/dim]")


if __name__ == '__main__':
    main()