"""
Starlink Connectivity Tools

A comprehensive suite of tools for managing Starlink satellite internet connections,
including connection management, bandwidth optimization, failover handling, and power management.
"""

__version__ = "0.1.0"
__author__ = "Daniel Novais"

from .connection_manager import ConnectionManager
from .bandwidth_optimizer import BandwidthOptimizer
from .failover_handler import FailoverHandler
from .power_manager import PowerManager
from .diagnostics import Diagnostics
from .starlink_monitor import StarlinkMonitor

__all__ = [
    "ConnectionManager",
    "BandwidthOptimizer",
    "FailoverHandler",
    "PowerManager",
    "Diagnostics",
    "StarlinkMonitor",
]
