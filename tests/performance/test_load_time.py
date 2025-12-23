import pytest
import time
import json
from pathlib import Path

class TestLoadTime:

    def test_import_speed(self):
        start = time.time()

        from debugbuddy.core.parsers import ErrorParser
        from debugbuddy.core.explainer import ErrorExplainer
        from debugbuddy.storage.history import HistoryManager

        end = time.time()
        load_time = end - start

        assert load_time < 1.0, f"Import took {load_time:.2f}s, expected < 1.0s"

    def test_parser_initialization(self):
        from debugbuddy.core.parsers import ErrorParser

        start = time.time()
        parser = ErrorParser()
        end = time.time()

        init_time = end - start
        assert init_time < 0.5, f"Parser init took {init_time:.2f}s"

    def test_explainer_initialization(self):
        from debugbuddy.core.explainer import ErrorExplainer

        start = time.time()
        explainer = ErrorExplainer()
        end = time.time()

        init_time = end - start
        assert init_time < 2.0, f"Explainer init took {init_time:.2f}s"

    def test_history_manager_initialization(self):
        from debugbuddy.storage.history import HistoryManager

        start = time.time()
        history = HistoryManager()
        end = time.time()

        init_time = end - start
        assert init_time < 0.5, f"History init took {init_time:.2f}s"

    def test_cli_startup_time(self):
        from click.testing import CliRunner
        from debugbuddy.cli import main

        runner = CliRunner()

        start = time.time()
        result = runner.invoke(main, ['--help'])
        end = time.time()

        startup_time = end - start
        assert result.exit_code == 0
        assert startup_time < 2.0, f"CLI startup took {startup_time:.2f}s"


class TestPatternLoadPerformance:

    def test_single_pattern_load(self):
        pattern_dir = Path(__file__).parent.parent.parent / 'patterns'
        python_patterns = pattern_dir / 'python.json'

        start = time.time()
        with open(python_patterns, 'r', encoding='utf-8') as f:
            data = json.load(f)
        end = time.time()

        load_time = end - start
        assert load_time < 0.1, f"Pattern load took {load_time:.4f}s"
        assert 'errors' in data

    def test_all_patterns_load(self):
        from debugbuddy.core.explainer import ErrorExplainer

        start = time.time()
        explainer = ErrorExplainer()
        end = time.time()

        load_time = end - start
        assert load_time < 2.0
        assert len(explainer.patterns) > 0

class TestPatternLoadPerformance:

    def test_single_pattern_load(self):
        import json

        pattern_dir = Path(__file__).parent.parent.parent / 'patterns'
        python_patterns = pattern_dir / 'python.json'

        start = time.time()
        with open(python_patterns, 'r') as f:
            data = json.load(f)
        end = time.time()

        load_time = end - start
        assert load_time < 0.1, f"Pattern load took {load_time:.4f}s"
        assert 'errors' in data

    def test_all_patterns_load(self):
        from debugbuddy.core.explainer import ErrorExplainer

        start = time.time()
        explainer = ErrorExplainer()
        end = time.time()

        load_time = end - start
        assert load_time < 2.0
        assert len(explainer.patterns) > 0

import pytest
import sys
from debugbuddy.core.parsers import ErrorParser
from debugbuddy.core.explainer import ErrorExplainer
from debugbuddy.storage.history import HistoryManager

def get_size(obj, seen=None):
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    seen.add(obj_id)

    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])

    return size

class TestMemoryUsage:

    def test_parser_memory(self):
        parser = ErrorParser()

        size_bytes = get_size(parser)
        size_mb = size_bytes / (1024 * 1024)

        assert size_mb < 1.0, f"Parser uses {size_mb:.2f}MB"

    def test_explainer_memory(self):
        explainer = ErrorExplainer()

        size_bytes = get_size(explainer)
        size_mb = size_bytes / (1024 * 1024)

        assert size_mb < 5.0, f"Explainer uses {size_mb:.2f}MB"

    def test_history_memory_empty(self):
        history = HistoryManager()
        history.clear()

        size_bytes = get_size(history)
        size_mb = size_bytes / (1024 * 1024)

        assert size_mb < 1.0, f"Empty history uses {size_mb:.2f}MB"

    def test_history_memory_with_data(self):
        from debugbuddy.core.parsers import ErrorParser
        from debugbuddy.core.explainer import ErrorExplainer

        parser = ErrorParser()
        explainer = ErrorExplainer()
        history = HistoryManager()
        history.clear()

        for i in range(100):
            error = f"NameError: name 'var{i}' is not defined"
            parsed = parser.parse(error)
            explanation = explainer.explain(parsed)
            history.add(parsed, explanation)

        size_bytes = get_size(history)
        size_mb = size_bytes / (1024 * 1024)

        assert size_mb < 10.0, f"History with 100 entries uses {size_mb:.2f}MB"

    def test_pattern_memory(self):
        from debugbuddy.core.explainer import ErrorExplainer

        explainer = ErrorExplainer()

        patterns_size = get_size(explainer.patterns)
        patterns_mb = patterns_size / (1024 * 1024)

        assert patterns_mb < 3.0, f"Patterns use {patterns_mb:.2f}MB"

import pytest
import time
import tempfile
from pathlib import Path
from debugbuddy.core.predictor import ErrorPredictor
from debugbuddy.storage.config import ConfigManager

@pytest.fixture
def predictor():
    config = ConfigManager()
    return ErrorPredictor(config)

@pytest.fixture
def test_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        return Path(f.name)

class TestPredictionSpeed:

    def test_single_file_prediction(self, predictor, test_file):
        start = time.time()
        predictions = predictor.predict_file(test_file)
        end = time.time()

        prediction_time = end - start

        assert prediction_time < 1.0, f"Prediction took {prediction_time:.2f}s"

    def test_static_analysis_speed(self, predictor, test_file):
        start = time.time()
        predictions = predictor._analyze_static(test_file)
        end = time.time()

        analysis_time = end - start
        assert analysis_time < 0.5, f"Static analysis took {analysis_time:.2f}s"

    def test_pattern_analysis_speed(self, predictor, test_file):
        start = time.time()
        predictions = predictor._analyze_patterns(test_file)
        end = time.time()

        analysis_time = end - start
        assert analysis_time < 0.5, f"Pattern analysis took {analysis_time:.2f}s"

    def test_large_file_prediction(self, predictor):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            for i in range(100):
                f.write(f'print("Line {i}")\n')
            file_path = Path(f.name)

        start = time.time()
        predictions = predictor.predict_file(file_path)
        end = time.time()

        prediction_time = end - start

        assert prediction_time < 5.0, f"Large file prediction took {prediction_time:.2f}s"

class TestParsingSpeed:

    def test_simple_error_parsing(self):
        from debugbuddy.core.parsers import ErrorParser

        parser = ErrorParser()
        error = "NameError: name 'x' is not defined"

        start = time.time()
        for _ in range(1000):
            parsed = parser.parse(error)
        end = time.time()

        total_time = end - start
        per_parse = total_time / 1000

        assert per_parse < 0.001, f"Per-parse time: {per_parse:.6f}s"

    def test_complex_error_parsing(self):
        from debugbuddy.core.parsers import ErrorParser

        parser = ErrorParser()

        start = time.time()
        for _ in range(100):
            parsed = parser.parse(error)
        end = time.time()

        total_time = end - start
        per_parse = total_time / 100

        assert per_parse < 0.01, f"Complex parse time: {per_parse:.6f}s"

class TestExplanationSpeed:

    def test_explanation_speed(self):
        from debugbuddy.core.parsers import ErrorParser
        from debugbuddy.core.explainer import ErrorExplainer

        parser = ErrorParser()
        explainer = ErrorExplainer()

        error = "NameError: name 'undefined_variable' is not defined"
        parsed = parser.parse(error)

        start = time.time()
        for _ in range(100):
            explanation = explainer.explain(parsed)
        end = time.time()

        total_time = end - start
        per_explanation = total_time / 100

        assert per_explanation < 0.01, f"Explanation time: {per_explanation:.6f}s"

    def test_pattern_matching_speed(self):
        from debugbuddy.core.explainer import ErrorExplainer

        explainer = ErrorExplainer()

        start = time.time()
        for i in range(1000):
            explainer._match_pattern(
                'nameerror',
                f'name var{i} is not defined',
                'python'
            )
        end = time.time()

        total_time = end - start
        per_match = total_time / 1000

        assert per_match < 0.001, f"Pattern match time: {per_match:.6f}s"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])