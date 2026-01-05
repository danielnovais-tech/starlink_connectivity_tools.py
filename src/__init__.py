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
