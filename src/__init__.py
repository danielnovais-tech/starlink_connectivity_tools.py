"""
Starlink Connectivity Tools
"""
from .failover_handler import (
    FailoverHandler,
    BackupConnection,
    FailoverStrategy
)

__all__ = [
    'FailoverHandler',
    'BackupConnection',
    'FailoverStrategy'
]
