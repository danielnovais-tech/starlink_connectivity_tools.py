"""Starlink Client - A Python library for interacting with Starlink satellite internet devices."""

from .client import StarlinkClient
from .models import NetworkStats

__version__ = "0.1.0"
__all__ = ["StarlinkClient", "NetworkStats"]
