import pytest
import sys
from debugbuddy.core.parsers import ErrorParser
from debugbuddy.core.explainer import ErrorExplainer
from debugbuddy.storage.history import HistoryManager
from debugbuddy.core.predictor import ErrorPredictor
from debugbuddy.storage.config import ConfigManager

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
        size_mb = get_size(parser) / (1024 * 1024)
        assert size_mb < 2.0, f"ErrorParser uses {size_mb:.2f} MB (too high)"

    def test_explainer_memory(self):
        explainer = ErrorExplainer()
        size_mb = get_size(explainer) / (1024 * 1024)
        assert size_mb < 10.0, f"ErrorExplainer uses {size_mb:.2f} MB (too high)"

    def test_predictor_memory(self):
        config = ConfigManager()
        predictor = ErrorPredictor(config)
        size_mb = get_size(predictor) / (1024 * 1024)
        assert size_mb < 15.0, f"ErrorPredictor uses {size_mb:.2f} MB (too high)"

    def test_history_manager_empty(self):
        history = HistoryManager()
        history.clear()
        size_mb = get_size(history) / (1024 * 1024)
        assert size_mb < 1.0, f"Empty HistoryManager uses {size_mb:.2f} MB"

    def test_history_manager_with_100_entries(self):
        parser = ErrorParser()
        explainer = ErrorExplainer()
        history = HistoryManager()
        history.clear()

        sample_error = "NameError: name 'undefined_var' is not defined on line 10"

        for i in range(100):
            parsed = parser.parse(sample_error.replace("undefined_var", f"var{i}"))
            explanation = explainer.explain(parsed)
            history.add(parsed, explanation)

        size_mb = get_size(history) / (1024 * 1024)
        assert size_mb < 20.0, f"HistoryManager with 100 entries uses {size_mb:.2f} MB"