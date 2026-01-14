import json
from pathlib import Path
from typing import Dict, List, Optional

class PatternManager:
    def __init__(self, pattern_dir: Optional[Path] = None, custom_dir: Optional[Path] = None):
        self.pattern_dir = pattern_dir or (Path(__file__).parent.parent.parent / 'patterns')
        self.custom_dir = custom_dir or (Path.home() / '.debugbuddy' / 'patterns' / 'custom')
        self._cache: Dict[Path, Dict[str, object]] = {}
        self.extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.c': 'c',
            '.h': 'c',
            '.cpp': 'c',
            '.hpp': 'c',
            '.php': 'php',
            '.java': 'java',
            '.rb': 'ruby',
        }

    def available_languages(self) -> List[str]:
        return sorted(p.stem for p in self.pattern_dir.glob('*.json'))

    def get_language_for_file(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        if suffix in self.extension_map:
            return self.extension_map[suffix]
        if suffix:
            lang = suffix.lstrip('.')
            if (self.pattern_dir / f'{lang}.json').exists():
                return lang
        return 'unknown'

    def load_patterns(self, language: Optional[str] = None, include_custom: bool = True):
        if language:
            return self._load_language(language, include_custom)

        patterns: Dict[str, List[dict]] = {}
        for file in self.pattern_dir.glob('*.json'):
            patterns[file.stem] = list(self._load_file_errors(file))

        if include_custom and self.custom_dir.exists():
            for file in self.custom_dir.glob('*.json'):
                patterns.setdefault(file.stem, [])
                patterns[file.stem].extend(self._load_file_errors(file))

        return patterns

    def save_patterns(self, language: str, patterns: List[dict], custom: bool = False):
        target_dir = self.custom_dir if custom else self.pattern_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        file = target_dir / f'{language}.json'
        with open(file, 'w', encoding='utf-8') as f:
            json.dump({'errors': patterns}, f, indent=2)

    def _load_language(self, language: str, include_custom: bool) -> List[dict]:
        errors = list(self._load_file_errors(self.pattern_dir / f'{language}.json'))
        if include_custom:
            errors.extend(self._load_file_errors(self.custom_dir / f'{language}.json'))
        return errors

    def _load_file_errors(self, file_path: Path) -> List[dict]:
        if not file_path.exists():
            return []
        mtime = file_path.stat().st_mtime
        cached = self._cache.get(file_path)
        if cached and cached['mtime'] == mtime:
            return cached['errors']
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        errors = data.get('errors', [])
        self._cache[file_path] = {'mtime': mtime, 'errors': errors}
        return errors
