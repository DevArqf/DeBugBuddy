import click
from rich.console import Console
from rich.table import Table
from ...integrations.github.client import GitHubClient
from ...integrations.github.search import GitHubSearcher
from ...storage.config import ConfigManager
from ...tui.runner import should_use_tui

console = Console()

@click.group()
def github():
    pass

@github.command()
@click.argument('error_text')
@click.option('--language', '-l', type=str, default='python')
@click.option('--repo', '-r', type=str, help='Limit search to a repo (owner/name)')
@click.option('--exact/--loose', default=True, help='Use exact phrase matching')
@click.option('--include-closed', is_flag=True, help='Include closed issues if no open results')
def search(error_text, language, repo, exact, include_closed):
    config = ConfigManager()
    token = config.get('github_token')

    client = GitHubClient(token)
    searcher = GitHubSearcher(client)

    console.print("\n[bold cyan]Searching GitHub...[/bold cyan]\n")

    solutions = searcher.find_solutions(
        error_text,
        language,
        repo=repo,
        exact=exact,
        include_closed=include_closed,
    )

    if not solutions:
        console.print("[yellow]No solutions found[/yellow]")
        return

    if should_use_tui():
        from ...tui.views import run_github_search_view
        run_github_search_view(solutions)
        return

    table = Table(title="GitHub Solutions")
    table.add_column("Title", style="cyan")
    table.add_column("State", style="green")
    table.add_column("Reactions", style="yellow")
    table.add_column("Comments", style="blue")

    for sol in solutions:
        table.add_row(
            sol['title'][:50] + "..." if len(sol['title']) > 50 else sol['title'],
            sol['state'],
            str(sol['reactions']),
            str(sol['comments'])
        )

    console.print(table)

    console.print("\n[dim]URLs:[/dim]")
    for i, sol in enumerate(solutions, 1):
        console.print(f"  {i}. {sol['url']}")

@github.command()
@click.argument('error_text')
@click.option('--repo', '-r', type=str, required=True)
def report(error_text, repo):
    config = ConfigManager()
    token = config.get('github_token')

    if not token:
        console.print("[red]GitHub token not configured[/red]")
        console.print("[dim]Set with: dbug config github_token YOUR_TOKEN[/dim]")
        return

    client = GitHubClient(token)

    title = f"[DeBugBuddy] {error_text[:50]}"
    body = f"Error reported via DeBugBuddy:\n\n```\n{error_text}\n```"

    issue = client.create_issue(repo, title, body, labels=['bug', 'debugbuddy'])

    if should_use_tui():
        from ...tui.views import run_github_report_view
        run_github_report_view(issue)
        return

    console.print(f"\n[green]Issue created: {issue['html_url']}[/green]")
