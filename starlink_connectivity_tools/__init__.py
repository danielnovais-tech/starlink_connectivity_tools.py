"""
Starlink Connectivity Tools

A Python package for interacting with Starlink-related APIs.
"""

__version__ = "0.1.0"

from .space_safety_api import SpaceSafetyAPI

__all__ = ["SpaceSafetyAPI", "__version__"]
