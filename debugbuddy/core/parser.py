import re
from typing import Dict, Optional

class ErrorParser:

    PYTHON_PATTERNS = {
        'traceback': re.compile(r'Traceback \(most recent call last\):.*?(\w+Error.*?)(?:\n|$)', re.DOTALL),
        'error_line': re.compile(r'(\w+Error): (.+)'),
        'file_line': re.compile(r'File "([^"]+)", line (\d+)'),
        'syntax_error': re.compile(r'SyntaxError: (.+)'),
        'name_error': re.compile(r'NameError: name \'([^\']+)\' is not defined'),
        'type_error': re.compile(r'TypeError: (.+)'),
        'attribute_error': re.compile(r'AttributeError: (.+)'),
        'import_error': re.compile(r'(ImportError|ModuleNotFoundError): (.+)'),
        'index_error': re.compile(r'IndexError: (.+)'),
        'key_error': re.compile(r'KeyError: (.+)'),
        'value_error': re.compile(r'ValueError: (.+)'),
    }

    JS_PATTERNS = {
        'reference_error': re.compile(r'ReferenceError: (.+) is not defined'),
        'type_error': re.compile(r'TypeError: (.+)'),
        'syntax_error': re.compile(r'SyntaxError: (.+)'),
        'range_error': re.compile(r'RangeError: (.+)'),
        'uri_error': re.compile(r'URIError: (.+)'),
        'file_line': re.compile(r'at (.+) \((.+):(\d+):(\d+)\)'),
    }

    def parse(self, error_text: str) -> Optional[Dict]:

        error_text = error_text.strip()

        result = self._parse_python(error_text)
        if result:
            result['language'] = 'python'
            return result

        result = self._parse_javascript(error_text)
        if result:
            result['language'] = 'javascript'
            return result

        return self._parse_generic(error_text)

    def _parse_python(self, text: str) -> Optional[Dict]:

        result = {
            'raw': text,
            'type': None,
            'message': None,
            'file': None,
            'line': None,
            'traceback': None,
        }

        traceback_match = self.PYTHON_PATTERNS['traceback'].search(text)
        if traceback_match:
            result['traceback'] = traceback_match.group(0)

        file_match = self.PYTHON_PATTERNS['file_line'].search(text)
        if file_match:
            result['file'] = file_match.group(1)
            result['line'] = int(file_match.group(2))

        for error_type, pattern in self.PYTHON_PATTERNS.items():
            if error_type in ['traceback', 'file_line', 'error_line']:
                continue

            match = pattern.search(text)
            if match:
                result['type'] = error_type.replace('_', ' ').title()
                result['message'] = match.group(1) if match.groups() else match.group(0)
                return result

        error_match = self.PYTHON_PATTERNS['error_line'].search(text)
        if error_match:
            result['type'] = error_match.group(1)
            result['message'] = error_match.group(2)
            return result

        return None if not result['type'] else result

    def _parse_javascript(self, text: str) -> Optional[Dict]:

        result = {
            'raw': text,
            'type': None,
            'message': None,
            'file': None,
            'line': None,
            'column': None,
        }

        for error_type, pattern in self.JS_PATTERNS.items():
            if error_type == 'file_line':
                match = pattern.search(text)
                if match:
                    result['function'] = match.group(1)
                    result['file'] = match.group(2)
                    result['line'] = int(match.group(3))
                    result['column'] = int(match.group(4))
                continue

            match = pattern.search(text)
            if match:
                result['type'] = error_type.replace('_', ' ').title()
                result['message'] = match.group(1)
                return result

        return None if not result['type'] else result

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

    def extract_code_snippet(self, error_text: str) -> Optional[str]:

        lines = error_text.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'\^+|~+', line):
                if i > 0:
                    return lines[i-1].strip()

        return None