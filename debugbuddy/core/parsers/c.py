import re
from typing import Dict, Optional
from .base import BaseParser

class CParser(BaseParser):
    language = 'c'

    PATTERNS = {
        'syntax_error': re.compile(r'syntax error: (.+)'),
        'undefined_ref': re.compile(r'undefined reference to \'([^\']+)\''),
        'type_mismatch': re.compile(r'incompatible types (.+)'),
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