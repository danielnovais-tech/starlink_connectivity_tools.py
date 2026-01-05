"""
Starlink Monitor Module
Provides monitoring capabilities for Starlink satellite connections
"""

import time
import threading
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from collections import deque

from src.config import Config


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
    
    def __init__(self, host: str = None, history_size: int = None, config: Config = None):
        """
        Initialize Starlink monitor
        
        Args:
            host: Starlink router IP address (overrides config)
            history_size: Number of historical metrics to retain (overrides config)
            config: Configuration object (creates default if None)
        """
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        
        self.host = host or self.config.get('monitor.default_host', '192.168.100.1')
        self.history_size = history_size or self.config.get('monitor.history_size', 1000)
        self.metrics_history: deque = deque(maxlen=self.history_size)
        self.initialized = False
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Load thresholds from config
        self.thresholds = self.config.get_thresholds()
        
        # Try to initialize connection
        self._initialize()
    
    def _initialize(self):
        """Initialize connection to Starlink router"""
        try:
            # TODO: Replace with actual Starlink router connection logic
            # For now, we'll mark as initialized to allow the CLI to work
            self.logger.info(f"Initializing connection to Starlink router at {self.host}")
            self.initialized = True
            self.logger.info("Starlink monitor initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Starlink connection: {e}")
            self.initialized = False
            return False
    
    def get_metrics(self) -> Optional[StarlinkMetrics]:
        """
        Get current Starlink metrics
        
        Returns:
            StarlinkMetrics object or None if failed
        """
        if not self.initialized:
            self.logger.warning("Cannot get metrics: monitor not initialized")
            return None
        
        try:
            # TODO: Replace with actual Starlink router API calls
            # For demo purposes, return mock data
            self.logger.debug("Fetching current metrics from Starlink router")
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
            self.logger.debug(f"Metrics retrieved: {metrics.download_speed} Mbps down, {metrics.latency} ms latency")
            
            return metrics
        except Exception as e:
            self.logger.error(f"Failed to get metrics: {e}", exc_info=True)
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
                self.logger.info(f"Threshold updated: {key} = {value}")
        # Save to config
        self.config.set_thresholds(**kwargs)
    
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
    
    def start_monitoring(self, interval: int = None):
        """
        Start continuous monitoring in background thread
        
        Args:
            interval: Monitoring interval in seconds (uses config default if None)
        """
        if self.monitoring:
            self.logger.warning("Monitoring already started")
            return
        
        interval = interval or self.config.get('monitor.default_interval', 60)
        self.logger.info(f"Starting continuous monitoring with {interval}s interval")
        self.monitoring = True
        
        def monitor_loop():
            while self.monitoring:
                try:
                    self.get_metrics()
                except Exception as e:
                    self.logger.error(f"Error in monitoring loop: {e}", exc_info=True)
                time.sleep(interval)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        if not self.monitoring:
            return
        
        self.logger.info("Stopping monitoring")
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
            self.logger.error("Cannot reboot: monitor not initialized")
            return False
        
        try:
            # TODO: Replace with actual reboot command implementation
            self.logger.warning("Sending reboot command to Starlink dish")
            self.logger.info("Reboot command would be sent to Starlink dish")
            return True
        except Exception as e:
            self.logger.error(f"Failed to reboot dish: {e}", exc_info=True)
            return False
