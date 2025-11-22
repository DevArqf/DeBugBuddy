import json
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    """Manage user configuration"""
    
    DEFAULT_CONFIG = {
        'verbose': False,
        'auto_save_history': True,
        'color_output': True,
        'max_history': 100,
        'ai_provider': None,  # 'openai' or 'anthropic'
        'openai_api_key': None,
        'anthropic_api_key': None,
        'ai_model': 'gpt-4',
        'default_language': 'python',
        'watch_exclude': ['__pycache__', '.git', 'node_modules', '.venv'],
    }
    
    def __init__(self):
        self.data_dir = Path.home() / '.debugbuddy'
        self.data_dir.mkdir(exist_ok=True)
        self.config_file = self.data_dir / 'config.json'
        self._ensure_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        
        config = self._load()
        return config.get(key, default)
    
    def get_all(self) -> Dict:
        """Get all configuration values"""
        
        return self._load()
    
    def set(self, key: str, value: Any):
        """Set a configuration value"""
        
        config = self._load()
        
        # type conversion for common values
        if key in ['verbose', 'auto_save_history', 'color_output']:
            value = self._parse_bool(value)
        elif key in ['max_history']:
            value = int(value)
        
        config[key] = value
        self._save(config)
    
    def reset(self):
        """Reset configuration to defaults"""
        
        self._save(self.DEFAULT_CONFIG.copy())
    
    def _ensure_config(self):
        """Ensure config file exists with defaults"""
        
        if not self.config_file.exists():
            self._save(self.DEFAULT_CONFIG.copy())
    
    def _load(self) -> Dict:
        """Load configuration from file"""
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # merge with defaults (in case new keys were added)
            merged = self.DEFAULT_CONFIG.copy()
            merged.update(config)
            return merged
            
        except (json.JSONDecodeError, IOError):
            return self.DEFAULT_CONFIG.copy()
    
    def _save(self, config: Dict):
        """Save configuration to file"""
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save config: {e}")
    
    @staticmethod
    def _parse_bool(value: Any) -> bool:
        """Parse boolean value from string or bool"""
        
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            return value.lower() in ['true', '1', 'yes', 'on']
        
        return bool(value)