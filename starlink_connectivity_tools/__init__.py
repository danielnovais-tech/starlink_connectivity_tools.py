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
"""Starlink Connectivity Tools - Python library for interacting with Starlink dish gRPC API."""

__version__ = "0.1.0"

from .client import StarlinkDishClient

__all__ = ["StarlinkDishClient"]
"""
Starlink Connectivity Tools - Python library for interacting with Starlink API
"""

from .client import StarlinkClient
from .accounts import AccountsAPI
from .addresses import AddressesAPI
from .data_usage import DataUsageAPI
from .routers import RoutersAPI
from .service_lines import ServiceLinesAPI
from .subscriptions import SubscriptionsAPI
from .user_terminals import UserTerminalsAPI
from .tls import TLSAPI

__version__ = "0.1.0"
__all__ = [
    "StarlinkClient",
    "AccountsAPI",
    "AddressesAPI",
    "DataUsageAPI",
    "RoutersAPI",
    "ServiceLinesAPI",
    "SubscriptionsAPI",
    "UserTerminalsAPI",
    "TLSAPI",
]
Starlink Connectivity Tools

A Python library for monitoring and managing Starlink dish connectivity.
A Python library for working with Starlink connectivity.
"""Starlink Connectivity Tools - Connection failover and management utilities."""

from .failover import FailoverHandler

__version__ = "0.1.0"
__all__ = ["FailoverHandler"]
"""
Starlink Connectivity Tools
A Python library for managing and monitoring Starlink connectivity.
"""

__version__ = "0.1.0"

from .dish import StarlinkDish
from .exceptions import StarlinkConnectionError, StarlinkEmergencyError

__all__ = [
    "StarlinkDish",
    "StarlinkConnectionError",
    "StarlinkEmergencyError",
]
from .connectivity import StarlinkConnectivity
from .utils import check_connection, format_speed

__all__ = ["StarlinkConnectivity", "check_connection", "format_speed"]
from .starlink_dish import StarlinkDish
from .emergency_mode import EmergencyMode

__all__ = ["StarlinkDish", "EmergencyMode"]
