"""
Starlink Connectivity Tools - A Python library for managing Starlink satellite connectivity.

This library provides tools for bandwidth optimization, connection management,
and prioritized data transmission over Starlink networks.
"""

from .optimizer import BandwidthOptimizer

__version__ = "0.1.0"
__all__ = ["BandwidthOptimizer"]
