"""
Starlink Monitor
Monitors Starlink connection health and performance
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class StarlinkMonitor:
    """Monitors Starlink connection status and health"""
    
    def __init__(self):
        self.thresholds = {
            'min_download_speed': 10.0,
            'max_latency': 100,
            'max_packet_loss': 5,
            'max_obstruction': 5
        }
        self.monitoring_active = False
        
        logger.info("StarlinkMonitor initialized")
    
    def set_thresholds(self, min_download_speed: Optional[float] = None,
                      max_latency: Optional[int] = None,
                      max_packet_loss: Optional[float] = None,
                      max_obstruction: Optional[float] = None):
        """Set monitoring thresholds"""
        if min_download_speed is not None:
            self.thresholds['min_download_speed'] = min_download_speed
        if max_latency is not None:
            self.thresholds['max_latency'] = max_latency
        if max_packet_loss is not None:
            self.thresholds['max_packet_loss'] = max_packet_loss
        if max_obstruction is not None:
            self.thresholds['max_obstruction'] = max_obstruction
        
        logger.info(f"Thresholds updated: {self.thresholds}")
    
    def start_monitoring(self):
        """Start monitoring Starlink connection"""
        self.monitoring_active = True
        logger.info("Starlink monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring Starlink connection"""
        self.monitoring_active = False
        logger.info("Starlink monitoring stopped")
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current Starlink metrics"""
        # Simulated metrics
        return {
            'download_speed': 50.0,
            'upload_speed': 10.0,
            'latency': 45,
            'packet_loss': 0.2,
            'obstruction_percentage': 2.0,
            'uptime': 7200
        }
    
    def get_monitor_status(self) -> Dict[str, Any]:
        """Get monitoring status"""
        return {
            'monitoring_active': self.monitoring_active,
            'thresholds': self.thresholds,
            'current_metrics': self.get_current_metrics() if self.monitoring_active else None
        }
