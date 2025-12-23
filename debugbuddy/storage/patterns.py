import json
from pathlib import Path

class PatternManager:
    def load_patterns(self, language=None):
        pattern_dir = Path(__file__).parent.parent.parent / 'patterns'
        if language:
            file = pattern_dir / f'{language}.json'
            if file.exists():
                with open(file, 'r') as f:
                    return json.load(f)['errors']
        else:
            # Load all
            patterns = {}
            for file in pattern_dir.glob('*.json'):
                with open(file, 'r') as f:
                    patterns[file.stem] = json.load(f)['errors']
            return patterns
    # Add save etc.