import pytest
from debugbuddy.core.parsers import ErrorParser
from debugbuddy.core.parsers.python import PythonParser
from debugbuddy.core.parsers.javascript import JavaScriptParser
from debugbuddy.core.parsers.typescript import TypeScriptParser
from debugbuddy.core.parsers.c import CParser
from debugbuddy.core.parsers.php import PHPParser

class TestPythonParser:

    def test_name_error(self):
        error = "NameError: name 'x' is not defined"
        parser = PythonParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Name Error'
        assert 'not defined' in result['message']
        assert result['language'] == 'python'

    def test_syntax_error(self):
        error = 'SyntaxError: invalid syntax'
        parser = PythonParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Syntax Error'
        assert result['language'] == 'python'

    def test_type_error(self):
        error = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
        parser = PythonParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Type Error'
        assert result['language'] == 'python'

    def test_index_error(self):
        error = "IndexError: list index out of range"
        parser = PythonParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Index Error'
        assert 'out of range' in result['message']

    def test_file_line_extraction(self):
        error = 'Traceback (most recent call last):\n File "test.py", line 42, in <module>\nNameError: name \'x\' is not defined'
        parser = PythonParser()
        result = parser.parse(error)

        assert result['file'] == 'test.py'
        assert result['line'] == 42

class TestJavaScriptParser:

    def test_reference_error(self):
        error = "ReferenceError: foo is not defined"
        parser = JavaScriptParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Reference Error'
        assert 'not defined' in result['message']
        assert result['language'] == 'javascript'

    def test_type_error(self):
        error = "TypeError: Cannot read property 'name' of undefined"
        parser = JavaScriptParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Type Error'
        assert result['language'] == 'javascript'

    def test_syntax_error(self):
        error = "SyntaxError: Unexpected token )"
        parser = JavaScriptParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Syntax Error'

    def test_file_line_extraction(self):
        error = 'Traceback (most recent call last):\n  File "test.py", line 42, in <module>\nNameError: name \'x\' is not defined'
        parser = PythonParser()
        result = parser.parse(error)
    
        assert result['file'] == 'test.py'
        assert result['line'] == 42

class TestTypeScriptParser:

    def test_type_error(self):
        error = "Type error: Argument of type 'string' is not assignable to parameter of type 'number'"
        parser = TypeScriptParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Type Error'
        assert result['language'] == 'typescript'

    def test_declaration_error(self):
        error = "Cannot find name 'myVariable'"
        parser = TypeScriptParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Declaration Error'

    def test_module_error(self):
        error = "Cannot find module './missing'"
        parser = TypeScriptParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Module Error'

class TestCParser:

    def test_syntax_error(self):
        error = "error: syntax error before 'token'"
        parser = CParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Syntax Error'
        assert result['language'] == 'c'

    def test_undefined_reference(self):
        error = "undefined reference to 'myFunction'"
        parser = CParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Undefined Ref'

    def test_type_mismatch(self):
        error = "incompatible types when assigning to type 'int' from type 'char *'"
        parser = CParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Type Mismatch'

class TestPHPParser:

    def test_parse_error(self):
        error = "Parse error: syntax error, unexpected ';' in test.php on line 5"
        parser = PHPParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Parse Error'
        assert result['language'] == 'php'

    def test_fatal_error(self):
        error = "Fatal error: Call to undefined function myFunc()"
        parser = PHPParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Fatal Error'

    def test_warning(self):
        error = "Warning: Division by zero in script.php"
        parser = PHPParser()
        result = parser.parse(error)

        assert result is not None
        assert result['type'] == 'Warning'

class TestErrorParser:

    def test_auto_detect_python(self):
        error = "Traceback (most recent call last):\nNameError: name 'x' is not defined"
        parser = ErrorParser()
        result = parser.parse(error)

        assert result is not None
        assert result['language'] == 'python'

    def test_auto_detect_javascript(self):
        error = "ReferenceError: foo is not defined"
        parser = ErrorParser()
        result = parser.parse(error)

        assert result is not None
        assert result['language'] == 'javascript'

    def test_explicit_language(self):
        error = "some generic error"
        parser = ErrorParser()
        result = parser.parse(error, language='python')

        assert result is not None

    def test_fallback_generic(self):
        error = "Unknown error format"
        parser = ErrorParser()
        result = parser.parse(error)

        assert result is not None
        assert result['language'] == 'unknown'

    def test_empty_input(self):
        parser = ErrorParser()
        result = parser.parse("")

        assert result is not None
        assert result['type'] == 'Unknown Error'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])