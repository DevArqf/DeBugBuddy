import re
from typing import Dict, Optional
from .base import BaseParser

class RubyParser(BaseParser):
    language = 'ruby'

    PATTERNS = {
        'exception': re.compile(r'^([A-Za-z_0-9:]+(?:Error|Exception))(?::\s*(.+))?', re.MULTILINE),
        'file_line': re.compile(r'(?:from\s+)?([^\n:]+\.rb):(\d+):')
    }

    def parse(self, text: str) -> Optional[Dict]:
        result = {
            'type': 'Unknown Error',
            'message': text.strip(),
            'file': None,
            'line': None,
            'language': 'ruby'
        }

        file_match = self.PATTERNS['file_line'].search(text)
        if file_match:
            file_value = file_match.group(1).strip()
            if file_value.startswith('from '):
                file_value = file_value[5:]
            result['file'] = file_value
            result['line'] = int(file_match.group(2))

        match = self.PATTERNS['exception'].search(text)
        if match:
            full_type = match.group(1)
            result['type'] = full_type.split('::')[-1]
            if match.group(2):
                result['message'] = match.group(2).strip()
            else:
                result['message'] = full_type

        return result
