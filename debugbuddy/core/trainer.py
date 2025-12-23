from typing import Dict, List
from pathlib import Path
from ..models.training import TrainingData
from ..models.pattern import Pattern
from ..storage.patterns import PatternManager

class PatternTrainer:
    def __init__(self, storage_manager):
        self.storage = storage_manager
        self.custom_patterns_dir = Path.home() / '.debugbuddy' / 'patterns' / 'custom'
        self.custom_patterns_dir.mkdir(parents=True, exist_ok=True)
        self.pattern_mgr = PatternManager()
    
    def add_training_example(self, error_text: str, explanation: str, 
                            fix: str, language: str) -> bool:
        training_data = TrainingData(
            error_text=error_text,
            explanation=explanation,
            fix=fix,
            language=language
        )
        return self.storage.save_training_data(training_data)
    
    def train_pattern(self, training_examples: List[TrainingData]) -> Pattern:
        keywords = self._extract_keywords(training_examples)
        
        pattern = Pattern(
            type=self._determine_error_type(training_examples),
            keywords=keywords,
            simple=self._generate_explanation(training_examples),
            fix=self._generate_fix(training_examples),
            language=training_examples[0].language
        )
        
        self._save_custom_pattern(pattern)
        
        return pattern
    
    def _extract_keywords(self, examples: List[TrainingData]) -> List[str]:
        keywords = set()
        for ex in examples:
            words = re.findall(r'\w+', ex.error_text.lower())
            keywords.update(words)
        return list(keywords)[:10]
    
    def _determine_error_type(self, examples: List[TrainingData]) -> str:
        return re.search(r'(\w+Error)', examples[0].error_text) .group(1) if re.search else 'Unknown'
    
    def _generate_explanation(self, examples: List[TrainingData]) -> str:
        return examples[0].explanation
    
    def _generate_fix(self, examples: List[TrainingData]) -> str:
        return examples[0].fix
    
    def _save_custom_pattern(self, pattern: Pattern):
        lang_dir = self.custom_patterns_dir / f"{pattern.language}.json"
        patterns = self.pattern_mgr.load_patterns(pattern.language) or []
        patterns.append(pattern.__dict__)
        with open(lang_dir, 'w') as f:
            json.dump({'errors': patterns}, f)
    
    def list_custom_patterns(self) -> List[Pattern]:
        patterns = []
        for file in self.custom_patterns_dir.glob('*.json'):
            with open(file, 'r') as f:
                data = json.load(f)
                for p in data.get('errors', []):
                    patterns.append(Pattern(**p))
        return patterns
    
    def delete_custom_pattern(self, pattern_id: str) -> bool:
        for file in self.custom_patterns_dir.glob('*.json'):
            with open(file, 'r') as f:
                data = json.load(f)
            errors = [p for p in data['errors'] if p['type'] + p['language'] != pattern_id]
            if len(errors) < len(data['errors']):
                with open(file, 'w') as f:
                    json.dump({'errors': errors}, f)
                return True
        return False