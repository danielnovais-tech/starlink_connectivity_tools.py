"""
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
