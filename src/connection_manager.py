"""
Updated connection manager with Starlink integration
"""
import time
import threading
import logging
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
        """Convert StarlinkMetrics to ConnectionMetrics"""
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
            import json
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
        
        logger.info(f"Found {len(connections)} available connections")
        return connections
    
    def _check_satellite_visibility(self, satellite_id: str) -> bool:
        """
        Check if satellite is visible (simulated)
        """
        import random
        return random.random() > 0.3
    
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
                self.active_connection = connection_id
                self.connections[connection_id] = ConnectionStatus.CONNECTED
                self.metrics[connection_id] = metrics
                
                logger.info(f"Successfully connected to {connection_id}")
                
                # Start monitoring if not already
                if not self.monitoring:
                    self.start_monitoring()
                
                return True
            else:
                logger.warning(f"Connection {connection_id} does not meet requirements")
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
        import random
        import time
        
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
        self.monitoring = True
        
        def monitor():
            while self.monitoring and self.active_connection:
                try:
                    metrics = self._measure_connection_quality(self.active_connection)
                    self.metrics[self.active_connection] = metrics
                    
                    # Check if connection is degrading
                    if not self._validate_connection(metrics):
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
                        best_score = score
                        best_connection = conn_id
                        
                except Exception as e:
                    logger.error(f"Failed to evaluate {conn_id}: {e}")
        
        if best_connection:
            logger.info(f"Switching to {best_connection} (score: {best_score:.2f})")
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
    
    def _calculate_current_score(self) -> float:
        """Calculate score for current connection"""
        if self.active_connection and self.active_connection in self.metrics:
            return self._calculate_connection_score(self.metrics[self.active_connection])
        return 0
    
    def reboot_active_connection(self) -> bool:
        """Reboot the active connection (useful for Starlink)"""
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
                time.sleep(300)  # Wait 5 minutes
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
