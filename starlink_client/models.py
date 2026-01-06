"""Data models for Starlink network statistics and device information."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class NetworkStats:
    """Network statistics from Starlink dish.
    
    Attributes:
        download_speed: Download speed in Mbps
        upload_speed: Upload speed in Mbps
        latency: Latency in milliseconds
        uptime: Device uptime in seconds
        obstruction_percentage: Percentage of time obstructed
        connected: Whether the dish is connected to satellites
    """
    download_speed: float
    upload_speed: float
    latency: float
    uptime: Optional[int] = None
    obstruction_percentage: Optional[float] = None
    connected: bool = True
