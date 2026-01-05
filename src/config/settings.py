"""
Configuration Settings

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
