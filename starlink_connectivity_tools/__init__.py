"""
Starlink Connectivity Tools - Python library for interacting with Starlink user terminals.

This library provides wrappers for common Starlink gRPC methods to manage and monitor
Starlink dishes, including status retrieval, configuration, and network management.
"""

from .client import StarlinkClient

__version__ = "0.1.0"
__all__ = ["StarlinkClient"]
