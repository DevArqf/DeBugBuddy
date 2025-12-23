import pytest
import tempfile
from pathlib import Path
from click.testing import CliRunner
from debugbuddy.cli import main
from debugbuddy.core.parsers import ErrorParser
from debugbuddy.core.explainer import ErrorExplainer
from debugbuddy.storage.history import HistoryManager
from debugbuddy.storage.config import ConfigManager

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def temp_error_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        return Path(f.name)

@pytest.fixture
def clean_history():
    history = HistoryManager()
    history.clear()
    yield history
    history.clear()

class TestCompleteWorkflow:

    def test_parse_explain_save_workflow(self, clean_history):
        error_text = "NameError: name 'x' is not defined"

        parser = ErrorParser()
        parsed = parser.parse(error_text)
        assert parsed is not None
        assert parsed['type'] == 'Name Error'

        explainer = ErrorExplainer()
        explanation = explainer.explain(parsed)
        assert 'simple' in explanation
        assert 'fix' in explanation

        clean_history.add(parsed, explanation)

        recent = clean_history.get_recent(limit=1)
        assert len(recent) == 1
        assert recent[0]['error_type'] == 'Name Error'

    def test_multiple_errors_workflow(self, clean_history):
        errors = [
            "NameError: name 'x' is not defined",
            "TypeError: unsupported operand type(s) for +",
            "IndexError: list index out of range",
            "KeyError: 'missing_key'"
        ]

        parser = ErrorParser()
        explainer = ErrorExplainer()

        for error_text in errors:
            parsed = parser.parse(error_text)
            explanation = explainer.explain(parsed)
            clean_history.add(parsed, explanation)

        recent = clean_history.get_recent(limit=10)
        assert len(recent) == 4

        stats = clean_history.get_stats()
        assert stats['total'] == 4
        assert len(stats['by_type']) == 4

class TestCLICommands:

    def test_explain_command_direct(self, runner):
        result = runner.invoke(main, ['explain', 'NameError: name x is not defined'])

        assert result.exit_code == 0
        assert 'NameError' in result.output or 'Error' in result.output

    def test_explain_command_stdin(self, runner):
        error_input = "TypeError: cannot concatenate str and int"
        result = runner.invoke(main, ['explain'], input=error_input)

        assert result.exit_code == 0

    def test_history_command(self, runner, clean_history):
        parser = ErrorParser()
        explainer = ErrorExplainer()

        error = "NameError: test error"
        parsed = parser.parse(error)
        explanation = explainer.explain(parsed)
        clean_history.add(parsed, explanation)

        result = runner.invoke(main, ['history'])
        assert result.exit_code == 0

    def test_history_stats_command(self, runner, clean_history):
        parser = ErrorParser()
        explainer = ErrorExplainer()

        for i in range(3):
            parsed = parser.parse(f"NameError: error {i}")
            explanation = explainer.explain(parsed)
            clean_history.add(parsed, explanation)

        result = runner.invoke(main, ['history', '--stats'])
        assert result.exit_code == 0
        assert 'Total errors' in result.output or 'total' in result.output.lower()

    def test_config_show_command(self, runner):
        result = runner.invoke(main, ['config', '--show'])

        assert result.exit_code == 0
        assert 'Configuration' in result.output or 'config' in result.output.lower()

    def test_config_set_command(self, runner):
        config = ConfigManager()

        result = runner.invoke(main, ['config', 'test_key', 'test_value'])

        value = config.get('test_key')
        assert value == 'test_value'

class TestErrorDetectionPipeline:

    def test_file_check_pipeline(self, temp_error_file):
        from debugbuddy.utils.helpers import detect_all_errors

        errors = detect_all_errors(temp_error_file)

        assert len(errors) > 0
        assert any('undefined_var' in str(error) for error in errors)

    def test_parse_all_languages(self):
        test_cases = [
            ("NameError: name 'x' is not defined", "python"),
            ("ReferenceError: foo is not defined", "javascript"),
            ("Type error: Cannot find name 'x'", "typescript"),
            ("undefined reference to 'func'", "c"),
            ("Parse error: syntax error", "php")
        ]

        parser = ErrorParser()
        explainer = ErrorExplainer()

        for error_text, expected_lang in test_cases:
            parsed = parser.parse(error_text)
            assert parsed is not None

            explanation = explainer.explain(parsed)
            assert 'simple' in explanation
            assert 'fix' in explanation

class TestSearchAndRetrieve:

    def test_search_history(self, clean_history):
        parser = ErrorParser()
        explainer = ErrorExplainer()

        errors = [
            "NameError: name 'foo' is not defined",
            "TypeError: cannot add int and str",
            "NameError: name 'bar' is not defined"
        ]

        for error in errors:
            parsed = parser.parse(error)
            explanation = explainer.explain(parsed)
            clean_history.add(parsed, explanation)

        results = clean_history.search('NameError')
        assert len(results) == 2

        results = clean_history.search('TypeError')
        assert len(results) == 1

    def test_find_similar_errors(self, clean_history):
        parser = ErrorParser()
        explainer = ErrorExplainer()

        error1 = "NameError: name 'x' is not defined"
        parsed1 = parser.parse(error1)
        explanation1 = explainer.explain(parsed1)
        clean_history.add(parsed1, explanation1)

        error2 = "NameError: name 'y' is not defined"
        parsed2 = parser.parse(error2)

        similar = clean_history.find_similar(parsed2)
        assert similar is not None
        assert similar['error_type'] == 'Name Error'

class TestConfigPersistence:

    def test_config_save_load(self):
        config = ConfigManager()

        config.set('test_option', 'test_value')
        config.set('verbose', True)

        config2 = ConfigManager()

        assert config2.get('test_option') == 'test_value'
        assert config2.get('verbose') is True

    def test_config_reset(self):
        config = ConfigManager()

        config.set('custom_key', 'custom_value')
        assert config.get('custom_key') == 'custom_value'

        config.reset()

        assert config.get('custom_key') is None

        assert config.get('verbose') is not None

class TestMultiLanguageSupport:

    def test_all_parsers(self):
        from debugbuddy.core.parsers import ErrorParser

        parser = ErrorParser()

        assert 'python' in parser.parsers
        assert 'javascript' in parser.parsers
        assert 'typescript' in parser.parsers
        assert 'c' in parser.parsers
        assert 'php' in parser.parsers

    def test_pattern_files_exist(self):
        from pathlib import Path

        pattern_dir = Path(__file__).parent.parent.parent / 'patterns'

        required_patterns = [
            'python.json',
            'javascript.json',
            'typescript.json',
            'c.json',
            'php.json',
            'common.json'
        ]

        for pattern_file in required_patterns:
            file_path = pattern_dir / pattern_file
            assert file_path.exists(), f"Missing pattern file: {pattern_file}"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])