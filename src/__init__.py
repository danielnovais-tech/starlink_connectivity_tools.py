"""
Starlink Connectivity Tools
"""

__version__ = '0.1.0'
Starlink Connectivity Tools - Core Modules
"""

__version__ = "1.0.0"
Starlink Connectivity Tools Package
"""

__version__ = "0.1.0"
"""Starlink Connectivity Tools - Core Implementation"""

from .power_manager import PowerManager, PowerMode, PowerProfile

__all__ = ['PowerManager', 'PowerMode', 'PowerProfile']
"""
Starlink Connectivity Tools
"""
from .failover_handler import (
    FailoverHandler,
    BackupConnection,
    FailoverStrategy
)

__all__ = [
    'FailoverHandler',
    'BackupConnection',
    'FailoverStrategy'
"""Starlink connectivity tools package"""
"""
Starlink Connectivity Tools
Main package for satellite connectivity optimization
"""

A Python library for managing Starlink connections, optimizing bandwidth,
handling failover scenarios, and managing power consumption.
"""

__version__ = "0.1.0"

from .connection_manager import ConnectionManager
from .bandwidth_optimizer import BandwidthOptimizer
from .failover_handler import FailoverHandler
from .power_manager import PowerManager
from .diagnostics import Diagnostics

__all__ = [
    "ConnectionManager",
    "BandwidthOptimizer",
    "FailoverHandler",
    "PowerManager",
    "Diagnostics",
]
