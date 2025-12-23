import re
import json
from .base import BaseParser
from .python import PythonParser
from .javascript import JavaScriptParser
from .typescript import TypeScriptParser
from .c import CParser
from .php import PHPParser
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

class ErrorParser:
    def __init__(self):
        self.parsers = {
            'python': PythonParser(),
            'javascript': JavaScriptParser(),
            'typescript': TypeScriptParser(),
            'c': CParser(),
            'php': PHPParser(),
        }

    def parse(self, error_text: str, language=None):
        error_text = error_text.strip()
        lower_text = error_text.lower()

        if language:
            if language in self.parsers:
                result = self.parsers[language].parse(error_text)
                if result:
                    result['language'] = language
                    return result

        if any(kw in lower_text for kw in ['traceback', 'file', 'line', 'python', 'py']):
            return self.parsers['python'].parse(error_text)
        elif any(kw in lower_text for kw in ['referenceerror', 'typeerror', 'syntaxerror', 'javascript', 'js']):
            return self.parsers['javascript'].parse(error_text)
        elif any(kw in lower_text for kw in ['type error', 'cannot find name', 'typescript', 'ts']):
            return self.parsers['typescript'].parse(error_text)
        elif any(kw in lower_text for kw in ['syntax error', 'undefined reference', 'c ', 'gcc']):
            return self.parsers['c'].parse(error_text)
        elif any(kw in lower_text for kw in ['parse error', 'fatal error', 'php']):
            return self.parsers['php'].parse(error_text)
        else:
            return self._parse_generic(error_text)

    def _parse_generic(self, text: str) -> Dict:
        lines = text.split('\n')
        first_line = lines[0] if lines else text

        return {
            'raw': text,
            'type': 'Unknown Error',
            'message': first_line[:200],
            'language': 'unknown',
            'file': None,
            'line': None,
        }