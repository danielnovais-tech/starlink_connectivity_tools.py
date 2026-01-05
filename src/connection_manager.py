"""
Satellite Connection Manager Module
Manages connections to satellite networks including Starlink
"""

import time
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ConnectionMetrics:
    """Metrics for a connection"""
    bandwidth_down: float
    bandwidth_up: float
    latency: float
    signal_strength: float
    packet_loss: float


class SatelliteConnectionManager:
    """Manage satellite network connections"""
    
    def __init__(self, enable_starlink: bool = True, starlink_host: str = "192.168.100.1"):
        """
        Initialize connection manager
        
        Args:
            enable_starlink: Whether to enable Starlink connectivity
            starlink_host: Starlink router IP address
        """
        self.logger = logging.getLogger(__name__)
        self.enable_starlink = enable_starlink
        self.starlink_host = starlink_host
        self.active_connection: Optional[str] = None
        self.available_connections: List[str] = []
        self.crisis_mode = False
        self.connection_metrics: Optional[ConnectionMetrics] = None
        
        # Import and initialize Starlink monitor if enabled
        if enable_starlink:
            try:
                from src.starlink_monitor import StarlinkMonitor
                self.starlink_monitor = StarlinkMonitor(host=starlink_host)
                self.logger.info("Starlink monitor initialized for connection manager")
            except ImportError as e:
                self.logger.error(f"Could not import StarlinkMonitor: {e}. Starlink functionality will be disabled.")
                self.starlink_monitor = None
        else:
            self.starlink_monitor = None
Updated connection manager with Starlink integration
"""
import time
import threading
import logging
import json
import random
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Union
from enum import Enum

# Import Starlink monitor if available
try:
    from .starlink_monitor import StarlinkMonitor, StarlinkMetrics
    STARLINK_AVAILABLE = True
except ImportError:
    STARLINK_AVAILABLE = False
    logging.warning("Starlink monitor not available")
Connection Manager - Updated with Starlink integration

Manages network connections with specific support for Starlink satellite internet.
Handles connection establishment, monitoring, and recovery.
"""

import logging
import time
from typing import Optional, Dict, Any
import requests
Connection Manager Module

Manages Starlink satellite connections, including establishing, 
monitoring, and maintaining stable connections.
"""


class ConnectionManager:
    """Manages Starlink satellite connections."""
    
    def __init__(self):
        """Initialize the connection manager."""
        self.connected = False
        self.connection_quality = 0
    
    def connect(self):
        """Establish a connection to the Starlink satellite."""
        # TODO: Implement connection logic
        pass
    
    def disconnect(self):
        """Disconnect from the Starlink satellite."""
        # TODO: Implement disconnection logic
        pass
    
    def check_status(self):
        """Check the current connection status."""
        # TODO: Implement status check logic
        return self.connected
    
    def get_connection_quality(self):
        """Get the current connection quality metric."""
        # TODO: Implement connection quality measurement
        return self.connection_quality
Satellite Connection Manager for Starlink connectivity tools.
"""
import json
from typing import Dict, List, Optional, Any
Satellite Connection Manager
Handles satellite connectivity, scanning, and connection management
"""

import logging
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages network connections with Starlink integration."""
    
    def __init__(self, starlink_endpoint: str = "192.168.100.1"):
        """
        Initialize the ConnectionManager.
        
        Args:
            starlink_endpoint: IP address or hostname of the Starlink router
        """
        self.starlink_endpoint = starlink_endpoint
        self.is_connected = False
        self.connection_type = None
        self.retry_count = 0
        self.max_retries = 3
        
    def connect(self) -> bool:
        """
        Establish a connection to the Starlink network.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        logger.info("Attempting to connect to Starlink network...")
        
        try:
            # Try to connect to Starlink router
            response = self._check_starlink_status()
            
            if response and response.get("connected", False):
                self.is_connected = True
                self.connection_type = "starlink"
                self.retry_count = 0
                logger.info("Successfully connected to Starlink network")
                return True
            else:
                logger.warning("Starlink not available, attempting fallback...")
                return self._fallback_connection()
                
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.retry_count += 1
            
            if self.retry_count < self.max_retries:
                logger.info(f"Retrying connection ({self.retry_count}/{self.max_retries})...")
                time.sleep(2)
                return self.connect()
            
            return False
    
    def disconnect(self) -> None:
        """Disconnect from the network."""
        logger.info("Disconnecting from network...")
        self.is_connected = False
        self.connection_type = None
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get current connection status.
        
        Returns:
            dict: Connection status information
        """
        return {
            "connected": self.is_connected,
            "connection_type": self.connection_type,
            "retry_count": self.retry_count,
            "starlink_endpoint": self.starlink_endpoint
        }
    
    def _check_starlink_status(self) -> Optional[Dict[str, Any]]:
        """
        Check Starlink router status.
        
        Returns:
            Optional[dict]: Status information from Starlink router, or None if unavailable
        """
        try:
            # Simulate Starlink status check
            # In a real implementation, this would query the Starlink gRPC API
            return {
                "connected": True,
                "uptime": 3600,
                "obstructed": False,
                "signal_quality": 95
            }
        except Exception as e:
            logger.error(f"Failed to check Starlink status: {e}")
            return None
    
    def _fallback_connection(self) -> bool:
        """
        Attempt to connect using fallback method.
        
        Returns:
            bool: True if fallback connection is successful
        """
        logger.info("Attempting fallback connection...")
        # Implement fallback logic here (e.g., cellular, other ISP)
        self.is_connected = False
        self.connection_type = "fallback"
        return False
    
    def check_starlink_health(self) -> Dict[str, Any]:
        """
        Perform comprehensive Starlink health check.
        
        Returns:
            dict: Health check results
        """
        status = self._check_starlink_status()
        
        if not status:
            return {
                "healthy": False,
                "error": "Unable to reach Starlink router"
            }
        
        return {
            "healthy": status.get("connected", False),
            "signal_quality": status.get("signal_quality", 0),
            "obstructed": status.get("obstructed", True),
            "uptime": status.get("uptime", 0)
        }
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
    Manages satellite connections with support for crisis mode and connection optimization.
    """
    
    def __init__(self):
        """Initialize the connection manager."""
        self.crisis_mode_enabled = False
        self.crisis_config = {}
        self.current_connection = None
        self.available_connections = []
    
    def enable_crisis_mode(self, config: Dict[str, Any]) -> None:
        """
        Enable crisis mode for emergency scenarios.
        
        Args:
            config: Configuration dictionary containing:
                - crisis_min_bandwidth: Minimum bandwidth in Mbps
                - crisis_max_latency: Maximum latency in ms
        """
        self.crisis_mode_enabled = True
        self.crisis_config = config
    
    def scan_available_connections(self) -> List[Dict[str, Any]]:
        """
        Scan for available satellite connections.
        
        Returns:
            List of available connections with their properties
        """
        # Simulate scanning for available connections
        self.available_connections = [
            {
                'id': 'sat-001',
                'name': 'Starlink Satellite 001',
                'bandwidth': 150.0,  # Mbps
                'latency': 20,  # ms
                'signal_strength': 95,  # percentage
                'available': True
            },
            {
                'id': 'sat-002',
                'name': 'Starlink Satellite 002',
                'bandwidth': 120.0,  # Mbps
                'latency': 25,  # ms
                'signal_strength': 88,  # percentage
                'available': True
            }
        ]
        
        # Filter connections based on crisis mode requirements
        if self.crisis_mode_enabled:
            filtered_connections = []
            min_bandwidth = self.crisis_config.get('crisis_min_bandwidth', 0)
            max_latency = self.crisis_config.get('crisis_max_latency', float('inf'))
            
            for conn in self.available_connections:
                if (conn['bandwidth'] >= min_bandwidth and 
                    conn['latency'] <= max_latency):
                    filtered_connections.append(conn)
            
            return filtered_connections
        
        return self.available_connections
    
    def connect(self, connection: Dict[str, Any]) -> bool:
        """
        Connect to a specific satellite connection.
        
        Args:
            connection: Connection dictionary from scan_available_connections()
            
        Returns:
            True if connection was successful, False otherwise
        """
        if connection.get('available', False):
            self.current_connection = connection
            return True
        return False
    
    def get_connection_report(self) -> Dict[str, Any]:
        """
        Get a detailed status report of the current connection.
        
        Returns:
            Dictionary containing connection status and metrics
        """
        if not self.current_connection:
            return {
                'status': 'disconnected',
                'message': 'No active connection',
                'crisis_mode': self.crisis_mode_enabled,
                'crisis_config': self.crisis_config if self.crisis_mode_enabled else None
            }
        
        return {
            'status': 'connected',
            'connection': {
                'id': self.current_connection['id'],
                'name': self.current_connection['name'],
                'bandwidth_mbps': self.current_connection['bandwidth'],
                'latency_ms': self.current_connection['latency'],
                'signal_strength': self.current_connection['signal_strength']
            },
            'crisis_mode': self.crisis_mode_enabled,
            'crisis_config': self.crisis_config if self.crisis_mode_enabled else None,
            'performance_metrics': {
                'bandwidth_utilization': '75%',
                'packet_loss': '0.1%',
                'uptime': '99.9%'
            }
        }
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
Main connection manager for satellite connectivity optimization
"""
import time
import threading
import logging
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from enum import Enum
import json
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectionStatus(Enum):
    """Connection status enumeration"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    DEGRADED = "degraded"
    SCANNING = "scanning"
    FAILED = "failed"
    OFFLINE = "offline"  # Starlink-specific


@dataclass
class ConnectionMetrics:
    """Unified metrics for connection quality"""
    """Metrics for connection quality"""
    latency: float  # in ms
    jitter: float  # in ms
    packet_loss: float  # percentage
    bandwidth_down: float  # Mbps
    bandwidth_up: float  # Mbps
    signal_strength: float  # dBm
    timestamp: float
    
    # Additional Starlink-specific fields (optional)
    obstruction_percent: Optional[float] = None
    satellites_connected: Optional[int] = None
    snr: Optional[float] = None
    status: Optional[str] = None
    
    @classmethod
    def from_starlink_metrics(cls, starlink_metrics: 'StarlinkMetrics') -> 'ConnectionMetrics':
        """Convert StarlinkMetrics to ConnectionMetrics."""
        return cls(
            latency=starlink_metrics.latency,
            jitter=starlink_metrics.jitter,
            packet_loss=starlink_metrics.packet_loss,
            bandwidth_down=starlink_metrics.download_speed,
            bandwidth_up=starlink_metrics.upload_speed,
            signal_strength=starlink_metrics.signal_strength,
            timestamp=starlink_metrics.timestamp,
            obstruction_percent=starlink_metrics.obstruction_percent,
            satellites_connected=starlink_metrics.satellites_connected,
            snr=starlink_metrics.snr,
            status=starlink_metrics.status
        )


class SatelliteConnectionManager:
    """Main connection manager with Starlink support"""
    
    def __init__(self, 
                 config_path: str = None,
                 enable_starlink: bool = True,
                 starlink_host: str = "192.168.100.1"):


class SatelliteConnectionManager:
    """Manages satellite connections with optimization for crisis scenarios"""
    
    # Constants for connection quality scoring
    MAX_LATENCY_FOR_SCORING = 1000  # ms
    MAX_BANDWIDTH_FOR_SCORING = 200  # Mbps
    MAX_PACKET_LOSS_FOR_SCORING = 100  # percentage
    MIN_SIGNAL_STRENGTH = -100  # dBm
    SIGNAL_RANGE = 60  # dBm
    
    # Connection parameters
    SATELLITE_VISIBILITY_THRESHOLD = 0.3  # Probability threshold for visibility
    CONNECTION_TIMEOUT = 2  # seconds
    
    def __init__(self, config_path: str = None):
        self.connections: Dict[str, ConnectionStatus] = {}
        self.metrics: Dict[str, ConnectionMetrics] = {}
        self.active_connection: Optional[str] = None
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Crisis mode parameters
        self.crisis_mode = False
        self.minimum_viable_bandwidth = 2.0  # Mbps
        self.max_acceptable_latency = 500  # ms
        
        # Starlink integration
        self.starlink_enabled = enable_starlink and STARLINK_AVAILABLE
        self.starlink_monitor = None
        self.starlink_connection_id = "starlink_satellite"
        
        if self.starlink_enabled:
            try:
                self.starlink_monitor = StarlinkMonitor(host=starlink_host)
                self.connections[self.starlink_connection_id] = ConnectionStatus.SCANNING
                logger.info(f"Starlink integration enabled for {starlink_host}")
            except Exception as e:
                logger.error(f"Failed to initialize Starlink: {e}")
                self.starlink_enabled = False
        
        # Load configuration if provided
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path: str):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.minimum_viable_bandwidth = config.get(
                    'minimum_viable_bandwidth', 
                    self.minimum_viable_bandwidth
                )
                self.max_acceptable_latency = config.get(
                    'max_acceptable_latency',
                    self.max_acceptable_latency
                )
                
                # Load Starlink-specific config
                starlink_config = config.get('starlink', {})
                if starlink_config and self.starlink_monitor:
                    thresholds = starlink_config.get('thresholds', {})
                    self.starlink_monitor.set_thresholds(**thresholds)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
    
    def scan_available_connections(self) -> List[str]:
        """
        Scan for available satellite connections
        
        Returns:
            List of available connection names
        """
        self.logger.debug("Scanning for available connections")
        self.available_connections = []
        
        if self.enable_starlink and self.starlink_monitor and self.starlink_monitor.initialized:
            self.available_connections.append("starlink_satellite")
            self.logger.info("Found Starlink satellite connection")
        
        return self.available_connections
    
    def connect(self, connection_name: str) -> bool:
        """
        Connect to specified satellite network
        
        Args:
            connection_name: Name of connection to use
            
        Returns:
            True if connected successfully
        """
        if connection_name not in self.available_connections:
            self.logger.warning(f"Connection '{connection_name}' not available")
            return False
        
        self.logger.info(f"Connecting to {connection_name}")
        
        if connection_name == "starlink_satellite" and self.starlink_monitor:
            # Get current metrics from Starlink
            metrics = self.starlink_monitor.get_metrics()
            
            if metrics:
                self.active_connection = connection_name
                self.connection_metrics = ConnectionMetrics(
                    bandwidth_down=metrics.download_speed,
                    bandwidth_up=metrics.upload_speed,
                    latency=metrics.latency,
                    signal_strength=metrics.signal_strength,
                    packet_loss=metrics.packet_loss
                )
                self.logger.info(f"Connected to {connection_name} successfully")
                return True
            else:
                self.logger.error(f"Failed to get metrics for {connection_name}")
        
        return False
    
    def disconnect(self):
        """Disconnect from current connection"""
        if self.active_connection:
            self.logger.info(f"Disconnecting from {self.active_connection}")
        self.active_connection = None
        self.connection_metrics = None
    
    def get_connection_report(self) -> Dict:
        """
        Get report on current connection
        Includes Starlink if enabled
        """
        connections = []
        
        # Check Starlink first if enabled
        if self.starlink_enabled and self.starlink_monitor:
            try:
                # Get current status
                metrics = self.starlink_monitor.get_metrics()
                if metrics and metrics.status == "online":
                    connections.append(self.starlink_connection_id)
                    self.connections[self.starlink_connection_id] = ConnectionStatus.SCANNING
                    logger.info("Starlink satellite available")
            except Exception as e:
                logger.warning(f"Failed to check Starlink: {e}")
        
        # Simulate other satellite connections
        # In real implementation, this would scan for other services
        if not self.crisis_mode:
            satellite_ids = [
                "other_sat_001",
                "other_sat_002"
            ]
            
            for sat_id in satellite_ids:
                if self._check_satellite_visibility(sat_id):
                    connections.append(sat_id)
                    self.connections[sat_id] = ConnectionStatus.SCANNING
        
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
            'active_connection': self.active_connection or 'none',
            'crisis_mode': self.crisis_mode,
            'available_connections': self.available_connections
        }
        
        if self.active_connection and self.connection_metrics:
            # Calculate connection score (0-1 scale)
            score = self._calculate_connection_score()
            report['connection_score'] = score
            
            report['current_metrics'] = {
                'bandwidth_down': self.connection_metrics.bandwidth_down,
                'bandwidth_up': self.connection_metrics.bandwidth_up,
                'latency': self.connection_metrics.latency,
                'signal_strength': self.connection_metrics.signal_strength,
                'packet_loss': self.connection_metrics.packet_loss
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
    
    def _calculate_connection_score(self) -> float:
        """
        Calculate connection quality score
        
        Returns:
            Score from 0.0 to 1.0
        """
        if not self.connection_metrics:
            return 0.0
        
        # Simple scoring based on metrics
        score = 1.0
        
        # Penalize based on latency (target < 50ms)
        if self.connection_metrics.latency > 50:
            score -= min(0.3, (self.connection_metrics.latency - 50) / 200)
        
        # Penalize based on packet loss
        score -= min(0.3, self.connection_metrics.packet_loss / 10)
        
        # Penalize based on low bandwidth
        if self.connection_metrics.bandwidth_down < 25:
            score -= min(0.4, (25 - self.connection_metrics.bandwidth_down) / 50)
        
        return max(0.0, score)
    def shutdown(self):
        """Gracefully shutdown the connection manager"""
        logger.info("Shutting down connection manager...")
        
        if self.active_connection:
            self.disconnect()
        
        self.available_connections.clear()
        logger.info("Connection manager shutdown complete")
        Returns list of connection IDs
        """
        connections = []
        
        # Simulate scanning for connections
        # In real implementation, this would interface with Starlink API
        satellite_ids = [
            "starlink_sat_001",
            "starlink_sat_002", 
            "starlink_sat_003"
        ]
        
        for sat_id in satellite_ids:
            if self._check_satellite_visibility(sat_id):
                connections.append(sat_id)
                self.connections[sat_id] = ConnectionStatus.SCANNING
        
        logger.info(f"Found {len(connections)} available connections")
        return connections
    
    def _check_satellite_visibility(self, satellite_id: str) -> bool:
        """
        Check if satellite is visible (simulated)
        """
        return random.random() > 0.3
        In real implementation, would use GPS and satellite ephemeris data
        """
        # Simulate satellite visibility check
        return random.random() > self.SATELLITE_VISIBILITY_THRESHOLD  # 70% chance of visibility
    
    def connect(self, connection_id: str) -> bool:
        """Establish connection to a specific satellite"""
        try:
            logger.info(f"Attempting to connect to {connection_id}")
            
            # Handle Starlink connection
            if connection_id == self.starlink_connection_id and self.starlink_monitor:
                return self._connect_starlink()
            
            # Handle other satellite connections (simulated)
            time.sleep(2)
            metrics = self._measure_connection_quality(connection_id)
            
            if self._validate_connection(metrics):
            # Simulate connection process
            time.sleep(self.CONNECTION_TIMEOUT)
            
            # Check connection quality
            metrics = self._measure_connection_quality(connection_id)
            
            if (metrics.bandwidth_down >= self.minimum_viable_bandwidth and 
                metrics.latency <= self.max_acceptable_latency):
                
                self.active_connection = connection_id
                self.connections[connection_id] = ConnectionStatus.CONNECTED
                self.metrics[connection_id] = metrics
                
                logger.info(f"Successfully connected to {connection_id}")
                logger.info(f"Metrics: {metrics}")
                
                # Start monitoring if not already
                if not self.monitoring:
                    self.start_monitoring()
                
                return True
            else:
                logger.warning(f"Connection {connection_id} does not meet requirements")
                logger.warning(f"Connection {connection_id} does not meet minimum requirements")
                self.connections[connection_id] = ConnectionStatus.DEGRADED
                return False
                
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.connections[connection_id] = ConnectionStatus.FAILED
            return False
    
    def _connect_starlink(self) -> bool:
        """Establish Starlink connection"""
        try:
            # Check if Starlink is already online
            metrics = self.starlink_monitor.get_metrics()
            
            if not metrics:
                logger.error("Failed to get Starlink metrics")
                return False
            
            # Convert Starlink metrics to our format
            connection_metrics = ConnectionMetrics.from_starlink_metrics(metrics)
            
            # Check if we should attempt recovery
            if metrics.status != "online":
                logger.warning(f"Starlink status is {metrics.status}, attempting recovery...")
                
                if self.crisis_mode:
                    # In crisis mode, we're more aggressive with recovery
                    if metrics.status == "offline":
                        logger.info("Attempting to unstow dish...")
                        self.starlink_monitor.unstow_dish()
                        time.sleep(60)  # Wait 1 minute
                        metrics = self.starlink_monitor.get_metrics()
            
            # Validate connection
            if self._validate_connection(connection_metrics) and metrics.status == "online":
                self.active_connection = self.starlink_connection_id
                self.connections[self.starlink_connection_id] = ConnectionStatus.CONNECTED
                self.metrics[self.starlink_connection_id] = connection_metrics
                
                logger.info(f"Starlink connected: {metrics.download_speed:.1f} Mbps, "
                           f"{metrics.latency:.1f} ms latency")
                
                # Start Starlink monitoring
                self.starlink_monitor.start_monitoring(interval=60)
                
                # Start our monitoring
                if not self.monitoring:
                    self.start_monitoring()
                
                return True
            else:
                logger.warning(f"Starlink connection not viable: status={metrics.status}")
                self.connections[self.starlink_connection_id] = ConnectionStatus.DEGRADED
                return False
                
        except Exception as e:
            logger.error(f"Starlink connection failed: {e}")
            self.connections[self.starlink_connection_id] = ConnectionStatus.FAILED
            return False
    
    def _validate_connection(self, metrics: ConnectionMetrics) -> bool:
        """Validate if connection meets minimum requirements"""
        if self.crisis_mode:
            # Relaxed requirements in crisis mode
            min_bandwidth = max(0.5, self.minimum_viable_bandwidth * 0.5)
            max_latency = min(2000, self.max_acceptable_latency * 2)
        else:
            min_bandwidth = self.minimum_viable_bandwidth
            max_latency = self.max_acceptable_latency
        
        return (metrics.bandwidth_down >= min_bandwidth and 
                metrics.latency <= max_latency)
    
    def _measure_connection_quality(self, connection_id: str) -> ConnectionMetrics:
        """
        Measure connection quality metrics
        For Starlink, uses real metrics; for others, simulated
        """
        if connection_id == self.starlink_connection_id and self.starlink_monitor:
            # Get real Starlink metrics
            starlink_metrics = self.starlink_monitor.get_metrics()
            if starlink_metrics:
                return ConnectionMetrics.from_starlink_metrics(starlink_metrics)
        
        # Simulated metrics for other connections
    def _measure_connection_quality(self, connection_id: str) -> ConnectionMetrics:
        """
        Measure connection quality metrics
        In real implementation, would perform actual network tests
        """
        # Simulated metrics
        return ConnectionMetrics(
            latency=random.uniform(20, 100),
            jitter=random.uniform(1, 10),
            packet_loss=random.uniform(0, 5),
            bandwidth_down=random.uniform(50, 200),
            bandwidth_up=random.uniform(10, 40),
            signal_strength=random.uniform(-60, -40),
            timestamp=time.time()
        )
    
    def enable_crisis_mode(self, settings: Dict = None):
        """Enable crisis mode with optimized settings"""
        """Enable crisis mode with optimized settings for emergencies"""
        self.crisis_mode = True
        
        # Adjust parameters for crisis mode
        if settings:
            self.minimum_viable_bandwidth = settings.get(
                'crisis_min_bandwidth', 
                1.0  # Lower threshold in crisis
            )
            self.max_acceptable_latency = settings.get(
                'crisis_max_latency',
                1000  # Higher tolerance in crisis
            )
        
        # Adjust Starlink thresholds if available
        if self.starlink_monitor:
            crisis_thresholds = {
                'min_download_speed': max(1.0, settings.get('crisis_min_bandwidth', 1.0)),
                'max_latency': min(1000, settings.get('crisis_max_latency', 1000)),
                'max_packet_loss': 20,  # Higher tolerance
                'max_obstruction': 10,  # Higher tolerance
            }
            self.starlink_monitor.set_thresholds(**crisis_thresholds)
        
        logger.info("Crisis mode enabled")
    
    def start_monitoring(self, interval: int = 30):
        """Start continuous monitoring of connection quality"""
        logger.info("Crisis mode enabled")
        logger.info(f"Min bandwidth: {self.minimum_viable_bandwidth} Mbps")
        logger.info(f"Max latency: {self.max_acceptable_latency} ms")
    
    def start_monitoring(self, interval: int = 30):
        """Start continuous monitoring of connection quality"""
        if self.monitoring:
            logger.warning("Monitoring is already active")
            return
            
        self.monitoring = True
        
        def monitor():
            while self.monitoring and self.active_connection:
                try:
                    metrics = self._measure_connection_quality(self.active_connection)
                    self.metrics[self.active_connection] = metrics
                    
                    # Check if connection is degrading
                    if not self._validate_connection(metrics):
                    if (metrics.bandwidth_down < self.minimum_viable_bandwidth or 
                        metrics.latency > self.max_acceptable_latency):
                        
                        logger.warning(f"Connection {self.active_connection} is degrading")
                        self.connections[self.active_connection] = ConnectionStatus.DEGRADED
                        
                        if not self.crisis_mode:
                            # Try to find better connection
                            self._auto_switch_connection()
                    
                    time.sleep(interval)
                    
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                    time.sleep(interval)
        
        self.monitor_thread = threading.Thread(target=monitor, daemon=True)
        self.monitor_thread.start()
        logger.info(f"Started monitoring with {interval}s interval")
    
    def _auto_switch_connection(self):
        """Automatically switch to better connection if available"""
        logger.info("Attempting auto-switch to better connection")
        
        available = self.scan_available_connections()
        best_connection = None
        best_score = -1
        
        current_score = self._calculate_current_score()
        
        for conn_id in available:
            if conn_id != self.active_connection:
                try:
                    metrics = self._measure_connection_quality(conn_id)
                    score = self._calculate_connection_score(metrics)
                    
                    if score > best_score and score > current_score * 1.2:  # 20% better
                    if score > best_score:
                        best_score = score
                        best_connection = conn_id
                        
                except Exception as e:
                    logger.error(f"Failed to evaluate {conn_id}: {e}")
        
        if best_connection:
            logger.info(f"Switching to {best_connection} (score: {best_score:.2f})")
        if best_connection and best_score > self._calculate_current_score():
            logger.info(f"Switching to {best_connection} (score: {best_score})")
            self.disconnect()
            return self.connect(best_connection)
        
        return False
    
    def _calculate_connection_score(self, metrics: ConnectionMetrics) -> float:
        """Calculate a score for connection quality"""
        # Weighted scoring system
        weights = {
            'latency': 0.3,
            'bandwidth': 0.4,
            'packet_loss': 0.2,
            'signal': 0.1
        }
        
        # Normalize and weight each metric
        latency_score = max(0, 1 - (metrics.latency / 1000)) * weights['latency']
        bandwidth_score = min(1, metrics.bandwidth_down / 200) * weights['bandwidth']
        packet_loss_score = max(0, 1 - (metrics.packet_loss / 100)) * weights['packet_loss']
        
        # Signal strength: convert dBm (-100 to -40) to 0-1 scale
        signal_normalized = max(0, min(1, (metrics.signal_strength + 100) / 60))
        signal_score = signal_normalized * weights['signal']
        
        # Bonus for Starlink if it has good satellite count
        bonus = 0
        if metrics.satellites_connected and metrics.satellites_connected > 5:
            bonus = 0.1 * (min(metrics.satellites_connected, 10) / 10)
        
        return latency_score + bandwidth_score + packet_loss_score + signal_score + bonus
        latency_score = max(0, 1 - (metrics.latency / self.MAX_LATENCY_FOR_SCORING)) * weights['latency']
        bandwidth_score = min(1, metrics.bandwidth_down / self.MAX_BANDWIDTH_FOR_SCORING) * weights['bandwidth']
        packet_loss_score = max(0, 1 - (metrics.packet_loss / self.MAX_PACKET_LOSS_FOR_SCORING)) * weights['packet_loss']
        signal_score = max(0, min(1, (metrics.signal_strength - self.MIN_SIGNAL_STRENGTH) / self.SIGNAL_RANGE)) * weights['signal']
        
        return latency_score + bandwidth_score + packet_loss_score + signal_score
    
    def _calculate_current_score(self) -> float:
        """Calculate score for current connection"""
        if self.active_connection and self.active_connection in self.metrics:
            return self._calculate_connection_score(self.metrics[self.active_connection])
        return 0
    
    def reboot_active_connection(self) -> bool:
        """
        Reboot the active connection (useful for Starlink).
        
        Note: This method blocks for ~5 minutes during Starlink reboot.
        Consider calling in a separate thread for non-blocking operation.
        """
        if not self.active_connection:
            logger.warning("No active connection to reboot")
            return False
        
        if self.active_connection == self.starlink_connection_id and self.starlink_monitor:
            logger.info("Rebooting Starlink dish...")
            success = self.starlink_monitor.reboot_dish()
            if success:
                # Update status
                self.connections[self.starlink_connection_id] = ConnectionStatus.SCANNING
                logger.info("Starlink reboot initiated. Will reconnect in 5 minutes.")
                # NOTE: Blocking sleep - dish needs ~5 minutes to reboot
                # For non-blocking operation, call this method in a separate thread
                time.sleep(300)  # Wait 5 minutes for dish to reboot
                return self.connect(self.starlink_connection_id)
            return False
        
        logger.warning(f"Reboot not supported for {self.active_connection}")
        return False
    
    def get_connection_report(self) -> Dict:
        """Generate a comprehensive connection report"""
        report = {
            'active_connection': self.active_connection,
            'crisis_mode': self.crisis_mode,
            'starlink_enabled': self.starlink_enabled,
            'total_connections': len(self.connections),
            'connection_status': {k: v.value for k, v in self.connections.items()},
            'timestamp': time.time()
        }
        
        if self.active_connection and self.active_connection in self.metrics:
            report['current_metrics'] = asdict(self.metrics[self.active_connection])
            report['connection_score'] = self._calculate_current_score()
        
        # Add Starlink-specific info if available
        if self.starlink_monitor and self.starlink_enabled:
            starlink_status = self.starlink_monitor.get_status()
            report['starlink_status'] = starlink_status
        
        return report
    
    def disconnect(self):
        """Disconnect from current connection"""
        if self.active_connection:
            logger.info(f"Disconnecting from {self.active_connection}")
            self.connections[self.active_connection] = ConnectionStatus.DISCONNECTED
            
            # Stop Starlink monitoring if it's active
            if self.active_connection == self.starlink_connection_id and self.starlink_monitor:
                self.starlink_monitor.stop_monitoring()
            
            self.active_connection = None
    
    def shutdown(self):
        """Clean shutdown of connection manager"""
        self.monitoring = False
        self.disconnect()
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        if self.starlink_monitor:
            self.starlink_monitor.stop_monitoring()
        
        logger.info("Connection manager shutdown complete")
        logger.info("Connection manager shutdown complete")
Connection Manager Module

Handles Starlink connection establishment, monitoring, and management.
"""


class ConnectionManager:
    """Manages Starlink satellite connection."""

    def __init__(self, config=None):
        """
        Initialize the ConnectionManager.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.connected = False
        self.connection_status = "disconnected"

    def connect(self):
        """
        Establish connection to Starlink satellite.

        Returns:
            bool: True if connection successful, False otherwise
        """
        # Placeholder implementation
        self.connected = True
        self.connection_status = "connected"
        return True

    def disconnect(self):
        """
        Disconnect from Starlink satellite.

        Returns:
            bool: True if disconnection successful, False otherwise
        """
        # Placeholder implementation
        self.connected = False
        self.connection_status = "disconnected"
        return True

    def get_status(self):
        """
        Get current connection status.

        Returns:
            dict: Connection status information
        """
        return {
            "connected": self.connected,
            "status": self.connection_status,
        }

    def reconnect(self):
        """
        Reconnect to Starlink satellite.

        Returns:
            bool: True if reconnection successful, False otherwise
        """
        self.disconnect()
        return self.connect()
