import pytest
from debugbuddy.core.parser import ErrorParser

def test_parse_python_syntax_error():
    parser = ErrorParser()
    error_text = "SyntaxError: invalid syntax\n  File \"test.py\", line 1"
    result = parser.parse(error_text)
    assert result['type'] == 'SyntaxError'
    assert result['language'] == 'python'

def test_parse_javascript_reference_error():
    parser = ErrorParser()
    error_text = "ReferenceError: x is not defined"
    result = parser.parse(error_text)
    assert result['type'] == 'Reference Error'
    assert result['language'] == 'javascript'

def test_parse_typescript_type_error():
    parser = ErrorParser()
    error_text = "Type error: 'string' is not assignable to type 'number'"
    result = parser.parse(error_text)
    assert result['type'] == 'Type Error'
    assert result['language'] == 'typescript'

def test_parse_c_undefined_reference():
    parser = ErrorParser()
    error_text = "undefined reference to 'foo'"
    result = parser.parse(error_text)
    assert result['type'] == 'Undefined Ref'
    assert result['language'] == 'c'

def test_parse_php_fatal_error():
    parser = ErrorParser()
    error_text = "Fatal error: Call to undefined function"
    result = parser.parse(error_text)
    assert result['type'] == 'Fatal Error'
    assert result['language'] == 'php'

def test_parse_generic():
    parser = ErrorParser()
    error_text = "Some unknown error"
    result = parser.parse(error_text)
    assert result['type'] == 'Unknown Error'
    assert result['language'] == 'unknown'

def test_extract_code_snippet():
    parser = ErrorParser()
    error_text = "    print(x)\n    {' ' * 4}^"
    snippet = parser.extract_code_snippet(error_text)
    assert snippet == "print(x)"