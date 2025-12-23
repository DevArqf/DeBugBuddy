from .base import BaseParser
from typing import Dict
import re

class PythonParser(BaseParser):
    language = 'python'

    PATTERNS = {
        'traceback': re.compile(r'Traceback \(most recent call last\):.*?(\w+Error.*?)(?:\n|$)', re.DOTALL),
        'error_line': re.compile(r'(\w+Error): (.+)'),
        'syntax_error': re.compile(r'SyntaxError: (.+)'),
        'name_error': re.compile(r'NameError: name \'([^\']+)\' is not defined'),
        'type_error': re.compile(r'TypeError: (.+)'),
        'attribute_error': re.compile(r'AttributeError: (.+)'),
        'import_error': re.compile(r'(ImportError|ModuleNotFoundError): (.+)'),
        'index_error': re.compile(r'IndexError: (.+)'),
        'key_error': re.compile(r'KeyError: (.+)'),
        'value_error': re.compile(r'ValueError: (.+)'),
    }

    def parse(self, text: str) -> Dict:
        result = super().parse(text)

        error_match = self.PATTERNS['error_line'].search(text)
        if error_match:
            result['type'] = error_match.group(1)
            result['message'] = error_match.group(2)
            return result

        for error_type, pattern in self.PATTERNS.items():
            if error_type in ['traceback', 'error_line', 'file_line']:
                continue
            match = pattern.search(text)
            if match:
                result['type'] = error_type.replace('_', ' ').title()
                result['message'] = match.group(1) if match.groups() else match.group(0)
                return result

        return result