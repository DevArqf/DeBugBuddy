import pytest
import tempfile
import json
from pathlib import Path
from debugbuddy.core.trainer import PatternTrainer
from debugbuddy.storage.config import ConfigManager
from debugbuddy.models.training import TrainingData
from debugbuddy.models.pattern import Pattern

@pytest.fixture
def config_manager():
    return ConfigManager()

@pytest.fixture
def trainer(config_manager, tmp_path):
    trainer = PatternTrainer(config_manager)
    trainer.custom_patterns_dir = tmp_path / 'patterns'
    trainer.custom_patterns_dir.mkdir(parents=True, exist_ok=True)
    return trainer

@pytest.fixture
def sample_training_data():
    return [
        TrainingData(
            error_text="CustomError: Something went wrong in module X",
            explanation="A custom error occurred in module X",
            fix="Check module X configuration",
            language="python"
        ),
        TrainingData(
            error_text="CustomError: Another issue in module X",
            explanation="Custom error in module X",
            fix="Verify module X settings",
            language="python"
        ),
        TrainingData(
            error_text="CustomError: Failed to process in module X",
            explanation="Processing failed in module X",
            fix="Review module X input data",
            language="python"
        )
    ]

class TestPatternTrainer:

    def test_init(self, trainer):
        assert trainer is not None
        assert trainer.storage is not None
        assert trainer.custom_patterns_dir.exists()
        assert trainer.pattern_mgr is not None

    def test_add_training_example(self, trainer):
        result = trainer.add_training_example(
            error_text="TestError: test message",
            explanation="This is a test error",
            fix="Fix the test",
            language="python"
        )

        assert isinstance(result, bool)

    def test_extract_keywords(self, trainer, sample_training_data):
        keywords = trainer._extract_keywords(sample_training_data)

        assert isinstance(keywords, list)
        assert len(keywords) <= 10
        assert 'customerror' in [k.lower() for k in keywords]
        assert 'module' in [k.lower() for k in keywords]

    def test_determine_error_type(self, trainer, sample_training_data):
        error_type = trainer._determine_error_type(sample_training_data)

        assert isinstance(error_type, str)
        assert 'CustomError' in error_type or 'Error' in error_type

    def test_generate_explanation(self, trainer, sample_training_data):
        explanation = trainer._generate_explanation(sample_training_data)

        assert isinstance(explanation, str)
        assert len(explanation) > 0

    def test_generate_fix(self, trainer, sample_training_data):
        fix = trainer._generate_fix(sample_training_data)

        assert isinstance(fix, str)
        assert len(fix) > 0

    def test_train_pattern(self, trainer, sample_training_data):
        pattern = trainer.train_pattern(sample_training_data)

        assert isinstance(pattern, Pattern)
        assert pattern.type is not None
        assert len(pattern.keywords) > 0
        assert pattern.simple is not None
        assert pattern.fix is not None
        assert pattern.language == 'python'

    def test_save_custom_pattern(self, trainer, sample_training_data):
        pattern = trainer.train_pattern(sample_training_data)

        pattern_file = trainer.custom_patterns_dir / f"{pattern.language}.json"
        assert pattern_file.exists()

        with open(pattern_file, 'r') as f:
            data = json.load(f)

        assert 'errors' in data
        assert len(data['errors']) > 0
        assert data['errors'][0]['type'] == pattern.type

    def test_list_custom_patterns_empty(self, trainer):
        patterns = trainer.list_custom_patterns()

        assert isinstance(patterns, list)
        assert len(patterns) == 0

    def test_list_custom_patterns(self, trainer, sample_training_data):
        pattern = trainer.train_pattern(sample_training_data)

        patterns = trainer.list_custom_patterns()

        assert len(patterns) > 0
        assert any(p.type == pattern.type for p in patterns)

    def test_delete_custom_pattern(self, trainer, sample_training_data):
        pattern = trainer.train_pattern(sample_training_data)
        pattern_id = pattern.type

        patterns_before = trainer.list_custom_patterns()
        assert any(p.type == pattern_id for p in patterns_before)

        result = trainer.delete_custom_pattern(pattern_id)
        assert result is True

        patterns_after = trainer.list_custom_patterns()
        assert not any(p.type == pattern_id for p in patterns_after)

    def test_delete_nonexistent_pattern(self, trainer):
        result = trainer.delete_custom_pattern('NonexistentError')
        assert result is False

    def test_multiple_languages(self, trainer):
        python_data = [
            TrainingData("PyError: test", "Python error", "Fix it", "python"),
            TrainingData("PyError: test2", "Python error", "Fix it", "python")
        ]

        js_data = [
            TrainingData("JsError: test", "JS error", "Fix it", "javascript"),
            TrainingData("JsError: test2", "JS error", "Fix it", "javascript")
        ]

        py_pattern = trainer.train_pattern(python_data)
        js_pattern = trainer.train_pattern(js_data)

        assert py_pattern.language == 'python'
        assert js_pattern.language == 'javascript'

        patterns = trainer.list_custom_patterns()
        assert len(patterns) == 2

class TestTrainingData:

    def test_creation(self):
        data = TrainingData(
            error_text="TestError: message",
            explanation="Explanation",
            fix="Fix",
            language="python"
        )

        assert data.error_text == "TestError: message"
        assert data.explanation == "Explanation"
        assert data.fix == "Fix"
        assert data.language == "python"
        assert data.timestamp is not None

    def test_timestamp_auto_generated(self):
        data = TrainingData(
            error_text="Test",
            explanation="Test",
            fix="Test",
            language="python"
        )

        from datetime import datetime
        assert isinstance(data.timestamp, datetime)

    def test_custom_timestamp(self):
        from datetime import datetime
        custom_time = datetime(2024, 1, 1, 12, 0, 0)

        data = TrainingData(
            error_text="Test",
            explanation="Test",
            fix="Test",
            language="python",
            timestamp=custom_time
        )

        assert data.timestamp == custom_time

class TestPattern:

    def test_creation(self):
        pattern = Pattern(
            type="CustomError",
            keywords=["custom", "error", "test"],
            simple="A custom error occurred",
            fix="Fix the custom error",
            language="python",
            example="# Example code"
        )

        assert pattern.type == "CustomError"
        assert len(pattern.keywords) == 3
        assert pattern.simple == "A custom error occurred"
        assert pattern.fix == "Fix the custom error"
        assert pattern.language == "python"
        assert pattern.example == "# Example code"

    def test_optional_example(self):
        pattern = Pattern(
            type="TestError",
            keywords=["test"],
            simple="Test error",
            fix="Fix test",
            language="python"
        )

        assert pattern.example == ''

if __name__ == '__main__':
    pytest.main([__file__, '-v'])