"""
Starlink Connectivity Tools

A Python library for interacting with Starlink user terminals.
Provides methods for device management, network monitoring, and configuration.
"""

from .client import StarlinkClient
from .models import (
    DeviceStatus,
    NetworkStats,
    TelemetryData,
    DeviceLocation,
    WiFiStatus,
    WiFiConfig,
    DishConfig,
    AccountData,
    Alert,
    AlertLevel,
    DeviceState,
    WiFiClient,
    HistoricalData,
)

__version__ = "0.1.0"

__all__ = [
    "StarlinkClient",
    "DeviceStatus",
    "NetworkStats",
    "TelemetryData",
    "DeviceLocation",
    "WiFiStatus",
    "WiFiConfig",
    "DishConfig",
    "AccountData",
    "Alert",
    "AlertLevel",
    "DeviceState",
    "WiFiClient",
    "HistoricalData",
]
