"""Starlink Connectivity Tools.

Crisis-optimized satellite connectivity management.
"""

__version__ = "0.1.0"
__author__ = "Daniel Novais"

# Import available modules only
try:
    from .client import StarlinkClient
except ImportError:
    StarlinkClient = None

try:
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
except ImportError:
    DeviceStatus = NetworkStats = TelemetryData = DeviceLocation = None
    WiFiStatus = WiFiConfig = DishConfig = AccountData = None
    Alert = AlertLevel = DeviceState = WiFiClient = HistoricalData = None

try:
    from .failover import FailoverHandler
except ImportError:
    FailoverHandler = None

try:
    from .dish import StarlinkDish
except ImportError:
    StarlinkDish = None

try:
    from .exceptions import StarlinkConnectionError, StarlinkEmergencyError
except ImportError:
    StarlinkConnectionError = StarlinkEmergencyError = None

try:
    from .connectivity import StarlinkConnectivity
except ImportError:
    StarlinkConnectivity = None

try:
    from .utils import check_connection, format_speed
except ImportError:
    check_connection = format_speed = None

try:
    from .starlink_dish import StarlinkDish as DishClient
except ImportError:
    DishClient = None

try:
    from .emergency_mode import EmergencyMode
except ImportError:
    EmergencyMode = None

# Export available items
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
    "FailoverHandler",
    "StarlinkDish",
    "StarlinkConnectionError",
    "StarlinkEmergencyError",
    "StarlinkConnectivity",
    "check_connection",
    "format_speed",
    "DishClient",
    "EmergencyMode",
]
