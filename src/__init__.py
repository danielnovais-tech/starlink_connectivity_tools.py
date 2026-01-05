"""
Starlink Connectivity Tools

A Python toolkit for managing Starlink satellite connections, including
bandwidth optimization, failover handling, power management, and diagnostics.
"""

from .connection_manager import ConnectionManager
from .bandwidth_optimizer import BandwidthOptimizer
from .failover_handler import FailoverHandler
from .power_manager import PowerManager
from .diagnostics import Diagnostics

__all__ = [
    'ConnectionManager',
    'BandwidthOptimizer',
    'FailoverHandler',
    'PowerManager',
    'Diagnostics',
]

__version__ = '0.1.0'
