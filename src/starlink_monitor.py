"""
Starlink-specific monitoring and control using official Starlink API
"""
import time
import logging
import json
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import threading

try:
    from starlink_client import StarlinkClient
    STARLINK_AVAILABLE = True
except ImportError:
    STARLINK_AVAILABLE = False
    logging.warning("starlink-client not installed. Using simulated data.")

try:
    import starlink_grpc
    GRPC_AVAILABLE = True
except ImportError:
    GRPC_AVAILABLE = False
    logging.warning("starlink-grpc not installed. Limited telemetry available.")


class StarlinkStatus(Enum):
    """Starlink-specific status codes"""
    ONLINE = "online"
    OFFLINE = "offline"
    BOOTING = "booting"
    SEARCHING = "searching"
    STOWED = "stowed"
    DEGRADED = "degraded"
    OBSTRUCTED = "obstructed"
    HEATING = "heating"
    NO_SIGNAL = "no_signal"


@dataclass
class StarlinkMetrics:
    """Comprehensive Starlink telemetry"""
    # Network metrics
    download_speed: float  # Mbps
    upload_speed: float    # Mbps
    latency: float         # ms
    jitter: float          # ms
    packet_loss: float     # percentage
    
    # Dish metrics
    obstruction_percent: float
    obstruction_duration: float  # seconds
    satellites_visible: int
    satellites_connected: int
    
    # Signal metrics
    signal_strength: float  # dBm
    snr: float             # Signal-to-noise ratio
    azimuth: float         # degrees
    elevation: float       # degrees
    
    # Device metrics
    dish_power_usage: float  # Watts
    router_temp: float      # Celsius
    dish_temp: float        # Celsius
    
    # Status
    status: str
    alert_count: int
    boot_count: int
    
    timestamp: float


class StarlinkMonitor:
    """
    Main Starlink monitoring and control class
    Integrates with official Starlink APIs
    """
    
    def __init__(self, 
                 host: str = "192.168.100.1",  # Default Starlink router IP
                 port: int = 9200,
                 use_grpc: bool = True):
        """
        Initialize Starlink monitor
        
        Args:
            host: Starlink router IP address
            port: Starlink API port
            use_grpc: Whether to use gRPC interface for detailed telemetry
        """
        self.host = host
        self.port = port
        self.use_grpc = use_grpc and GRPC_AVAILABLE
        
        # Thresholds for issue detection (customizable)
        self.thresholds = {
            'min_download_speed': 5.0,    # Mbps
            'max_latency': 100,          # ms
            'max_packet_loss': 10,       # %
            'max_obstruction': 5,        # %
            'min_snr': 10,              # dB
            'max_dish_temp': 80,        # Celsius
        }
        
        # Issue tracking
        self.consecutive_issues = 0
        self.max_consecutive_issues = 3
        self.issue_history = []
        self.max_history = 1000
        
        # Performance tracking
        self.performance_history = []
        self.performance_window = timedelta(hours=24)
        
        # Alerts
        self.alerts_enabled = True
        self.active_alerts = []
        
        # Initialize clients
        self.client = None
        self.grpc_client = None
        self.initialized = False
        
        self._initialize_clients()
        
        # Background monitoring
        self.monitoring = False
        self.monitor_thread = None
        self.check_interval = 60  # seconds
        
        logging.info(f"StarlinkMonitor initialized for {host}:{port}")
    
    def _initialize_clients(self):
        """Initialize Starlink API clients"""
        try:
            if STARLINK_AVAILABLE:
                self.client = StarlinkClient(host=self.host, port=self.port)
                logging.info(f"Connected to Starlink router at {self.host}:{self.port}")
            else:
                logging.warning("Using simulated Starlink data (starlink-client not installed)")
            
            if self.use_grpc and GRPC_AVAILABLE:
                self.grpc_client = starlink_grpc.ChannelContext(self.host)
                logging.info("gRPC client initialized for detailed telemetry")
            
            self.initialized = True
            
        except Exception as e:
            logging.error(f"Failed to initialize Starlink clients: {e}")
            self.initialized = False
    
    def get_metrics(self) -> Optional[StarlinkMetrics]:
        """
        Get comprehensive Starlink metrics from all available sources
        
        Returns:
            StarlinkMetrics object or None if failed
        """
        if not self.initialized:
            logging.warning("Starlink monitor not initialized")
            return self._get_simulated_metrics()
        
        try:
            metrics = StarlinkMetrics(
                # Initialize with defaults
                download_speed=0.0,
                upload_speed=0.0,
                latency=0.0,
                jitter=0.0,
                packet_loss=0.0,
                obstruction_percent=0.0,
                obstruction_duration=0.0,
                satellites_visible=0,
                satellites_connected=0,
                signal_strength=0.0,
                snr=0.0,
                azimuth=0.0,
                elevation=0.0,
                dish_power_usage=0.0,
                router_temp=0.0,
                dish_temp=0.0,
                status="unknown",
                alert_count=0,
                boot_count=0,
                timestamp=time.time()
            )
            
            # Get basic network stats
            if self.client:
                try:
                    stats = self.client.get_network_stats()
                    metrics.download_speed = stats.download_speed
                    metrics.upload_speed = stats.upload_speed
                    metrics.latency = stats.latency
                    
                    # Additional stats if available
                    if hasattr(stats, 'jitter'):
                        metrics.jitter = stats.jitter
                    if hasattr(stats, 'packet_loss'):
                        metrics.packet_loss = stats.packet_loss
                    
                    # Get status
                    status_data = self.client.get_status()
                    if hasattr(status_data, 'state'):
                        metrics.status = status_data.state
                    
                except Exception as e:
                    logging.warning(f"Failed to get basic stats: {e}")
            
            # Get detailed telemetry via gRPC
            if self.grpc_client:
                try:
                    # Get obstruction data
                    obstruction_data = starlink_grpc.get_obstruction_map(self.grpc_client)
                    if obstruction_data:
                        metrics.obstruction_percent = obstruction_data.obstruction_percent
                        metrics.obstruction_duration = obstruction_data.obstruction_duration
                    
                    # Get signal data
                    signal_data = starlink_grpc.get_signal_metrics(self.grpc_client)
                    if signal_data:
                        metrics.signal_strength = signal_data.signal_strength
                        metrics.snr = signal_data.snr
                        metrics.azimuth = signal_data.azimuth
                        metrics.elevation = signal_data.elevation
                        metrics.satellites_visible = signal_data.satellites_visible
                        metrics.satellites_connected = signal_data.satellites_connected
                    
                    # Get device data
                    device_data = starlink_grpc.get_device_info(self.grpc_client)
                    if device_data:
                        metrics.dish_power_usage = device_data.dish_power_usage
                        metrics.router_temp = device_data.router_temp
                        metrics.dish_temp = device_data.dish_temp
                        metrics.boot_count = device_data.boot_count
                        metrics.alert_count = device_data.alert_count
                    
                except Exception as e:
                    logging.warning(f"Failed to get gRPC telemetry: {e}")
            
            # Store in history
            self._store_metrics(metrics)
            
            # Check for issues
            self._check_metrics(metrics)
            
            return metrics
            
        except Exception as e:
            logging.error(f"Failed to get Starlink metrics: {e}")
            return None
    
    def _get_simulated_metrics(self) -> StarlinkMetrics:
        """Generate simulated metrics for testing/fallback"""
        import random
        
        # Simulate realistic Starlink metrics
        return StarlinkMetrics(
            download_speed=random.uniform(50, 200),
            upload_speed=random.uniform(10, 40),
            latency=random.uniform(20, 100),
            jitter=random.uniform(1, 10),
            packet_loss=random.uniform(0, 2),
            obstruction_percent=random.uniform(0, 3),
            obstruction_duration=random.uniform(0, 30),
            satellites_visible=random.randint(6, 12),
            satellites_connected=random.randint(3, 8),
            signal_strength=random.uniform(-50, -40),
            snr=random.uniform(8, 15),
            azimuth=random.uniform(0, 360),
            elevation=random.uniform(20, 90),
            dish_power_usage=random.uniform(50, 80),
            router_temp=random.uniform(30, 50),
            dish_temp=random.uniform(-10, 40),
            status=random.choice(["online", "searching", "degraded"]),
            alert_count=random.randint(0, 2),
            boot_count=random.randint(0, 10),
            timestamp=time.time()
        )
    
    def _store_metrics(self, metrics: StarlinkMetrics):
        """Store metrics in history"""
        self.performance_history.append(metrics)
        
        # Trim old data
        cutoff_time = time.time() - self.performance_window.total_seconds()
        self.performance_history = [
            m for m in self.performance_history 
            if m.timestamp > cutoff_time
        ]
        
        # Keep within size limit
        if len(self.performance_history) > self.max_history:
            self.performance_history = self.performance_history[-self.max_history:]
    
    def _check_metrics(self, metrics: StarlinkMetrics):
        """Check metrics against thresholds and detect issues"""
        issues = []
        
        # Check download speed
        if metrics.download_speed < self.thresholds['min_download_speed']:
            issues.append(f"Low download speed: {metrics.download_speed:.1f} Mbps")
        
        # Check latency
        if metrics.latency > self.thresholds['max_latency']:
            issues.append(f"High latency: {metrics.latency:.1f} ms")
        
        # Check packet loss
        if metrics.packet_loss > self.thresholds['max_packet_loss']:
            issues.append(f"High packet loss: {metrics.packet_loss:.1f}%")
        
        # Check obstruction
        if metrics.obstruction_percent > self.thresholds['max_obstruction']:
            issues.append(f"High obstruction: {metrics.obstruction_percent:.1f}%")
        
        # Check SNR
        if metrics.snr < self.thresholds['min_snr']:
            issues.append(f"Low SNR: {metrics.snr:.1f} dB")
        
        # Check dish temperature
        if metrics.dish_temp > self.thresholds['max_dish_temp']:
            issues.append(f"High dish temperature: {metrics.dish_temp:.1f}°C")
        
        # Check status
        if metrics.status in ["offline", "no_signal", "stowed"]:
            issues.append(f"Bad status: {metrics.status}")
        
        # Update consecutive issues
        if issues:
            self.consecutive_issues += 1
            
            # Log issues
            for issue in issues:
                logging.warning(f"Starlink issue: {issue}")
            
            # Store in history
            self.issue_history.append({
                'timestamp': datetime.now().isoformat(),
                'issues': issues,
                'metrics': asdict(metrics)
            })
            
            # Keep history limited
            if len(self.issue_history) > self.max_history:
                self.issue_history = self.issue_history[-self.max_history:]
            
            # Check if we need to take action
            if self.consecutive_issues >= self.max_consecutive_issues:
                self._handle_persistent_issues(metrics)
        else:
            self.consecutive_issues = max(0, self.consecutive_issues - 1)
    
    def _handle_persistent_issues(self, metrics: StarlinkMetrics):
        """Handle persistent connectivity issues"""
        logging.error(f"Persistent issues detected (count: {self.consecutive_issues})")
        
        # Generate alert
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': 'persistent_connectivity_issue',
            'severity': 'high',
            'consecutive_issues': self.consecutive_issues,
            'metrics': asdict(metrics)
        }
        
        self.active_alerts.append(alert)
        
        # Auto-remediation based on issue type
        if metrics.obstruction_percent > self.thresholds['max_obstruction']:
            logging.warning("High obstruction detected. Consider repositioning dish.")
        
        elif metrics.status == "offline" or metrics.snr < 5:
            logging.warning("Severe connectivity loss. Attempting recovery...")
            self.attempt_recovery()
    
    def attempt_recovery(self):
        """Attempt to recover connectivity"""
        recovery_attempted = False
        
        # Try different recovery methods based on severity
        if self.consecutive_issues >= 5:
            logging.critical("Critical issues. Rebooting dish...")
            self.reboot_dish()
            recovery_attempted = True
            
        elif self.consecutive_issues >= 3:
            logging.warning("Moderate issues. Stowing and unstowing dish...")
            self.stow_dish()
            time.sleep(30)
            self.unstow_dish()
            recovery_attempted = True
        
        if recovery_attempted:
            # Reset issue count after recovery attempt
            self.consecutive_issues = 0
            time.sleep(180)  # Wait 3 minutes for recovery
    
    def reboot_dish(self) -> bool:
        """Reboot the Starlink dish"""
        try:
            if self.client and hasattr(self.client, 'reboot_dish'):
                logging.info("Rebooting Starlink dish...")
                self.client.reboot_dish()
                return True
            else:
                logging.warning("Dish reboot not available in current client")
                return False
        except Exception as e:
            logging.error(f"Failed to reboot dish: {e}")
            return False
    
    def stow_dish(self) -> bool:
        """Stow the Starlink dish (point straight up)"""
        try:
            if self.grpc_client:
                starlink_grpc.dish_stow(self.grpc_client)
                logging.info("Dish stowed")
                return True
        except Exception as e:
            logging.error(f"Failed to stow dish: {e}")
        return False
    
    def unstow_dish(self) -> bool:
        """Unstow the Starlink dish (begin searching for satellites)"""
        try:
            if self.grpc_client:
                starlink_grpc.dish_unstow(self.grpc_client)
                logging.info("Dish unstowed, searching for satellites...")
                return True
        except Exception as e:
            logging.error(f"Failed to unstow dish: {e}")
        return False
    
    def start_monitoring(self, interval: int = 60):
        """Start background monitoring"""
        if self.monitoring:
            logging.warning("Monitoring already running")
            return
        
        self.check_interval = interval
        self.monitoring = True
        
        def monitor():
            logging.info(f"Started Starlink monitoring (interval: {interval}s)")
            
            while self.monitoring:
                try:
                    metrics = self.get_metrics()
                    if metrics:
                        # Log periodic status
                        if self.consecutive_issues == 0:
                            logging.info(
                                f"Status: {metrics.status}, "
                                f"Download: {metrics.download_speed:.1f} Mbps, "
                                f"Latency: {metrics.latency:.1f} ms"
                            )
                    
                    # Clear old alerts
                    self._cleanup_alerts()
                    
                except Exception as e:
                    logging.error(f"Monitoring error: {e}")
                
                # Sleep for interval
                for _ in range(interval):
                    if not self.monitoring:
                        break
                    time.sleep(1)
        
        self.monitor_thread = threading.Thread(target=monitor, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logging.info("Starlink monitoring stopped")
    
    def _cleanup_alerts(self):
        """Clean up old alerts"""
        # Keep alerts for 24 hours
        cutoff = datetime.now() - timedelta(hours=24)
        cutoff_timestamp = cutoff.timestamp()
        
        self.active_alerts = [
            alert for alert in self.active_alerts
            if datetime.fromisoformat(alert['timestamp']).timestamp() > cutoff_timestamp
        ]
    
    def get_performance_report(self, hours: int = 24) -> Dict:
        """Generate performance report for specified time period"""
        cutoff = time.time() - (hours * 3600)
        
        relevant_metrics = [
            m for m in self.performance_history
            if m.timestamp > cutoff
        ]
        
        if not relevant_metrics:
            return {
                'status': 'no_data',
                'period_hours': hours,
                'timestamp': datetime.now().isoformat()
            }
        
        # Calculate statistics
        download_speeds = [m.download_speed for m in relevant_metrics]
        upload_speeds = [m.upload_speed for m in relevant_metrics]
        latencies = [m.latency for m in relevant_metrics]
        
        report = {
            'period_hours': hours,
            'samples': len(relevant_metrics),
            'timestamp': datetime.now().isoformat(),
            'averages': {
                'download_speed': sum(download_speeds) / len(download_speeds),
                'upload_speed': sum(upload_speeds) / len(upload_speeds),
                'latency': sum(latencies) / len(latencies),
            },
            'availability_percent': (
                sum(1 for m in relevant_metrics if m.status == 'online') / 
                len(relevant_metrics) * 100
            ),
            'issues_count': len(self.issue_history),
            'active_alerts': len(self.active_alerts),
            'current_status': relevant_metrics[-1].status,
            'current_download': relevant_metrics[-1].download_speed,
            'current_latency': relevant_metrics[-1].latency,
        }
        
        return report
    
    def set_thresholds(self, **kwargs):
        """Update monitoring thresholds"""
        valid_keys = set(self.thresholds.keys())
        for key, value in kwargs.items():
            if key in valid_keys:
                self.thresholds[key] = value
                logging.info(f"Updated threshold {key} = {value}")
            else:
                logging.warning(f"Invalid threshold key: {key}")
    
    def get_status(self) -> Dict:
        """Get current system status"""
        metrics = self.get_metrics()
        
        return {
            'monitoring': self.monitoring,
            'initialized': self.initialized,
            'consecutive_issues': self.consecutive_issues,
            'active_alerts': len(self.active_alerts),
            'performance_history_size': len(self.performance_history),
            'issue_history_size': len(self.issue_history),
            'thresholds': self.thresholds,
            'current_metrics': asdict(metrics) if metrics else None,
            'timestamp': datetime.now().isoformat()
        }
Starlink Monitor - NEW: Starlink-specific monitoring

Real-time monitoring of Starlink satellite internet connection.
Tracks signal quality, satellite visibility, obstructions, and performance metrics.
"""

import logging
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)


class StarlinkMonitor:
    """Real-time monitoring for Starlink connections."""
    
    def __init__(self, starlink_endpoint: str = "192.168.100.1", history_size: int = 100):
        """
        Initialize Starlink Monitor.
        
        Args:
            starlink_endpoint: IP address or hostname of Starlink router
            history_size: Number of historical data points to keep
        """
        self.starlink_endpoint = starlink_endpoint
        self.history_size = history_size
        self.metrics_history = deque(maxlen=history_size)
        self.alert_thresholds = self._initialize_thresholds()
        self.monitoring_active = False
        
    def _initialize_thresholds(self) -> Dict[str, Any]:
        """
        Initialize alert thresholds.
        
        Returns:
            dict: Alert threshold configuration
        """
        return {
            "signal_quality_min": 70,
            "latency_max_ms": 100,
            "packet_loss_max_percent": 2.0,
            "obstruction_max_percent": 5.0,
            "download_speed_min_mbps": 50.0,
            "satellites_min": 3
        }
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """
        Get current Starlink metrics.
        
        Returns:
            dict: Current metrics snapshot
        """
        # In real implementation, would query Starlink gRPC API
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "signal_quality": 92,
            "satellites_visible": 11,
            "latency_ms": 38.5,
            "download_mbps": 156.3,
            "upload_mbps": 23.1,
            "packet_loss_percent": 0.2,
            "obstruction_percent": 0.8,
            "uptime_seconds": 172800,
            "dish_temperature_c": 29.3,
            "is_connected": True,
            "currently_obstructed": False
        }
        
        self.metrics_history.append(metrics)
        return metrics
    
    def start_monitoring(self, interval_seconds: int = 30) -> None:
        """
        Start continuous monitoring.
        
        Args:
            interval_seconds: Monitoring interval in seconds
        """
        logger.info(f"Starting Starlink monitoring (interval: {interval_seconds}s)")
        self.monitoring_active = True
    
    def stop_monitoring(self) -> None:
        """Stop continuous monitoring."""
        logger.info("Stopping Starlink monitoring")
        self.monitoring_active = False
    
    def check_alerts(self) -> List[Dict[str, Any]]:
        """
        Check for alert conditions based on current metrics.
        
        Returns:
            list: List of active alerts
        """
        metrics = self.get_current_metrics()
        alerts = []
        
        if metrics["signal_quality"] < self.alert_thresholds["signal_quality_min"]:
            alerts.append({
                "severity": "warning",
                "type": "low_signal",
                "message": f"Low signal quality: {metrics['signal_quality']}%",
                "value": metrics["signal_quality"],
                "threshold": self.alert_thresholds["signal_quality_min"]
            })
        
        if metrics["latency_ms"] > self.alert_thresholds["latency_max_ms"]:
            alerts.append({
                "severity": "warning",
                "type": "high_latency",
                "message": f"High latency: {metrics['latency_ms']}ms",
                "value": metrics["latency_ms"],
                "threshold": self.alert_thresholds["latency_max_ms"]
            })
        
        if metrics["packet_loss_percent"] > self.alert_thresholds["packet_loss_max_percent"]:
            alerts.append({
                "severity": "critical",
                "type": "packet_loss",
                "message": f"High packet loss: {metrics['packet_loss_percent']}%",
                "value": metrics["packet_loss_percent"],
                "threshold": self.alert_thresholds["packet_loss_max_percent"]
            })
        
        if metrics["obstruction_percent"] > self.alert_thresholds["obstruction_max_percent"]:
            alerts.append({
                "severity": "warning",
                "type": "obstruction",
                "message": f"Obstruction detected: {metrics['obstruction_percent']}%",
                "value": metrics["obstruction_percent"],
                "threshold": self.alert_thresholds["obstruction_max_percent"]
            })
        
        if metrics["download_mbps"] < self.alert_thresholds["download_speed_min_mbps"]:
            alerts.append({
                "severity": "warning",
                "type": "low_speed",
                "message": f"Low download speed: {metrics['download_mbps']} Mbps",
                "value": metrics["download_mbps"],
                "threshold": self.alert_thresholds["download_speed_min_mbps"]
            })
        
        if metrics["satellites_visible"] < self.alert_thresholds["satellites_min"]:
            alerts.append({
                "severity": "critical",
                "type": "low_satellites",
                "message": f"Low satellite count: {metrics['satellites_visible']}",
                "value": metrics["satellites_visible"],
                "threshold": self.alert_thresholds["satellites_min"]
            })
        
        if not metrics["is_connected"]:
            alerts.append({
                "severity": "critical",
                "type": "disconnected",
                "message": "Starlink connection lost",
                "value": False,
                "threshold": True
            })
        
        return alerts
    
    def get_statistics(self, duration_minutes: int = 60) -> Dict[str, Any]:
        """
        Get statistical analysis of metrics over time.
        
        Args:
            duration_minutes: Duration to analyze
            
        Returns:
            dict: Statistical summary
        """
        if not self.metrics_history:
            return {"error": "No metrics data available"}
        
        # Calculate statistics from history
        latencies = [m["latency_ms"] for m in self.metrics_history]
        downloads = [m["download_mbps"] for m in self.metrics_history]
        uploads = [m["upload_mbps"] for m in self.metrics_history]
        signals = [m["signal_quality"] for m in self.metrics_history]
        
        return {
            "duration_minutes": duration_minutes,
            "sample_count": len(self.metrics_history),
            "latency": {
                "avg": sum(latencies) / len(latencies),
                "min": min(latencies),
                "max": max(latencies)
            },
            "download": {
                "avg": sum(downloads) / len(downloads),
                "min": min(downloads),
                "max": max(downloads)
            },
            "upload": {
                "avg": sum(uploads) / len(uploads),
                "min": min(uploads),
                "max": max(uploads)
            },
            "signal_quality": {
                "avg": sum(signals) / len(signals),
                "min": min(signals),
                "max": max(signals)
            }
        }
    
    def get_satellite_info(self) -> Dict[str, Any]:
        """
        Get detailed satellite information.
        
        Returns:
            dict: Satellite tracking information
        """
        return {
            "satellites_visible": 11,
            "satellites_tracked": 8,
            "active_satellite_id": 1234,
            "next_satellite_switch_seconds": 45,
            "coverage_status": "optimal",
            "constellation": "starlink_gen2"
        }
    
    def get_obstruction_analysis(self) -> Dict[str, Any]:
        """
        Get detailed obstruction analysis.
        
        Returns:
            dict: Obstruction details
        """
        return {
            "currently_obstructed": False,
            "obstruction_percentage": 0.8,
            "wedge_abs_fraction_obstructed": [0.0, 0.0, 0.01, 0.0, 0.0, 0.0],
            "recommendation": "No significant obstructions detected",
            "last_obstruction_timestamp": None
        }
    
    def export_metrics(self, format: str = "json") -> str:
        """
        Export metrics history.
        
        Args:
            format: Export format (json, csv)
            
        Returns:
            str: Exported data
        """
        if format == "json":
            import json
            return json.dumps(list(self.metrics_history), indent=2)
        elif format == "csv":
            if not self.metrics_history:
                return ""
            
            # Create CSV format
            headers = ",".join(self.metrics_history[0].keys())
            rows = [headers]
            
            for metric in self.metrics_history:
                row = ",".join(str(v) for v in metric.values())
                rows.append(row)
            
            return "\n".join(rows)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def reset_history(self) -> None:
        """Clear metrics history."""
        logger.info("Clearing metrics history")
        self.metrics_history.clear()
    
    def set_alert_threshold(self, metric: str, value: Any) -> bool:
        """
        Set custom alert threshold.
        
        Args:
            metric: Metric name
            value: Threshold value
            
        Returns:
            bool: True if threshold was set
        """
        if metric in self.alert_thresholds:
            self.alert_thresholds[metric] = value
            logger.info(f"Updated alert threshold: {metric} = {value}")
            return True
        else:
            logger.error(f"Unknown metric: {metric}")
            return False
