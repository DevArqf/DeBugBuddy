import re
from typing import Dict, Optional

class BaseParser:
    PATTERNS = {}

    def parse(self, text: str) -> Optional[Dict]:
        result = {
            'raw': text,
            'type': None,
            'message': None,
            'file': None,
            'line': None,
            'language': self.language,
        }
        # Common parsing logic
        # For example, file_line = re.compile(r'File "([^"]+)", line (\d+)')
        file_match = re.search(r'File "([^"]+)", line (\d+)', text)
        if file_match:
            result['file'] = file_match.group(1)
            result['line'] = int(file_match.group(2))

        return result if result['type'] else None