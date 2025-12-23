import pytest
from debugbuddy.core.explainer import ErrorExplainer
from debugbuddy.core.parser import ErrorParser

@pytest.fixture
def explainer():
    return ErrorExplainer()

@pytest.fixture
def parser():
    return ErrorParser()

def test_explain_python_syntax(explainer, parser):
    error_text = "SyntaxError: invalid syntax"
    parsed = parser.parse(error_text)
    explanation = explainer.explain(parsed)
    assert 'simple' in explanation
    assert 'syntax' in explanation['simple'].lower()

def test_explain_javascript_type_error(explainer, parser):
    error_text = "TypeError: cannot read property"
    parsed = parser.parse(error_text)
    explanation = explainer.explain(parsed)
    assert 'fix' in explanation
    assert any(word in explanation['fix'].lower() for word in ['null', 'undefined', 'property'])

def test_explain_generic(explainer):
    parsed = {'type': 'Unknown', 'message': 'test', 'language': 'unknown'}
    explanation = explainer.explain(parsed)
    assert explanation['simple'] == 'A general error occurred. Check the message for details.'

def test_get_name_suggestions(explainer):
    parsed = {'type': 'NameError', 'message': "name 'prinnt' is not defined"}
    explanation = explainer.explain(parsed)
    suggestions = explanation.get('suggestions', [])
    assert any('print' in s.lower() for s in suggestions)

def test_search_patterns(explainer):
    results = explainer.search_patterns('syntax')
    assert len(results) > 0
    assert any('syntax' in r['name'].lower() for r in results)