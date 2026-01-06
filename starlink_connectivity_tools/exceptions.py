"""
Exceptions for Starlink Connectivity Tools
"""


class StarlinkConnectionError(Exception):
    """Raised when unable to connect to Starlink dish"""
    pass


class StarlinkEmergencyError(Exception):
    """Raised when an emergency condition is detected"""
    pass
