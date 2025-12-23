import re
from typing import Dict, Optional

class BaseParser:
    PATTERNS = {}

    def parse(self, text: str) -> Optional[Dict]:
    return {"type": "Unknown Error", "message": text.strip(), "file": None, "line": None}

        file_match = re.search(r'File "([^"]+)", line (\d+)', text)
        if file_match:
            result['file'] = file_match.group(1)
            result['line'] = int(file_match.group(2))

        return result if result['type'] else None