import pytest
from click.testing import CliRunner
from rich.console import Console
from debugbuddy.cli import main

console = Console()

@pytest.mark.integration
class TestCliGithubCommand:

    def test_github_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ['github', '--help'])
        assert result.exit_code == 0
        assert 'github' in result.output.lower()
        assert 'help' in result.output or '--help' in result.output

    def test_github_invalid_subcommand(self):
        runner = CliRunner()
        result = runner.invoke(main, ['github', 'invalid'])
        assert result.exit_code != 0  # should show error or usage

    # placeholder for now as exact functionality may vary.
    def test_github_placeholder(self):
        runner = CliRunner()
        result = runner.invoke(main, ['github'])
        # adjust based on actual behavior
        assert result.exit_code == 0 or 'usage' in result.output.lower()