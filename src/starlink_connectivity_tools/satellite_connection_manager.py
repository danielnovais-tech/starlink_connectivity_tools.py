"""Unified satellite connection management with automatic failover."""

import time
import random
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
from loguru import logger

from .starlink_api import StarlinkAPI


class ConnectionType(Enum):
    """Types of satellite connections."""
    STARLINK = "starlink"
    IRIDIUM = "iridium"
    INMARSAT = "inmarsat"
    THURAYA = "thuraya"
    OTHER = "other"


class ConnectionStatus(Enum):
    """Connection status states."""
    CONNECTED = "connected"
    DEGRADED = "degraded"
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    FAILED = "failed"


class SatelliteConnection:
    """Represents a single satellite connection."""

    def __init__(
        self,
        name: str,
        connection_type: ConnectionType,
        priority: int = 0,
        api_client: Optional[Any] = None,
    ):
        """
        Initialize a satellite connection.

        Args:
            name: Connection name
            connection_type: Type of satellite connection
            priority: Priority level (higher = more preferred)
            api_client: API client for this connection (e.g., StarlinkAPI)
        """
        self.name = name
        self.connection_type = connection_type
        self.priority = priority
        self.api_client = api_client
        self.status = ConnectionStatus.DISCONNECTED
        self.metrics = {}
        self.last_check = None
        self.failure_count = 0
        self.last_failure = None

    def get_metrics(self) -> Dict[str, Any]:
        """Get current connection metrics."""
        if self.connection_type == ConnectionType.STARLINK and self.api_client:
            try:
                status = self.api_client.get_status()
                self.metrics = {
                    "latency_ms": status.get("ping_latency_ms", 0),
                    "downlink_mbps": status.get("downlink_throughput_bps", 0) / 1_000_000,
                    "uplink_mbps": status.get("uplink_throughput_bps", 0) / 1_000_000,
                    "snr": status.get("snr", 0),
                    "obstructed": status.get("obstructed", False),
                    "state": status.get("state", "UNKNOWN"),
                }
                self.last_check = time.time()
                
                # Update status based on metrics
                if self.metrics["state"] == "CONNECTED":
                    if self.metrics["obstructed"] or self.metrics["latency_ms"] > 100:
                        self.status = ConnectionStatus.DEGRADED
                    else:
                        self.status = ConnectionStatus.CONNECTED
                        self.failure_count = 0
                else:
                    self.status = ConnectionStatus.CONNECTING
                
                return self.metrics
                
            except Exception as e:
                logger.error(f"Error getting metrics for {self.name}: {e}")
                self.failure_count += 1
                self.last_failure = time.time()
                self.status = ConnectionStatus.FAILED
                return {}
        else:
            # Simulated metrics for other connection types
            return self._get_simulated_metrics()

    def _get_simulated_metrics(self) -> Dict[str, Any]:
        """Generate simulated metrics for non-Starlink connections."""
        base_latency = {
            ConnectionType.IRIDIUM: 1500,
            ConnectionType.INMARSAT: 800,
            ConnectionType.THURAYA: 600,
            ConnectionType.OTHER: 500,
        }
        
        latency = base_latency.get(self.connection_type, 500) + random.randint(-100, 100)
        
        return {
            "latency_ms": latency,
            "downlink_mbps": random.uniform(0.5, 5.0),
            "uplink_mbps": random.uniform(0.3, 2.0),
            "snr": random.uniform(5.0, 12.0),
            "obstructed": False,
            "state": "CONNECTED",
        }

    def test_connection(self) -> bool:
        """Test if connection is working."""
        metrics = self.get_metrics()
        return bool(metrics and metrics.get("state") in ["CONNECTED", "DEGRADED"])


class SatelliteConnectionManager:
    """Manages multiple satellite connections with automatic failover."""

    def __init__(self):
        """Initialize the connection manager."""
        self.connections: List[SatelliteConnection] = []
        self.active_connection: Optional[SatelliteConnection] = None
        self.failover_threshold = 3  # Number of failures before failover
        self.check_interval = 30  # Seconds between health checks
        self.last_health_check = None

    def add_connection(
        self,
        name: str,
        connection_type: ConnectionType,
        priority: int = 0,
        **kwargs
    ) -> SatelliteConnection:
        """
        Add a satellite connection.

        Args:
            name: Connection name
            connection_type: Type of satellite connection
            priority: Priority level (higher = more preferred)
            **kwargs: Additional arguments (e.g., target for Starlink)

        Returns:
            Created SatelliteConnection object
        """
        api_client = None
        
        if connection_type == ConnectionType.STARLINK:
            api_client = StarlinkAPI(
                target=kwargs.get("target"),
                simulation_mode=kwargs.get("simulation_mode", False)
            )
        
        connection = SatelliteConnection(name, connection_type, priority, api_client)
        self.connections.append(connection)
        
        # Sort by priority (highest first)
        self.connections.sort(key=lambda c: c.priority, reverse=True)
        
        logger.info(f"Added connection: {name} ({connection_type.value}) with priority {priority}")
        return connection

    def get_active_connection(self) -> Optional[SatelliteConnection]:
        """Get the currently active connection."""
        return self.active_connection

    def select_best_connection(self) -> Optional[SatelliteConnection]:
        """
        Select the best available connection based on priority and health.

        Returns:
            Best available connection or None
        """
        if not self.connections:
            logger.warning("No connections available")
            return None

        # Test connections in priority order
        for connection in self.connections:
            if connection.test_connection():
                logger.info(f"Selected connection: {connection.name}")
                return connection

        logger.error("No working connections found")
        return None

    def connect(self) -> bool:
        """
        Establish connection using the best available satellite.

        Returns:
            True if connection established successfully
        """
        connection = self.select_best_connection()
        
        if connection:
            self.active_connection = connection
            logger.info(f"Connected via {connection.name}")
            return True
        
        logger.error("Failed to establish any connection")
        return False

    def perform_health_check(self) -> Dict[str, Any]:
        """
        Check health of all connections.

        Returns:
            Dictionary with health status of all connections
        """
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "active_connection": self.active_connection.name if self.active_connection else None,
            "connections": [],
        }

        for connection in self.connections:
            metrics = connection.get_metrics()
            health_status["connections"].append({
                "name": connection.name,
                "type": connection.connection_type.value,
                "status": connection.status.value,
                "priority": connection.priority,
                "metrics": metrics,
                "failure_count": connection.failure_count,
            })

        self.last_health_check = time.time()
        return health_status

    def check_and_failover(self) -> bool:
        """
        Check active connection and failover if necessary.

        Returns:
            True if failover occurred
        """
        if not self.active_connection:
            return self.connect()

        # Check if current connection is still healthy
        if self.active_connection.failure_count >= self.failover_threshold:
            logger.warning(
                f"Connection {self.active_connection.name} has failed {self.active_connection.failure_count} times. "
                "Attempting failover..."
            )
            
            # Try to find a better connection
            new_connection = self.select_best_connection()
            
            if new_connection and new_connection != self.active_connection:
                old_name = self.active_connection.name
                self.active_connection = new_connection
                logger.info(f"Failed over from {old_name} to {new_connection.name}")
                return True

        return False

    def get_connection_stats(self) -> Dict[str, Any]:
        """
        Get statistics for all connections.

        Returns:
            Dictionary with connection statistics
        """
        stats = {
            "total_connections": len(self.connections),
            "active_connection": self.active_connection.name if self.active_connection else None,
            "connections": {},
        }

        for connection in self.connections:
            stats["connections"][connection.name] = {
                "type": connection.connection_type.value,
                "status": connection.status.value,
                "priority": connection.priority,
                "failure_count": connection.failure_count,
                "last_check": connection.last_check,
                "metrics": connection.metrics,
            }

        return stats

    def auto_recover(self, connection_name: Optional[str] = None) -> bool:
        """
        Attempt to recover a failed connection.

        Args:
            connection_name: Name of connection to recover (or active if None)

        Returns:
            True if recovery was successful
        """
        target_connection = None
        
        if connection_name:
            target_connection = next(
                (c for c in self.connections if c.name == connection_name),
                None
            )
        else:
            target_connection = self.active_connection

        if not target_connection:
            logger.error("No connection to recover")
            return False

        logger.info(f"Attempting to recover connection: {target_connection.name}")

        # If it's a Starlink connection, try reboot
        if target_connection.connection_type == ConnectionType.STARLINK and target_connection.api_client:
            try:
                logger.info("Attempting Starlink dish reboot...")
                if target_connection.api_client.reboot():
                    time.sleep(60)  # Wait for reboot
                    target_connection.failure_count = 0
                    return target_connection.test_connection()
            except Exception as e:
                logger.error(f"Failed to reboot: {e}")

        # Reset failure count and try again
        target_connection.failure_count = 0
        return target_connection.test_connection()

    def close_all(self):
        """Close all connections."""
        for connection in self.connections:
            if connection.api_client and hasattr(connection.api_client, 'close'):
                connection.api_client.close()
        
        self.connections.clear()
        self.active_connection = None
        logger.info("Closed all connections")
