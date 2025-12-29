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
def empty_py_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("# Empty file\n")
    yield Path(f.name)
    Path(f.name).unlink()


@pytest.fixture
def large_py_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        for i in range(1000):
            f.write(f"def func{i}():\n    print('Hello {i}')\n")
    yield Path(f.name)
    Path(f.name).unlink()


class TestPredictionSpeed:

    def test_predict_empty_file(self, predictor, empty_py_file):
        start = time.time()
        predictions = predictor.predict_file(empty_py_file)
        duration = time.time() - start
        assert len(predictions) == 0 or all(p.severity == "low" for p in predictions)
        assert duration < 1.0, f"Prediction on empty file took {duration:.2f}s"

    def test_predict_small_file(self, predictor):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("x = undefined_variable\n")
            file_path = Path(f.name)

        start = time.time()
        predictions = predictor.predict_file(file_path)
        duration = time.time() - start

        assert duration < 2.0, f"Prediction on small buggy file took {duration:.2f}s"

    def test_predict_large_file(self, predictor, large_py_file):
        start = time.time()
        predictions = predictor.predict_file(large_py_file)
        duration = time.time() - start
        assert duration < 10.0, f"Prediction on large file took {duration:.2f}s"