"""
Configuration management for Starlink Monitor
"""

import json
import os
from typing import Dict, Any


DEFAULT_CONFIG = {
    "thresholds": {
        "min_download_speed": 25.0,  # Mbps
        "max_latency": 100.0,  # ms
        "max_packet_loss": 5.0,  # %
        "max_obstruction": 10.0,  # %
    },
    "logging": {
        "level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": None,  # Set to a path to enable file logging
    },
    "monitor": {
        "default_host": "192.168.100.1",
        "history_size": 1000,
        "default_interval": 60,
    }
}


class Config:
    """Configuration manager for Starlink Monitor"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to config file. If None, uses default config.
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default config file path"""
        # Try to use user's home directory
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".config", "starlink_monitor")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "config.json")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults to ensure all keys exist
                config = DEFAULT_CONFIG.copy()
                for key in loaded_config:
                    if isinstance(loaded_config[key], dict) and key in config:
                        config[key].update(loaded_config[key])
                    else:
                        config[key] = loaded_config[key]
                return config
            except Exception as e:
                print(f"Warning: Failed to load config from {self.config_path}: {e}")
                print("Using default configuration")
                return DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Dict[str, Any] = None):
        """
        Save configuration to file
        
        Args:
            config: Configuration to save. If None, saves current config.
        """
        config_to_save = config or self.config
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
        except Exception as e:
            print(f"Error: Failed to save config to {self.config_path}: {e}")
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def get_thresholds(self) -> Dict[str, float]:
        """Get threshold configuration"""
        return self.config.get('thresholds', DEFAULT_CONFIG['thresholds'])
    
    def set_thresholds(self, **kwargs):
        """Set threshold values"""
        for key, value in kwargs.items():
            if key in self.config['thresholds']:
                self.config['thresholds'][key] = value
        self.save_config()
