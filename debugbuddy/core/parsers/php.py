import re
from typing import Dict, Optional
from .base import BaseParser

class PHPParser(BaseParser):
    language = 'php'

    PATTERNS = {
        'parse_error': re.compile(r'Parse error: (.+)'),
        'fatal_error': re.compile(r'Fatal error: (.+)'),
        'warning': re.compile(r'Warning: (.+)'),
        'notice': re.compile(r'Notice: (.+)'),
    }

    def parse(self, text: str) -> Optional[Dict]:
        result = super().parse(text)

        for error_type, pattern in self.PATTERNS.items():
            match = pattern.search(text)
            if match:
                result['type'] = error_type.replace('_', ' ').title()
                result['message'] = match.group(0)
                return result

        return result if 'type' in result and result['type'] != "Unknown Error" else result