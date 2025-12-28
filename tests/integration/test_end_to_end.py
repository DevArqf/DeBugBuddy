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
        f.write("def test():\n")
        f.write("print('missing indent')\n")
        f.flush()
        file_path = Path(f.name)
    yield file_path
    if file_path.exists():
        file_path.unlink()

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
        
        print(f"DEBUG - Parsed result: {parsed}")
        
        assert parsed is not None, "Parser returned None"
        assert parsed['type'] == 'Name Error', f"Expected 'Name Error' but got '{parsed['type']}'"

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
            "TypeError: unsupported operand",
            "IndexError: list index out of range",
            "KeyError: 'missing_key'"
        ]

        parser = ErrorParser()
        explainer = ErrorExplainer()

        for error_text in errors:
            parsed = parser.parse(error_text)
            print(f"DEBUG - Parsing '{error_text}' -> Type: {parsed.get('type')}")
            explanation = explainer.explain(parsed)
            clean_history.add(parsed, explanation)

        recent = clean_history.get_recent(limit=10)
        assert len(recent) == 4, f"Expected 4 entries, got {len(recent)}"

        stats = clean_history.get_stats()
        assert stats['total'] == 4
        assert len(stats['by_type']) >= 2

class TestErrorDetectionPipeline:

    def test_file_check_pipeline(self, temp_error_file):
        from debugbuddy.utils.helpers import detect_all_errors

        with open(temp_error_file, 'r') as f:
            content = f.read()
            print(f"DEBUG - File content: {content}")
    
        errors = detect_all_errors(temp_error_file)
    
        print(f"DEBUG - Detected errors: {errors}")
    
        assert len(errors) > 0, "No errors detected in file with syntax error"
    
        error_texts = [str(e) for e in errors]
    
        has_error = any(
            'error' in e.lower() or 
            'indent' in e.lower() 
            for e in error_texts
        )
        assert has_error, f"Expected to find an error in: {error_texts}"

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
        if len(results) == 0:
            results = clean_history.search('Name Error')
        
        assert len(results) >= 1, "Should find at least one NameError"

        results = clean_history.search('TypeError')
        if len(results) == 0:
            results = clean_history.search('Type Error')
        
        assert len(results) >= 1, "Should find at least one TypeError"

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
        assert similar is not None, "Should find similar error"
        
        assert similar['error_type'] in ['Name Error', 'NameError'], \
            f"Expected 'Name Error' or 'NameError', got '{similar['error_type']}'"

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