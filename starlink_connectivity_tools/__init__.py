"""
Starlink Connectivity Tools - Python library for interacting with Starlink API
"""

from .client import StarlinkClient
from .accounts import AccountsAPI
from .addresses import AddressesAPI
from .data_usage import DataUsageAPI
from .routers import RoutersAPI
from .service_lines import ServiceLinesAPI
from .subscriptions import SubscriptionsAPI
from .user_terminals import UserTerminalsAPI
from .tls import TLSAPI

__version__ = "0.1.0"
__all__ = [
    "StarlinkClient",
    "AccountsAPI",
    "AddressesAPI",
    "DataUsageAPI",
    "RoutersAPI",
    "ServiceLinesAPI",
    "SubscriptionsAPI",
    "UserTerminalsAPI",
    "TLSAPI",
]
