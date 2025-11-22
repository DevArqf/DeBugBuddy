import json
from pathlib import Path
from typing import Dict, List

class ErrorExplainer:
    """Explain errors using pattern matching"""
    
    def __init__(self):
        self.patterns = self._load_patterns()
    
    def _load_patterns(self) -> Dict:
        """Load error patterns from JSON files"""
        
        patterns = {}
        pattern_dir = Path(__file__).parent.parent / 'patterns'
        
        for pattern_file in pattern_dir.glob('*.json'):
            try:
                with open(pattern_file, 'r') as f:
                    patterns[pattern_file.stem] = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load {pattern_file}: {e}")
        
        return patterns
    
    def explain(self, parsed_error: Dict) -> Dict:
        """Generate human-friendly explanation"""
        
        error_type = parsed_error.get('type', '').lower()
        language = parsed_error.get('language', 'common')
        message = parsed_error.get('message', '')
        
        explanation = self._match_pattern(error_type, message, language)
        
        if not explanation:
            explanation = self._generic_explanation(parsed_error)
        
        return explanation
    
    def _match_pattern(self, error_type: str, message: str, language: str) -> Dict:
        """Match error against known patterns"""
        
        if language in self.patterns:
            for pattern in self.patterns[language].get('errors', []):
                if self._matches(error_type, message, pattern):
                    return pattern
        
        if 'common' in self.patterns:
            for pattern in self.patterns['common'].get('errors', []):
                if self._matches(error_type, message, pattern):
                    return pattern
        
        return None
    
    def _matches(self, error_type: str, message: str, pattern: Dict) -> bool:
        """Check if error matches pattern"""
        
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
        """Generate generic explanation for unknown errors"""
        
        error_type = parsed_error.get('type', 'Unknown Error')
        message = parsed_error.get('message', '')
        
        templates = {
            'syntax': {
                'simple': "There's a syntax mistake in your code.",
                'fix': "Check the line mentioned for typos, missing brackets, or incorrect indentation."
            },
            'name': {
                'simple': "You're using a variable or function that doesn't exist.",
                'fix': "Make sure you've defined it or imported it correctly."
            },
            'type': {
                'simple': "You're trying to do something with the wrong type of data.",
                'fix': "Check the types of your variables. You might be mixing strings, numbers, or None."
            },
            'import': {
                'simple': "Python can't find the module you're trying to import.",
                'fix': "Install it with: pip install <module_name>"
            },
            'attribute': {
                'simple': "You're trying to access something that doesn't exist on this object.",
                'fix': "Check if the attribute exists or if the object is None."
            },
        }
        
        for key, template in templates.items():
            if key in error_type.lower():
                return template
        
        # fallback
        return {
            'simple': f"{error_type}: {message[:100]}",
            'fix': "Check the error message and the line number. Review your recent changes."
        }
    
    def search_patterns(self, keyword: str) -> List[Dict]:
        """Search patterns by keyword"""
        
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
                        'description': pattern.get('simple', ''),
                        'language': lang
                    })
        
        return results
    
    def get_related_errors(self, error_type: str) -> List[str]:
        """Get list of related error types"""
        
        related = {
            'syntax': ['IndentationError', 'TabError'],
            'name': ['AttributeError', 'ImportError'],
            'type': ['ValueError', 'AttributeError'],
        }
        
        error_lower = error_type.lower()
        for key, errors in related.items():
            if key in error_lower:
                return errors
        
        return []