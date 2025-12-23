import pytest
from pathlib import Path
import tempfile
from debugbuddy.core.predictor import ErrorPredictor
from debugbuddy.storage.config import ConfigManager
from debugbuddy.models.prediction import Prediction

@pytest.fixture
def config_manager():
    return ConfigManager()

@pytest.fixture
def predictor(config_manager):
    return ErrorPredictor(config_manager)

@pytest.fixture
def python_file_with_errors():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        return Path(f.name)

@pytest.fixture
def python_file_with_syntax_error():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        return Path(f.name)

@pytest.fixture
def clean_python_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        return Path(f.name)

class TestErrorPredictor:

    def test_init(self, predictor):
        assert predictor is not None
        assert predictor.config is not None
        assert predictor.pattern_mgr is not None

    def test_predict_file_with_errors(self, predictor, python_file_with_errors):
        predictions = predictor.predict_file(python_file_with_errors)

        assert len(predictions) > 0
        assert all(isinstance(p, Prediction) for p in predictions)

        confidences = [p.confidence for p in predictions]
        assert confidences == sorted(confidences, reverse=True)

    def test_predict_syntax_error(self, predictor, python_file_with_syntax_error):
        predictions = predictor.predict_file(python_file_with_syntax_error)

        assert len(predictions) > 0

        syntax_errors = [p for p in predictions if p.error_type == 'SyntaxError']
        assert len(syntax_errors) > 0
        assert syntax_errors[0].confidence == 1.0
        assert syntax_errors[0].severity == 'critical'

    def test_predict_clean_file(self, predictor, clean_python_file):
        predictions = predictor.predict_file(clean_python_file)

        high_confidence = [p for p in predictions if p.confidence > 0.7]
        assert len(high_confidence) == 0

    def test_prediction_fields(self, predictor, python_file_with_errors):
        predictions = predictor.predict_file(python_file_with_errors)

        if predictions:
            pred = predictions[0]
            assert pred.file is not None
            assert pred.line is not None
            assert pred.error_type is not None
            assert pred.message is not None
            assert 0 <= pred.confidence <= 1.0
            assert pred.suggestion is not None
            assert pred.severity in ['low', 'medium', 'high', 'critical']

    def test_undefined_variable_detection(self, predictor, python_file_with_errors):
        predictions = predictor.predict_file(python_file_with_errors)

        name_errors = [p for p in predictions if p.error_type == 'NameError']
        assert len(name_errors) > 0

        messages = [p.message for p in name_errors]
        assert any('undefined_variable' in msg for msg in messages)

    def test_static_analysis(self, predictor, python_file_with_errors):
        predictions = predictor._analyze_static(python_file_with_errors)

        assert isinstance(predictions, list)
        assert all(isinstance(p, Prediction) for p in predictions)

    def test_pattern_analysis(self, predictor, python_file_with_errors):
        predictions = predictor._analyze_patterns(python_file_with_errors)

        assert isinstance(predictions, list)

    def test_ml_analysis(self, predictor, python_file_with_errors):
        predictions = predictor._analyze_ml(python_file_with_errors)

        assert isinstance(predictions, list)

class TestPredictionModel:

    def test_prediction_creation(self):
        pred = Prediction(
            file='test.py',
            line=10,
            column=5,
            error_type='NameError',
            message="name 'x' is not defined",
            confidence=0.9,
            suggestion='Define x before using it',
            severity='high'
        )

        assert pred.file == 'test.py'
        assert pred.line == 10
        assert pred.column == 5
        assert pred.error_type == 'NameError'
        assert pred.confidence == 0.9
        assert pred.severity == 'high'

    def test_prediction_optional_column(self):
        pred = Prediction(
            file='test.py',
            line=10,
            column=None,
            error_type='TypeError',
            message='Type mismatch',
            confidence=0.7,
            suggestion='Check types',
            severity='medium'
        )

        assert pred.column is None

if __name__ == '__main__':
    pytest.main([__file__, '-v'])