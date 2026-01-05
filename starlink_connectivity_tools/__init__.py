"""
Starlink Connectivity Tools

A Python library for working with Starlink connectivity.
"""

__version__ = "0.1.0"

from .connectivity import StarlinkConnectivity
from .utils import check_connection, format_speed

__all__ = ["StarlinkConnectivity", "check_connection", "format_speed"]
