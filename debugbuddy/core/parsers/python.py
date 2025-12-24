import re
from typing import Dict, Optional
from .base import BaseParser

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

    def parse(self, text: str) -> Optional[Dict]:
        result = {
            "raw": text,
            "type": "Unknown Error",
            "message": text.strip(),
            "file": None,
            "line": None,
            "language": "python"
        }

        file_match = re.search(r'File "([^"]+)", line (\d+)', text)
        if file_match:
            result['file'] = file_match.group(1)
            result['line'] = int(file_match.group(2))

        error_match = self.PATTERNS['error_line'].search(text)
        if error_match:
            error_type = error_match.group(1)
            if error_type.endswith('Error'):
                base = error_type[:-5]
                spaced = re.sub(r'([A-Z])', r' \1', base).strip()
                result['type'] = f"{spaced} Error"
            else:
                result['type'] = error_type
            result['message'] = error_match.group(2)
            return result

        for error_type, pattern in self.PATTERNS.items():
            if error_type in ['traceback', 'error_line']:
                continue
            match = pattern.search(text)
            if match:
                formatted_type = error_type.replace('_', ' ').title()
                result['type'] = formatted_type
                result['message'] = match.group(1) if match.groups() else match.group(0)
                return result

        return result