"""
Satellite Connection Manager Module
Manages connections to satellite networks including Starlink
"""

import time
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
            except ImportError as e:
                print(f"Warning: Could not import StarlinkMonitor: {e}")
                self.starlink_monitor = None
        else:
            self.starlink_monitor = None
    
    def scan_available_connections(self) -> List[str]:
        """
        Scan for available satellite connections
        
        Returns:
            List of available connection names
        """
        self.available_connections = []
        
        if self.enable_starlink and self.starlink_monitor and self.starlink_monitor.initialized:
            self.available_connections.append("starlink_satellite")
        
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
            return False
        
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
                return True
        
        return False
    
    def disconnect(self):
        """Disconnect from current connection"""
        self.active_connection = None
        self.connection_metrics = None
    
    def get_connection_report(self) -> Dict:
        """
        Get report on current connection
        
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
