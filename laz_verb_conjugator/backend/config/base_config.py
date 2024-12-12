from typing import Dict, Any, Optional
from pathlib import Path
import yaml
import os
from threading import Lock

class LazuriConfig:
    """Base configuration class for Lazuri Conjugator."""
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LazuriConfig, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if not self._initialized:
            self._config: Dict[str, Any] = {}
            self._config_file: Optional[Path] = None
            self._initialized = True
            self._load_default_config()

    def _load_default_config(self) -> None:
        """Load default configuration settings."""
        self._config = {
            'data_file': 'data/verb_data.csv',
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file': 'logs/lazuri.log'
            },
            'cache': {
                'enabled': True,
                'max_size': 1000,
                'ttl': 3600  # Time to live in seconds
            },
            'regions': ['FA', 'PZ', 'AŞ', 'HO'],
            'supported_tenses': ['present', 'past', 'future', 'past_progressive'],
            'supported_aspects': ['potential', 'passive']
        }

    def load_config(self, config_file: Path) -> None:
        """
        Load configuration from a YAML file.
        
        Args:
            config_file: Path to the configuration file
        
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid
        """
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
            
        with config_file.open('r', encoding='utf-8') as f:
            loaded_config = yaml.safe_load(f)
            
        # Deep update current config
        self._deep_update(self._config, loaded_config)
        self._config_file = config_file

    def _deep_update(self, base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> None:
        """Recursively update a dictionary."""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict:
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (dot notation supported)
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        try:
            value = self._config
            for k in key.split('.'):
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key (dot notation supported)
            value: Value to set
        """
        with self._lock:
            keys = key.split('.')
            target = self._config
            for k in keys[:-1]:
                target = target.setdefault(k, {})
            target[keys[-1]] = value

    def save(self) -> None:
        """Save current configuration to file if one was loaded."""
        if self._config_file:
            with self._config_file.open('w', encoding='utf-8') as f:
                yaml.safe_dump(self._config, f, allow_unicode=True)

    @property
    def all(self) -> Dict[str, Any]:
        """Get complete configuration dictionary."""
        return self._config.copy()