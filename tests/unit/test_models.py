import pytest
from datetime import datetime
from debugbuddy.models.error import Error
from debugbuddy.models.pattern import Pattern
from debugbuddy.models.prediction import Prediction
from debugbuddy.models.training import TrainingData

class TestErrorModel:

    def test_creation(self):
        error = Error(
            raw="NameError: name 'x' is not defined",
            type="NameError",
            message="name 'x' is not defined",
            file="test.py",
            line="10",
            language="python"
        )

        assert error.raw == "NameError: name 'x' is not defined"
        assert error.type == "NameError"
        assert error.message == "name 'x' is not defined"
        assert error.file == "test.py"
        assert error.line == "10"
        assert error.language == "python"

    def test_optional_fields(self):
        error = Error(
            raw="Generic error",
            type="Unknown",
            message="Something went wrong"
        )

        assert error.file is None
        assert error.line is None
        assert error.language == 'unknown'

    def test_minimal_error(self):
        error = Error(
            raw="Error",
            type="Error",
            message="Error occurred"
        )

        assert error.raw is not None
        assert error.type is not None
        assert error.message is not None

class TestPatternModel:

    def test_creation(self):
        pattern = Pattern(
            type="NameError",
            keywords=["name", "not defined", "undefined"],
            simple="Variable not defined before use",
            fix="Define the variable before using it",
            language="python",
            example="x = 5  # Define before use"
        )

        assert pattern.type == "NameError"
        assert len(pattern.keywords) == 3
        assert pattern.simple == "Variable not defined before use"
        assert pattern.fix == "Define the variable before using it"
        assert pattern.language == "python"
        assert pattern.example == "x = 5  # Define before use"

    def test_default_example(self):
        pattern = Pattern(
            type="TestError",
            keywords=["test"],
            simple="Test error",
            fix="Fix test",
            language="python"
        )

        assert pattern.example == ''

    def test_keyword_list(self):
        keywords = ["error", "exception", "failed"]
        pattern = Pattern(
            type="RuntimeError",
            keywords=keywords,
            simple="Runtime error",
            fix="Check runtime conditions",
            language="python"
        )

        assert isinstance(pattern.keywords, list)
        assert pattern.keywords == keywords

class TestPredictionModel:

    def test_creation(self):
        prediction = Prediction(
            file="test.py",
            line=42,
            column=10,
            error_type="NameError",
            message="name 'variable' is not defined",
            confidence=0.95,
            suggestion="Define 'variable' before using it",
            severity="high"
        )

        assert prediction.file == "test.py"
        assert prediction.line == 42
        assert prediction.column == 10
        assert prediction.error_type == "NameError"
        assert prediction.message == "name 'variable' is not defined"
        assert prediction.confidence == 0.95
        assert prediction.suggestion == "Define 'variable' before using it"
        assert prediction.severity == "high"

    def test_optional_column(self):
        prediction = Prediction(
            file="test.py",
            line=10,
            column=None,
            error_type="TypeError",
            message="Type mismatch",
            confidence=0.8,
            suggestion="Check types",
            severity="medium"
        )

        assert prediction.column is None

    def test_severity_levels(self):
        severities = ['low', 'medium', 'high', 'critical']

        for severity in severities:
            prediction = Prediction(
                file="test.py",
                line=1,
                column=None,
                error_type="TestError",
                message="Test",
                confidence=0.5,
                suggestion="Fix",
                severity=severity
            )
            assert prediction.severity == severity

    def test_confidence_range(self):
        pred1 = Prediction(
            file="test.py", line=1, column=None,
            error_type="Test", message="Test",
            confidence=0.1, suggestion="Fix", severity="low"
        )
        assert pred1.confidence == 0.1

        pred2 = Prediction(
            file="test.py", line=1, column=None,
            error_type="Test", message="Test",
            confidence=1.0, suggestion="Fix", severity="critical"
        )
        assert pred2.confidence == 1.0

class TestTrainingDataModel:

    def test_creation(self):
        data = TrainingData(
            error_text="NameError: name 'x' is not defined",
            explanation="Variable 'x' was not defined before use",
            fix="Define x = something before using it",
            language="python"
        )

        assert data.error_text == "NameError: name 'x' is not defined"
        assert data.explanation == "Variable 'x' was not defined before use"
        assert data.fix == "Define x = something before using it"
        assert data.language == "python"
        assert isinstance(data.timestamp, datetime)

    def test_auto_timestamp(self):
        data = TrainingData(
            error_text="Error",
            explanation="Explanation",
            fix="Fix",
            language="python"
        )

        assert data.timestamp is not None
        assert isinstance(data.timestamp, datetime)

        now = datetime.now()
        diff = (now - data.timestamp).total_seconds()
        assert diff < 1.0

    def test_custom_timestamp(self):
        custom_time = datetime(2024, 1, 1, 12, 0, 0)

        data = TrainingData(
            error_text="Error",
            explanation="Explanation",
            fix="Fix",
            language="python",
            timestamp=custom_time
        )

        assert data.timestamp == custom_time

    def test_multiple_languages(self):
        languages = ['python', 'javascript', 'typescript', 'c', 'php', 'java', 'ruby']

        for lang in languages:
            data = TrainingData(
                error_text=f"{lang} error",
                explanation=f"{lang} explanation",
                fix=f"{lang} fix",
                language=lang
            )
            assert data.language == lang

class TestModelIntegration:

    def test_error_to_pattern(self):
        error = Error(
            raw="TypeError: cannot add int and str",
            type="TypeError",
            message="cannot add int and str",
            language="python"
        )

        pattern = Pattern(
            type=error.type,
            keywords=["type", "cannot add", "int", "str"],
            simple="Type mismatch in operation",
            fix="Convert types before operation",
            language=error.language
        )

        assert pattern.type == error.type
        assert pattern.language == error.language

    def test_training_data_to_pattern(self):
        training = TrainingData(
            error_text="CustomError: custom issue",
            explanation="A custom error occurred",
            fix="Fix the custom issue",
            language="python"
        )

        pattern = Pattern(
            type="CustomError",
            keywords=["custom", "error", "issue"],
            simple=training.explanation,
            fix=training.fix,
            language=training.language
        )

        assert pattern.simple == training.explanation
        assert pattern.fix == training.fix
        assert pattern.language == training.language

    def test_prediction_from_error(self):
        error = Error(
            raw="NameError at line 10",
            type="NameError",
            message="name not defined",
            file="test.py",
            line="10",
            language="python"
        )

        prediction = Prediction(
            file=error.file,
            line=int(error.line),
            column=None,
            error_type=error.type,
            message=error.message,
            confidence=0.9,
            suggestion="Define the variable",
            severity="high"
        )

        assert prediction.file == error.file
        assert prediction.line == int(error.line)
        assert prediction.error_type == error.type

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
