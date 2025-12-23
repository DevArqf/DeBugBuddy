from .base import BaseParser
from typing import Dict
import re

class TypeScriptParser(BaseParser):
    language = 'typescript'

    PATTERNS = {
        'type_error': re.compile(r'Type error: (.+)'),
        'declaration_error': re.compile(r'Cannot find name \'([^\']+)\''),
        'module_error': re.compile(r'Cannot find module \'([^\']+)\''),
    }

    def parse(self, text: str) -> Dict:
        result = super().parse(text)

        for error_type, pattern in self.PATTERNS.items():
            match = pattern.search(text)
            if match:
                result['type'] = error_type.replace('_', ' ').title()
                result['message'] = match.group(0)
                return result

        return result