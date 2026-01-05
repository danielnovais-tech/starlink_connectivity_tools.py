"""
Starlink Connectivity Tools

A Python library for monitoring and managing Starlink dish connectivity.
"""

__version__ = "0.1.0"

from .dish import StarlinkDish
from .exceptions import StarlinkConnectionError, StarlinkEmergencyError

__all__ = [
    "StarlinkDish",
    "StarlinkConnectionError",
    "StarlinkEmergencyError",
]
