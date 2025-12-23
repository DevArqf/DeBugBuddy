# debugbuddy/core/parsers/__init__.py
from .base import BaseParser
from .python import PythonParser
from .javascript import JavaScriptParser
from .typescript import TypeScriptParser
from .c import CParser
from .php import PHPParser

class ErrorParser:
    def __init__(self):
        self.parsers = {
            'python': PythonParser(),
            'javascript': JavaScriptParser(),
            'typescript': TypeScriptParser(),
            'c': CParser(),
            'php': PHPParser(),
        }

    def parse(self, error_text, language=None):
        if language and language in self.parsers:
            return self.parsers[language].parse(error_text)
        # Else try all or detect
        # Implement detection
        for parser in self.parsers.values():
            result = parser.parse(error_text)
            if result:
                return result
        return None