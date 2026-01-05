"""
Starlink Monitor Module
Provides monitoring capabilities for Starlink satellite connections
"""

import time
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from collections import deque


@dataclass
class StarlinkMetrics:
    """Data class for Starlink metrics"""
    timestamp: float
    status: str
    satellites_connected: int
    download_speed: float
    upload_speed: float
    latency: float
    packet_loss: float
    signal_strength: float
    snr: float
    azimuth: float
    elevation: float
    obstruction_percent: float
    dish_power_usage: float
    dish_temp: float
    router_temp: float
    boot_count: int


class StarlinkMonitor:
    """Monitor Starlink satellite connection metrics"""
    
    def __init__(self, host: str = "192.168.100.1", history_size: int = 1000):
        """
        Initialize Starlink monitor
        
        Args:
            host: Starlink router IP address
            history_size: Number of historical metrics to retain
        """
        self.host = host
        self.history_size = history_size
        self.metrics_history: deque = deque(maxlen=history_size)
        self.initialized = False
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Default thresholds for alerts
        self.thresholds = {
            'min_download_speed': 25.0,  # Mbps
            'max_latency': 100.0,  # ms
            'max_packet_loss': 5.0,  # %
            'max_obstruction': 10.0,  # %
        }
        
        # Try to initialize connection
        self._initialize()
    
    def _initialize(self):
        """Initialize connection to Starlink router"""
        try:
            # Simulate initialization - in real implementation, this would connect to the router
            # For now, we'll mark as initialized to allow the CLI to work
            self.initialized = True
            return True
        except Exception as e:
            print(f"Failed to initialize Starlink connection: {e}")
            self.initialized = False
            return False
    
    def get_metrics(self) -> Optional[StarlinkMetrics]:
        """
        Get current Starlink metrics
        
        Returns:
            StarlinkMetrics object or None if failed
        """
        if not self.initialized:
            return None
        
        try:
            # Simulate getting metrics - in real implementation, this would query the router
            # For demo purposes, return mock data
            metrics = StarlinkMetrics(
                timestamp=time.time(),
                status="online",
                satellites_connected=8,
                download_speed=150.5,
                upload_speed=25.3,
                latency=35.2,
                packet_loss=0.5,
                signal_strength=-85.5,
                snr=12.5,
                azimuth=180.0,
                elevation=45.0,
                obstruction_percent=2.1,
                dish_power_usage=85.0,
                dish_temp=42.5,
                router_temp=38.0,
                boot_count=5
            )
            
            # Add to history
            self.metrics_history.append(metrics)
            
            return metrics
        except Exception as e:
            print(f"Failed to get metrics: {e}")
            return None
    
    def set_thresholds(self, **kwargs):
        """
        Set monitoring thresholds
        
        Args:
            **kwargs: Threshold key-value pairs to update
        """
        for key, value in kwargs.items():
            if key in self.thresholds:
                self.thresholds[key] = value
    
    def get_performance_report(self, hours: int = 24) -> Dict:
        """
        Generate performance report for specified time period
        
        Args:
            hours: Number of hours to include in report
            
        Returns:
            Dictionary containing performance metrics
        """
        if not self.metrics_history:
            return {
                'status': 'no_data',
                'samples': 0,
                'availability_percent': 0.0,
                'issues_count': 0,
                'active_alerts': 0,
                'averages': {
                    'download_speed': 0.0,
                    'upload_speed': 0.0,
                    'latency': 0.0
                },
                'current_status': 'unknown',
                'current_download': 0.0,
                'current_latency': 0.0
            }
        
        # Filter metrics by time period
        cutoff_time = time.time() - (hours * 3600)
        recent_metrics = [m for m in self.metrics_history if m.timestamp >= cutoff_time]
        
        if not recent_metrics:
            recent_metrics = list(self.metrics_history)
        
        # Calculate averages
        avg_download = sum(m.download_speed for m in recent_metrics) / len(recent_metrics)
        avg_upload = sum(m.upload_speed for m in recent_metrics) / len(recent_metrics)
        avg_latency = sum(m.latency for m in recent_metrics) / len(recent_metrics)
        
        # Count online samples
        online_count = sum(1 for m in recent_metrics if m.status == 'online')
        availability = (online_count / len(recent_metrics)) * 100
        
        # Count issues
        issues = sum(1 for m in recent_metrics if (
            m.download_speed < self.thresholds['min_download_speed'] or
            m.latency > self.thresholds['max_latency'] or
            m.packet_loss > self.thresholds['max_packet_loss'] or
            m.obstruction_percent > self.thresholds['max_obstruction']
        ))
        
        # Get current metrics
        current = recent_metrics[-1] if recent_metrics else None
        
        return {
            'status': 'ok',
            'samples': len(recent_metrics),
            'availability_percent': availability,
            'issues_count': issues,
            'active_alerts': 0,  # Could implement active alert tracking
            'averages': {
                'download_speed': avg_download,
                'upload_speed': avg_upload,
                'latency': avg_latency
            },
            'current_status': current.status if current else 'unknown',
            'current_download': current.download_speed if current else 0.0,
            'current_latency': current.latency if current else 0.0
        }
    
    def start_monitoring(self, interval: int = 60):
        """
        Start continuous monitoring in background thread
        
        Args:
            interval: Monitoring interval in seconds
        """
        if self.monitoring:
            return
        
        self.monitoring = True
        
        def monitor_loop():
            while self.monitoring:
                self.get_metrics()
                time.sleep(interval)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def reboot_dish(self) -> bool:
        """
        Send reboot command to Starlink dish
        
        Returns:
            True if command sent successfully, False otherwise
        """
        if not self.initialized:
            return False
        
        try:
            # Simulate reboot command - in real implementation, this would send the command
            print("Reboot command would be sent to Starlink dish")
            return True
        except Exception as e:
            print(f"Failed to reboot dish: {e}")
            return False
