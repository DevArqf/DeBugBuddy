import pytest
import tempfile
import json
from pathlib import Path
from click.testing import CliRunner
from debugbuddy.cli import main

@pytest.fixture
def training_data_file():
    data = {
        "examples": [
            {"error": "NameError: name 'x' is not defined", "explanation": "Variable not defined", "fix": "Define x"}
        ]
    }
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
    yield Path(f.name)
    Path(f.name).unlink()

@pytest.mark.integration
class TestCliTrainCommand:

    def test_train_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ['train', '--help'])
        assert result.exit_code == 0
        assert 'train' in result.output.lower()

    def test_train_with_interactive_flag(self):
        runner = CliRunner()
        result = runner.invoke(main, ['train', '--interactive', '--language', 'python'], 
                              input='done\n')
        assert 'train' in result.output.lower() or 'example' in result.output.lower()

    def test_train_list_custom_patterns(self):
        """Test listing custom patterns"""
        runner = CliRunner()
        result = runner.invoke(main, ['train'])
        assert result.exit_code == 0