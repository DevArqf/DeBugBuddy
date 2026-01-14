import re
from typing import Dict, Optional
from .base import BaseParser

class JavaParser(BaseParser):
    language = 'java'

    PATTERNS = {
        'exception': re.compile(
            r'(?:Exception in thread \"[^\"]+\"\s+)?([A-Za-z0-9_.$]+(?:Exception|Error))(?:\s*:\s*(.+))?'
        ),
        'file_line': re.compile(r'\(([^()]+\.java):(\d+)\)'),
    }

    def parse(self, text: str) -> Optional[Dict]:
        result = {
            'type': 'Unknown Error',
            'message': text.strip(),
            'file': None,
            'line': None,
            'language': 'java'
        }

        file_match = self.PATTERNS['file_line'].search(text)
        if file_match:
            result['file'] = file_match.group(1)
            result['line'] = int(file_match.group(2))

        match = self.PATTERNS['exception'].search(text)
        if match:
            full_type = match.group(1)
            result['type'] = full_type.split('.')[-1].split('$')[-1]
            if match.group(2):
                result['message'] = match.group(2).strip()
            else:
                result['message'] = full_type

        return result
