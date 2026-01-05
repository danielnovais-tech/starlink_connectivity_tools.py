"""
Satellite Connection Manager
Handles satellite connectivity, scanning, and connection management
"""

import logging
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ConnectionMetrics:
    """Metrics for a satellite connection"""
    bandwidth_down: float = 0.0  # Mbps
    bandwidth_up: float = 0.0    # Mbps
    latency: float = 0.0          # ms
    packet_loss: float = 0.0      # percentage
    signal_strength: float = 0.0  # dBm
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


class SatelliteConnectionManager:
    """
    Manages satellite connections for Starlink
    """
    
    def __init__(self, config_file: str = None):
        """
        Initialize the connection manager
        
        Args:
            config_file: Optional path to configuration file
        """
        self.config_file = config_file
        self.active_connection: Optional[str] = None
        self.available_connections: List[str] = []
        self.metrics: Dict[str, ConnectionMetrics] = {}
        self.crisis_mode = False
        self.crisis_config = {}
        
        logger.info("SatelliteConnectionManager initialized")
        
        if config_file:
            self._load_config(config_file)
    
    def _load_config(self, config_file: str):
        """Load configuration from file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                # Process configuration
                logger.info(f"Configuration loaded from {config_file}")
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using defaults")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
    
    def enable_crisis_mode(self, crisis_config: dict):
        """
        Enable crisis mode with special configuration
        
        Args:
            crisis_config: Dictionary with crisis mode settings
        """
        self.crisis_mode = True
        self.crisis_config = crisis_config
        logger.warning(f"Crisis mode enabled: {crisis_config}")
    
    def scan_available_connections(self) -> List[str]:
        """
        Scan for available satellite connections
        
        Returns:
            List of available connection IDs
        """
        logger.info("Scanning for available satellite connections...")
        
        # Simulate scanning for connections
        # In real implementation, would interface with Starlink hardware
        self.available_connections = [
            "starlink-sat-001",
            "starlink-sat-002",
            "starlink-sat-003"
        ]
        
        # Initialize metrics for each connection
        for conn_id in self.available_connections:
            if conn_id not in self.metrics:
                self.metrics[conn_id] = ConnectionMetrics(
                    bandwidth_down=100.0,
                    bandwidth_up=20.0,
                    latency=40.0,
                    packet_loss=0.1,
                    signal_strength=-65.0
                )
        
        logger.info(f"Found {len(self.available_connections)} connections")
        return self.available_connections
    
    def connect(self, connection_id: str) -> bool:
        """
        Connect to a specific satellite
        
        Args:
            connection_id: ID of the connection to connect to
            
        Returns:
            True if connection successful, False otherwise
        """
        if connection_id not in self.available_connections:
            logger.error(f"Connection {connection_id} not available")
            return False
        
        try:
            # Simulate connection establishment
            logger.info(f"Connecting to {connection_id}...")
            
            self.active_connection = connection_id
            
            # Update metrics for active connection
            if connection_id in self.metrics:
                self.metrics[connection_id].last_updated = datetime.now()
            
            logger.info(f"Successfully connected to {connection_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to {connection_id}: {e}")
            return False
    
    def disconnect(self, connection_id: str = None):
        """
        Disconnect from satellite
        
        Args:
            connection_id: Optional specific connection to disconnect
        """
        if connection_id is None:
            connection_id = self.active_connection
        
        if connection_id:
            logger.info(f"Disconnecting from {connection_id}")
            if self.active_connection == connection_id:
                self.active_connection = None
    
    def get_connection_report(self) -> dict:
        """
        Get current connection status report
        
        Returns:
            Dictionary with connection information
        """
        report = {
            'active_connection': self.active_connection,
            'available_connections': len(self.available_connections),
            'crisis_mode': self.crisis_mode
        }
        
        if self.active_connection and self.active_connection in self.metrics:
            metrics = self.metrics[self.active_connection]
            report['current_metrics'] = {
                'bandwidth_down': metrics.bandwidth_down,
                'bandwidth_up': metrics.bandwidth_up,
                'latency': metrics.latency,
                'packet_loss': metrics.packet_loss,
                'signal_strength': metrics.signal_strength
            }
        
        return report
    
    def shutdown(self):
        """Gracefully shutdown the connection manager"""
        logger.info("Shutting down connection manager...")
        
        if self.active_connection:
            self.disconnect()
        
        self.available_connections.clear()
        logger.info("Connection manager shutdown complete")
