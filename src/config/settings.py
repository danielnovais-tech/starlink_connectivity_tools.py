"""
Configuration Settings
Configuration Settings Module

Centralized configuration for Starlink connectivity tools.
"""

import os
from typing import Dict, Any


class Settings:
    """Application settings."""
    
    # Starlink Configuration
    STARLINK_ENDPOINT = os.getenv("STARLINK_ENDPOINT", "192.168.100.1")
    STARLINK_GRPC_PORT = int(os.getenv("STARLINK_GRPC_PORT", "9200"))
    
    # Network Configuration
    PING_TIMEOUT = 5
    CONNECTION_RETRY_MAX = 3
    CONNECTION_RETRY_DELAY = 2
    
    # Monitoring Configuration
    MONITOR_INTERVAL_SECONDS = 30
    METRICS_HISTORY_SIZE = 100
    
    # Power Management
    DEFAULT_POWER_MODE = "normal"
    BATTERY_CAPACITY_WH = 1000.0
    
    # Bandwidth Configuration
    DEFAULT_BANDWIDTH_PROFILE = "normal"
    MAX_DOWNLOAD_MBPS = 200.0
    MAX_UPLOAD_MBPS = 40.0
    
    # Alert Thresholds
    ALERT_SIGNAL_QUALITY_MIN = 70
    ALERT_LATENCY_MAX_MS = 100
    ALERT_PACKET_LOSS_MAX_PERCENT = 2.0
    ALERT_OBSTRUCTION_MAX_PERCENT = 5.0
    ALERT_DOWNLOAD_SPEED_MIN_MBPS = 50.0
    
    # Failover Configuration
    PRIMARY_CONNECTION = "starlink"
    BACKUP_CONNECTIONS = ["cellular", "ethernet"]
    FAILOVER_CHECK_INTERVAL = 60
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """
        Convert settings to dictionary.
        
        Returns:
            dict: Settings as dictionary
        """
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("_") and key.isupper()
        }
    
    @classmethod
    def update_from_dict(cls, config: Dict[str, Any]) -> None:
        """
        Update settings from dictionary.
        
        Args:
            config: Configuration dictionary
        """
        for key, value in config.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
# Default configuration settings
DEFAULT_CONFIG = {
    "connection": {
        "timeout": 30,
        "retry_attempts": 3,
        "retry_delay": 5,
    },
    "bandwidth": {
        "default_limit": None,  # No limit
        "optimization_enabled": False,
    },
    "failover": {
        "enabled": False,
        "backup_connections": [],
        "auto_failover": True,
        "health_check_interval": 60,
    },
    "power": {
        "default_mode": "normal",
        "low_power_threshold": 20,  # Battery percentage
    },
    "diagnostics": {
        "log_level": "INFO",
        "enable_monitoring": True,
        "test_interval": 300,  # seconds
    },
}


class Settings:
    """Manages application settings."""

    def __init__(self, custom_config=None):
        """
        Initialize Settings with optional custom configuration.

        Args:
            custom_config: Optional dictionary with custom settings
        """
        self.config = DEFAULT_CONFIG.copy()
        if custom_config:
            self.update(custom_config)

    def get(self, key, default=None):
        """
        Get a configuration value.

        Args:
            key: Configuration key (supports dot notation, e.g., 'connection.timeout')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        if not key or not isinstance(key, str):
            return default
        
        keys = [k for k in key.split(".") if k]  # Filter out empty strings
        if not keys:
            return default
            
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value

    def set(self, key, value):
        """
        Set a configuration value.

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set

        Returns:
            bool: True if set successfully, False if key is invalid
        """
        if not key or not isinstance(key, str):
            return False
            
        keys = [k for k in key.split(".") if k]  # Filter out empty strings
        if not keys:
            return False
            
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        return True

    def update(self, config_dict):
        """
        Update configuration with a dictionary.

        Args:
            config_dict: Dictionary with configuration updates

        Returns:
            bool: True if updated successfully
        """
        self._deep_update(self.config, config_dict)
        return True

    def _deep_update(self, base_dict, update_dict):
        """
        Recursively update nested dictionaries.

        Args:
            base_dict: Base dictionary to update
            update_dict: Dictionary with updates
        """
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value

    def reset(self):
        """
        Reset configuration to defaults.

        Returns:
            bool: True if reset successfully
        """
        self.config = DEFAULT_CONFIG.copy()
        return True

    def get_all(self):
        """
        Get all configuration settings.

        Returns:
            dict: All configuration settings
        """
        return self.config.copy()
