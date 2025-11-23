import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class HistoryManager:

    def __init__(self):
        self.data_dir = Path.home() / '.debugbuddy'
        self.data_dir.mkdir(exist_ok=True)
        self.history_file = self.data_dir / 'history.json'

    def add(self, error: Dict, explanation: Dict):

        history = self._load()

        entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error.get('type', 'Unknown'),
            'message': error.get('message', '')[:200],
            'file': error.get('file'),
            'line': error.get('line'),
            'language': error.get('language', 'unknown'),
            'simple': explanation.get('simple', '')[:100],
            'fix': explanation.get('fix', '')[:200],
        }

        history.append(entry)

        if len(history) > 100:
            history = history[-100:]

        self._save(history)

    def get_recent(self, limit: int = 10) -> List[Dict]:

        history = self._load()
        return history[-limit:][::-1]

    def find_similar(self, error: Dict) -> Optional[Dict]:

        history = self._load()
        error_type = error.get('type', '').lower()

        for entry in reversed(history):
            if entry['error_type'].lower() == error_type:
                return entry

        return None

    def search(self, keyword: str) -> List[Dict]:

        history = self._load()
        keyword_lower = keyword.lower()

        results = []
        for entry in history:
            searchable = [
                entry['error_type'],
                entry['message'],
                entry['simple'],
            ]

            if any(keyword_lower in str(field).lower() for field in searchable):
                results.append(entry)

        return results

    def clear(self):
        self._save([])

    def get_stats(self) -> Dict:

        history = self._load()

        if not history:
            return {
                'total': 0,
                'by_type': {},
                'by_language': {},
            }

        stats = {
            'total': len(history),
            'by_type': {},
            'by_language': {},
        }

        for entry in history:
            error_type = entry['error_type']
            language = entry.get('language', 'unknown')

            stats['by_type'][error_type] = stats['by_type'].get(error_type, 0) + 1
            stats['by_language'][language] = stats['by_language'].get(language, 0) + 1

        return stats

    def _load(self) -> List[Dict]:

        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save(self, history: List[Dict]):

        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save history: {e}")