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

    TS_PATTERNS = {
        'type_error': re.compile(r'Type error: (.+)'),
        'declaration_error': re.compile(r'Cannot find name \'([^\']+)\''),
        'module_error': re.compile(r'Cannot find module \'([^\']+)\''),
    }

    C_PATTERNS = {
        'syntax_error': re.compile(r'syntax error: (.+)'),
        'undefined_ref': re.compile(r'undefined reference to \'([^\']+)\''),
        'type_mismatch': re.compile(r'incompatible types (.+)'),
    }

    PHP_PATTERNS = {
        'parse_error': re.compile(r'Parse error: (.+)'),
        'fatal_error': re.compile(r'Fatal error: (.+)'),
        'warning': re.compile(r'Warning: (.+)'),
        'notice': re.compile(r'Notice: (.+)'),
    }

    def parse(self, error_text: str, language: Optional[str] = None) -> Optional[Dict]:
        error_text = error_text.strip()
        lower_text = error_text.lower()

        if language:
            parse_method = f'_parse_{language}'
            if hasattr(self, parse_method):
                result = getattr(self, parse_method)(error_text)
                if result:
                    result['language'] = language
                    return result

        if any(kw in lower_text for kw in ['traceback', 'file', 'line', 'python', 'py']):
            return self._parse_python(error_text)
        elif any(kw in lower_text for kw in ['referenceerror', 'typeerror', 'syntaxerror', 'javascript', 'js']):
            return self._parse_js(error_text)
        elif any(kw in lower_text for kw in ['type error', 'cannot find name', 'typescript', 'ts']):
            return self._parse_ts(error_text)
        elif any(kw in lower_text for kw in ['syntax error', 'undefined reference', 'c ', 'gcc']):
            return self._parse_c(error_text)
        elif any(kw in lower_text for kw in ['parse error', 'fatal error', 'php']):
            return self._parse_php(error_text)
        else:
            return self._parse_generic(error_text)

    def _parse_python(self, text: str) -> Optional[Dict]:
        result = {
            'raw': text,
            'type': None,
            'message': None,
            'file': None,
            'line': None,
            'language': 'python',
        }

        file_match = self.PYTHON_PATTERNS['file_line'].search(text)
        if file_match:
            result['file'] = file_match.group(1)
            result['line'] = int(file_match.group(2))

        error_match = self.PYTHON_PATTERNS['error_line'].search(text)
        if error_match:
            result['type'] = error_match.group(1)
            result['message'] = error_match.group(2)
            return result

        for error_type, pattern in self.PYTHON_PATTERNS.items():
            if error_type in ['traceback', 'error_line', 'file_line']:
                continue
            match = pattern.search(text)
            if match:
                result['type'] = error_type.replace('_', ' ').title()
                result['message'] = match.group(1) if match.groups() else match.group(0)
                return result

        return result if result['type'] else None

    def _parse_js(self, text: str) -> Optional[Dict]:
        result = {
            'raw': text,
            'type': None,
            'message': None,
            'file': None,
            'line': None,
            'language': 'javascript',
        }

        file_match = self.JS_PATTERNS['file_line'].search(text)
        if file_match:
            result['file'] = file_match.group(2)
            result['line'] = int(file_match.group(3))

        for error_type, pattern in self.JS_PATTERNS.items():
            if error_type == 'file_line':
                continue
            match = pattern.search(text)
            if match:
                result['type'] = error_type.replace('_', ' ').title()
                result['message'] = match.group(1) if match.groups() else match.group(0)
                return result

        return result if result['type'] else None

    def _parse_ts(self, text: str) -> Optional[Dict]:
        result = {
            'raw': text,
            'type': None,
            'message': None,
            'file': None,
            'line': None,
            'language': 'typescript',
        }

        for error_type, pattern in self.TS_PATTERNS.items():
            match = pattern.search(text)
            if match:
                result['type'] = error_type.replace('_', ' ').title()
                result['message'] = match.group(0)
                return result

        return result if result['type'] else None

    def _parse_c(self, text: str) -> Optional[Dict]:
        result = {
            'raw': text,
            'type': None,
            'message': None,
            'file': None,
            'line': None,
            'language': 'c',
        }

        for error_type, pattern in self.C_PATTERNS.items():
            match = pattern.search(text)
            if match:
                result['type'] = error_type.replace('_', ' ').title()
                result['message'] = match.group(0)
                return result

        return result if result['type'] else None

    def _parse_php(self, text: str) -> Optional[Dict]:
        result = {
            'raw': text,
            'type': None,
            'message': None,
            'file': None,
            'line': None,
            'language': 'php',
        }

        for error_type, pattern in self.PHP_PATTERNS.items():
            match = pattern.search(text)
            if match:
                result['type'] = error_type.replace('_', ' ').title()
                result['message'] = match.group(0)
                return result

        return result if result['type'] else None

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