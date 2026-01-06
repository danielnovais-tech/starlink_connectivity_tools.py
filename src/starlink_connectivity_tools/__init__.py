"""Starlink Connectivity Tools - Crisis-optimized satellite connectivity management."""

__version__ = "0.1.0"
__author__ = "Daniel Novais"

from .starlink_api import StarlinkAPI
from .satellite_connection_manager import SatelliteConnectionManager
from .crisis_monitor import CrisisMonitor
from .diagnostics import DiagnosticsEngine

__all__ = [
    "StarlinkAPI",
    "SatelliteConnectionManager",
    "CrisisMonitor",
    "DiagnosticsEngine",
]
