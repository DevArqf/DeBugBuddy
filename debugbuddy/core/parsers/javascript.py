import re
from typing import Dict, Optional
from .base import BaseParser

class JavaScriptParser(BaseParser):
    language = 'javascript'

    PATTERNS = {
        'reference_error': re.compile(r'ReferenceError: (.+) is not defined'),
        'type_error': re.compile(r'TypeError: (.+)'),
        'syntax_error': re.compile(r'SyntaxError: (.+)'),
        'range_error': re.compile(r'RangeError: (.+)'),
        'uri_error': re.compile(r'URIError: (.+)'),
        'file_line': re.compile(r'at (.+) \((.+):(\d+):(\d+)\)'),
    }

    def parse(self, text: str) -> Optional[Dict]:
        result = super().parse(text)

        file_match = self.PATTERNS['file_line'].search(text)
        if file_match:
            result['file'] = file_match.group(2)
            result['line'] = int(file_match.group(3))

        for error_type, pattern in self.PATTERNS.items():
            if error_type == 'file_line':
                continue
            match = pattern.search(text)
            if match:
                result['type'] = error_type.replace('_', ' ').title()
                result['message'] = match.group(1) if match.groups() else match.group(0)
                return result

        return result if result['type'] else None