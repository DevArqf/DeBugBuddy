import json
import difflib
from pathlib import Path
from typing import Dict, List, Optional

class ErrorExplainer:

    def __init__(self):
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> Dict:

        patterns = {}
        pattern_dir = Path(__file__).parent.parent / 'patterns'

        for pattern_file in pattern_dir.glob('*.json'):
            try:
                with open(pattern_file, 'r', encoding='utf-8') as f:
                    patterns[pattern_file.stem] = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load {pattern_file}: {e}")

        return patterns

    def explain(self, parsed_error: Dict) -> Dict:

        error_type = parsed_error.get('type', '').lower()
        language = parsed_error.get('language', 'common')
        message = parsed_error.get('message', '')

        explanation = self._match_pattern(error_type, message, language)

        if not explanation:
            explanation = self._generic_explanation(parsed_error)

        if 'name' in error_type.lower() and 'not defined' in message.lower():
            explanation['suggestions'] = self._get_name_suggestions(message, parsed_error)

        return explanation

    def _match_pattern(self, error_type: str, message: str, language: str) -> Optional[Dict]:

        if language in self.patterns:
            for pattern in self.patterns[language].get('errors', []):
                if self._matches(error_type, message, pattern):
                    return pattern.copy()

        if 'common' in self.patterns:
            for pattern in self.patterns['common'].get('errors', []):
                if self._matches(error_type, message, pattern):
                    return pattern.copy()

        return None

    def _matches(self, error_type: str, message: str, pattern: Dict) -> bool:

        pattern_type = pattern.get('type', '').lower()
        keywords = pattern.get('keywords', [])

        if pattern_type and pattern_type in error_type:
            return True

        message_lower = message.lower()
        for keyword in keywords:
            if keyword.lower() in message_lower:
                return True

        return False

    def _generic_explanation(self, parsed_error: Dict) -> Dict:

        error_type = parsed_error.get('type', 'Unknown Error')
        message = parsed_error.get('message', '')

        templates = {
            'syntax': {
                'simple': "🔍 There's a syntax mistake in your code.",
                'fix': "Check the line mentioned for:\n  • Typos or misspellings\n  • Missing brackets, quotes, or colons\n  • Incorrect indentation",
                'example': None
            },
            'name': {
                'simple': "🔍 You're using something that doesn't exist or wasn't imported.",
                'fix': "Make sure you:\n  • Defined it before using it\n  • Spelled it correctly\n  • Imported it if it's from a module",
                'example': None
            },
            'type': {
                'simple': "🔍 You're mixing incompatible data types or using something incorrectly.",
                'fix': "Check:\n  • Are you mixing strings and numbers?\n  • Using the right function arguments?\n  • Object types match what you expect?",
                'example': None
            },
            'import': {
                'simple': "🔍 Python can't find the module you're trying to import.",
                'fix': "Try:\n  • pip install <module_name>\n  • Check spelling\n  • Verify virtual environment is active",
                'example': None
            },
            'attribute': {
                'simple': "🔍 You're trying to access something that doesn't exist on this object.",
                'fix': "Debug:\n  • Check if object is None\n  • Verify attribute name\n  • Print object to see what it is",
                'example': None
            },
        }

        for key, template in templates.items():
            if key in error_type.lower():
                return template

        return {
            'simple': f"🔍 {error_type}: {message[:100]}",
            'fix': "Debug steps:\n  • Read the error message carefully\n  • Check the line number mentioned\n  • Review your recent changes\n  • Search the error online if needed",
            'example': None
        }

    def _get_name_suggestions(self, message: str, parsed_error: Dict) -> List[str]:

        import re
        match = re.search(r"name ['\"]([^'\"]+)['\"]", message)
        if not match:
            return []

        undefined_name = match.group(1)

        suggestions = []

        builtins = [
            'print', 'len', 'range', 'list', 'dict', 'str', 'int', 'float',
            'True', 'False', 'None', 'input', 'open', 'max', 'min', 'sum',
            'abs', 'all', 'any', 'enumerate', 'zip', 'map', 'filter'
        ]

        close_matches = difflib.get_close_matches(
            undefined_name, 
            builtins, 
            n=3, 
            cutoff=0.6
        )

        if close_matches:
            suggestions.extend([f"Did you mean: {match}?" for match in close_matches])

        if not suggestions:
            suggestions = [
                f"Check spelling of '{undefined_name}'",
                f"Did you forget to define '{undefined_name}'?",
                f"Need to import '{undefined_name}'?"
            ]

        return suggestions

    def search_patterns(self, keyword: str) -> List[Dict]:

        results = []
        keyword_lower = keyword.lower()

        for lang, data in self.patterns.items():
            for pattern in data.get('errors', []):
                searchable = [
                    pattern.get('type', ''),
                    pattern.get('simple', ''),
                    pattern.get('fix', ''),
                ] + pattern.get('keywords', [])

                if any(keyword_lower in str(field).lower() for field in searchable):
                    results.append({
                        'name': pattern.get('type', 'Unknown'),
                        'description': pattern.get('simple', '').replace('🔍 ', ''),
                        'language': lang
                    })

        return results

    def get_related_errors(self, error_type: str) -> List[str]:

        related = {
            'syntax': ['IndentationError', 'TabError', 'EOFError'],
            'name': ['AttributeError', 'ImportError', 'UnboundLocalError'],
            'type': ['ValueError', 'AttributeError', 'KeyError'],
            'import': ['ModuleNotFoundError', 'ImportError'],
            'index': ['KeyError', 'ValueError'],
            'attribute': ['TypeError', 'NameError'],
        }

        error_lower = error_type.lower()
        for key, errors in related.items():
            if key in error_lower:
                return errors

        return []

    def get_code_example(self, error_type: str) -> Optional[str]:

        for lang, data in self.patterns.items():
            for pattern in data.get('errors', []):
                if error_type.lower() in pattern.get('type', '').lower():
                    return pattern.get('example')

        return None