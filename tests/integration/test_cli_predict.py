import pytest
import tempfile
from pathlib import Path
from click.testing import CliRunner
from debugbuddy.cli import main

@pytest.fixture
def sample_py_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("undefined_var = x\nprint(undefined_var)\n")
    yield Path(f.name)
    Path(f.name).unlink()

@pytest.mark.integration
class TestCliPredictCommand:

    def test_predict_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ['predict', '--help'])
        assert result.exit_code == 0
        assert 'predict' in result.output.lower()

    def test_predict_on_file(self, sample_py_file):
        runner = CliRunner()
        result = runner.invoke(main, ['predict', str(sample_py_file)])
        assert result.exit_code == 0
        assert 'potential issue' in result.output.lower() or 'nameerror' in result.output.lower() or 'no issues' in result.output.lower()

    def test_predict_nonexistent_file(self):
        runner = CliRunner()
        result = runner.invoke(main, ['predict', 'nonexistent.py'])
        assert result.exit_code != 0
        assert 'error' in result.output.lower() or 'not found' in result.output.lower()