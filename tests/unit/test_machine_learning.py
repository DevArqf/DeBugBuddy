import pytest
import numpy as np
from pathlib import Path
import tempfile
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from debugbuddy.models.ml_engine import (
    NeuralNetwork,
    ErrorEmbedding,
    FeatureExtractor,
    MLEngine,
    TrainingExample
)

class TestNeuralNetwork:

    def test_initialization(self):
        nn = NeuralNetwork(
            input_size=10,
            hidden_sizes=[20, 10],
            output_size=5
        )

        assert len(nn.layers) == 3
        assert nn.layers[0]['w'].shape == (10, 20)
        assert nn.layers[1]['w'].shape == (20, 10)
        assert nn.layers[2]['w'].shape == (10, 5)

    def test_forward_pass(self):
        nn = NeuralNetwork(input_size=5, hidden_sizes=[10], output_size=3)
        X = np.random.randn(2, 5)

        output = nn.forward(X)

        assert output.shape == (2, 3)
        assert np.allclose(output.sum(axis=1), 1.0)
        assert np.all(output >= 0) and np.all(output <= 1)

    def test_activation_functions(self):
        nn = NeuralNetwork(input_size=5, hidden_sizes=[10], output_size=3)

        x = np.array([-2, -1, 0, 1, 2])
        relu_out = nn.relu(x)
        assert np.array_equal(relu_out, [0, 0, 0, 1, 2])

        relu_grad = nn.relu_derivative(x)
        assert np.array_equal(relu_grad, [0, 0, 0, 1, 1])

        logits = np.array([[1, 2, 3], [1, 1, 1]])
        softmax_out = nn.softmax(logits)
        assert softmax_out.shape == (2, 3)
        assert np.allclose(softmax_out.sum(axis=1), 1.0)

    def test_training(self):
        X = np.array([
            [1, 0], [0, 1], [1, 1], [0, 0],
            [1, 0], [0, 1], [1, 1], [0, 0]
        ])
        y = np.array([
            [1, 0], [0, 1], [1, 0], [0, 1],
            [1, 0], [0, 1], [1, 0], [0, 1]
        ])

        nn = NeuralNetwork(
            input_size=2,
            hidden_sizes=[4],
            output_size=2,
            learning_rate=0.1
        )

        losses = nn.train(X, y, epochs=50, batch_size=4)

        assert losses[0] > losses[-1]
        assert len(losses) == 50

    def test_prediction(self):
        nn = NeuralNetwork(input_size=3, hidden_sizes=[5], output_size=2)
        X = np.random.randn(5, 3)

        predictions = nn.predict(X)

        assert predictions.shape == (5, 2)
        assert np.all(predictions >= 0) and np.all(predictions <= 1)

class TestErrorEmbedding:

    def test_initialization(self):
        embedding = ErrorEmbedding(embedding_dim=64, window_size=2)

        assert embedding.embedding_dim == 64
        assert embedding.window_size == 2
        assert embedding.embeddings is None

    def test_tokenization(self):
        embedding = ErrorEmbedding()
        text = "NameError: name 'x' is not defined"

        tokens = embedding.tokenize(text)

        assert 'nameerror' in tokens
        assert 'name' in tokens
        assert 'not' in tokens
        assert 'defined' in tokens

    def test_vocab_building(self):
        embedding = ErrorEmbedding(embedding_dim=32)
        texts = [
            "NameError: name 'x' is not defined",
            "TypeError: cannot add int and str",
            "NameError: name 'y' is not defined"
        ]

        embedding.build_vocab(texts)

        assert embedding.vocab_size > 0
        assert 'nameerror' in embedding.word_to_idx
        assert 'typeerror' in embedding.word_to_idx
        assert embedding.embeddings is not None
        assert embedding.embeddings.shape[0] == embedding.vocab_size
        assert embedding.embeddings.shape[1] == 32

    def test_training_pairs_generation(self):
        embedding = ErrorEmbedding(window_size=2)
        embedding.word_to_idx = {'name': 0, 'error': 1, 'is': 2, 'not': 3, 'defined': 4}

        text = "name error is not defined"
        pairs = embedding.generate_training_pairs(text)

        assert len(pairs) > 0
        assert all(isinstance(p, tuple) and len(p) == 2 for p in pairs)

    def test_embedding_training(self):
        embedding = ErrorEmbedding(embedding_dim=16)
        texts = [
            "NameError: name 'x' is not defined",
            "NameError: name 'y' is not defined",
            "TypeError: type mismatch"
        ]

        embedding.train(texts, epochs=2)

        assert embedding.embeddings is not None
        assert embedding.vocab_size > 0

    def test_text_embedding(self):
        embedding = ErrorEmbedding(embedding_dim=16)
        texts = [
            "NameError: name 'x' is not defined",
            "TypeError: type mismatch"
        ]

        embedding.train(texts, epochs=2)

        vec = embedding.embed("NameError: undefined variable")

        assert vec.shape == (16,)
        assert not np.all(vec == 0)

    def test_similarity(self):
        embedding = ErrorEmbedding(embedding_dim=32)
        texts = [
            "NameError: name 'x' is not defined",
            "NameError: name 'y' is not defined",
            "TypeError: cannot add int and str"
        ]

        embedding.train(texts, epochs=5)

        vec1 = embedding.embed("NameError: name 'a' is not defined")
        vec2 = embedding.embed("NameError: name 'b' is not defined")
        vec3 = embedding.embed("TypeError: type error")

        def cosine_sim(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

        sim_12 = cosine_sim(vec1, vec2)
        sim_13 = cosine_sim(vec1, vec3)

        assert sim_12 > sim_13

class TestFeatureExtractor:

    def test_initialization(self):
        extractor = FeatureExtractor()

        assert len(extractor.error_keywords) > 0
        assert 'python' in extractor.language_indicators

    def test_feature_extraction(self):
        extractor = FeatureExtractor()
        error = "NameError: name 'undefined_variable' is not defined"

        features = extractor.extract(error, language='python')

        assert isinstance(features, np.ndarray)
        assert len(features) > 0
        assert features.dtype == np.float64

    def test_feature_consistency(self):
        extractor = FeatureExtractor()
        error = "TypeError: cannot add int and str"

        features1 = extractor.extract(error)
        features2 = extractor.extract(error)

        assert np.array_equal(features1, features2)

    def test_different_languages(self):
        extractor = FeatureExtractor()

        python_error = "NameError: name 'x' is not defined"
        js_error = "ReferenceError: x is not defined"

        py_features = extractor.extract(python_error, 'python')
        js_features = extractor.extract(js_error, 'javascript')

        assert not np.array_equal(py_features, js_features)

class TestMLEngine:

    @pytest.fixture
    def sample_examples(self):
        return [
            TrainingExample("NameError: name 'x' is not defined", "NameError", "python"),
            TrainingExample("NameError: name 'y' is not defined", "NameError", "python"),
            TrainingExample("TypeError: cannot add int and str", "TypeError", "python"),
            TrainingExample("TypeError: type mismatch", "TypeError", "python"),
            TrainingExample("IndexError: list index out of range", "IndexError", "python"),
            TrainingExample("IndexError: index too large", "IndexError", "python"),
        ]

    def test_initialization(self, tmp_path):
        engine = MLEngine(model_dir=tmp_path)

        assert engine.model_dir == tmp_path
        assert engine.feature_extractor is not None
        assert not engine.trained

    def test_data_preparation(self, sample_examples):
        engine = MLEngine()
        X, y = engine.prepare_data(sample_examples)

        assert X.shape[0] == len(sample_examples)
        assert y.shape[0] == len(sample_examples)
        assert y.shape[1] == 3

        assert np.allclose(y.sum(axis=1), 1.0)

    def test_classifier_training(self, sample_examples, tmp_path):
        engine = MLEngine(model_dir=tmp_path)

        losses = engine.train_classifier(sample_examples, epochs=20)

        assert engine.trained
        assert engine.classifier is not None
        assert len(losses) == 20
        assert losses[-1] < losses[0]

    def test_embedding_training(self, sample_examples, tmp_path):
        engine = MLEngine(model_dir=tmp_path)

        engine.train_embeddings(sample_examples, epochs=3)

        assert engine.embedding_model is not None
        assert engine.embedding_model.embeddings is not None

    def test_error_classification(self, sample_examples, tmp_path):
        engine = MLEngine(model_dir=tmp_path)
        engine.train_classifier(sample_examples, epochs=30)

        result = engine.classify_error("NameError: name 'z' is not defined", "python")

        assert 'predictions' in result
        assert len(result['predictions']) > 0
        assert 'type' in result['predictions'][0]
        assert 'confidence' in result['predictions'][0]

        top = result['top_prediction']
        assert top is not None
    
        assert top['type'] in ['NameError', 'TypeError', 'IndexError', 'Name Error'], \
            f"Expected one of the trained types, got: {top['type']}"

    def test_save_and_load_models(self, sample_examples, tmp_path):
        engine1 = MLEngine(model_dir=tmp_path)
        engine1.train_classifier(sample_examples, epochs=20)
        engine1.train_embeddings(sample_examples, epochs=3)

        engine1.save_models()

        engine2 = MLEngine(model_dir=tmp_path)
        engine2.load_models()

        assert engine2.trained
        assert engine2.classifier is not None
        assert engine2.embedding_model is not None

        result = engine2.classify_error("NameError: undefined", "python")
        assert 'predictions' in result

    def test_prediction_confidence(self, sample_examples, tmp_path):
        engine = MLEngine(model_dir=tmp_path)
        engine.train_classifier(sample_examples, epochs=50)

        result1 = engine.classify_error("NameError: name 'foo' is not defined", "python")
        top1 = result1['top_prediction']

        result2 = engine.classify_error("Random error message", "python")
        top2 = result2['top_prediction']

        assert 0 <= top1['confidence'] <= 1.0
        assert 0 <= top2['confidence'] <= 1.0

class TestMLIntegration:

    def test_integration_with_parser(self, tmp_path):
        from debugbuddy.core.parsers import ErrorParser

        parser = ErrorParser()
        errors = [
            "NameError: name 'x' is not defined",
            "NameError: name 'y' is not defined",
            "TypeError: cannot add types",
            "TypeError: type mismatch",
        ]

        examples = []
        for error in errors:
            parsed = parser.parse(error)
            if parsed:
                example = TrainingExample(
                error_text=parsed.get('message', error),
                error_type=parsed['type'],
                language=parsed['language']
            )
            examples.append(example)

        engine = MLEngine(model_dir=tmp_path)
        engine.train_classifier(examples, epochs=20)

        new_error = "NameError: name 'z' is not defined"
        parsed_new = parser.parse(new_error)

        result = engine.classify_error(parsed_new.get('message', new_error), parsed_new['language'])

        assert result['top_prediction']['type'] in ['Name Error', 'NameError', 'Unknown Error']

    def test_ml_enhanced_prediction(self, tmp_path):
        from debugbuddy.core.predictor import ErrorPredictor
        from debugbuddy.storage.config import ConfigManager

        config = ConfigManager()
        predictor = ErrorPredictor(config)

        examples = [
            TrainingExample(f"NameError {i}", "NameError", "python")
            for i in range(10)
        ]

        engine = MLEngine(model_dir=tmp_path)
        engine.train_classifier(examples, epochs=10)

        assert engine.trained

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])