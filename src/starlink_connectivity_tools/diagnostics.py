"""Enhanced diagnostics with Starlink telemetry integration."""

import json
import numpy as np
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import deque
from loguru import logger

from .starlink_api import StarlinkAPI
from .satellite_connection_manager import SatelliteConnectionManager, ConnectionType


class Alert:
    """Represents a diagnostic alert."""

    def __init__(
        self,
        alert_type: str,
        severity: str,
        message: str,
        recommendation: str,
        timestamp: Optional[datetime] = None,
    ):
        """Initialize an alert."""
        self.alert_type = alert_type
        self.severity = severity  # "info", "warning", "critical"
        self.message = message
        self.recommendation = recommendation
        self.timestamp = timestamp or datetime.now()
        self.acknowledged = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary."""
        return {
            "type": self.alert_type,
            "severity": self.severity,
            "message": self.message,
            "recommendation": self.recommendation,
            "timestamp": self.timestamp.isoformat(),
            "acknowledged": self.acknowledged,
        }


class DiagnosticsEngine:
    """Enhanced diagnostics with historical tracking and automated alerting."""

    def __init__(self, connection_manager: SatelliteConnectionManager):
        """
        Initialize diagnostics engine.

        Args:
            connection_manager: Satellite connection manager instance
        """
        self.connection_manager = connection_manager
        self.alerts: List[Alert] = []
        self.performance_baseline: Dict[str, float] = {}
        self.telemetry_history: deque = deque(maxlen=2000)
        self.last_diagnostic_run: Optional[datetime] = None

    def run_full_diagnostic(self) -> Dict[str, Any]:
        """
        Run comprehensive diagnostic check.

        Returns:
            Complete diagnostic report
        """
        logger.info("Running full diagnostic check")
        
        active_conn = self.connection_manager.get_active_connection()
        
        if not active_conn:
            alert = Alert(
                "connectivity",
                "critical",
                "No active connection",
                "Check satellite dish and establish connection",
            )
            self.alerts.append(alert)
            return {
                "status": "critical",
                "alerts": [a.to_dict() for a in self.alerts],
                "timestamp": datetime.now().isoformat(),
            }

        # Collect telemetry
        telemetry = self._collect_telemetry(active_conn)
        self.telemetry_history.append(telemetry)

        # Run diagnostic checks
        self._check_connection_quality(telemetry)
        self._check_hardware_status(telemetry)
        self._check_performance_degradation(telemetry)
        self._check_obstructions(telemetry)

        self.last_diagnostic_run = datetime.now()

        return {
            "status": self._get_overall_status(),
            "connection": active_conn.name,
            "telemetry": telemetry,
            "alerts": [a.to_dict() for a in self.alerts if not a.acknowledged],
            "all_alerts": [a.to_dict() for a in self.alerts],
            "timestamp": datetime.now().isoformat(),
        }

    def _collect_telemetry(self, connection) -> Dict[str, Any]:
        """Collect telemetry from active connection."""
        telemetry = {
            "timestamp": datetime.now().isoformat(),
            "connection_name": connection.name,
            "connection_type": connection.connection_type.value,
            "metrics": connection.metrics.copy(),
        }

        # Get additional Starlink-specific telemetry
        if connection.connection_type == ConnectionType.STARLINK and connection.api_client:
            try:
                status = connection.api_client.get_status()
                telemetry["starlink_status"] = status
                
                obstruction_map = connection.api_client.get_obstruction_map()
                telemetry["obstruction_map"] = obstruction_map
                
            except Exception as e:
                logger.error(f"Error collecting Starlink telemetry: {e}")

        return telemetry

    def _check_connection_quality(self, telemetry: Dict[str, Any]):
        """Check connection quality metrics."""
        metrics = telemetry.get("metrics", {})
        
        # Check latency
        latency = metrics.get("latency_ms", 0)
        if latency > 200:
            self.alerts.append(Alert(
                "latency",
                "critical" if latency > 500 else "warning",
                f"High latency detected: {latency:.1f}ms",
                "Check for obstructions, network congestion, or try failover to backup connection",
            ))
        
        # Check bandwidth
        downlink = metrics.get("downlink_mbps", 0)
        if downlink < 5:
            self.alerts.append(Alert(
                "bandwidth",
                "warning",
                f"Low downlink bandwidth: {downlink:.1f} Mbps",
                "Check for obstructions or signal interference",
            ))

        # Check SNR
        snr = metrics.get("snr", 0)
        if snr < 5:
            self.alerts.append(Alert(
                "signal",
                "warning",
                f"Low signal-to-noise ratio: {snr:.1f} dB",
                "Check dish alignment and remove any obstructions",
            ))

    def _check_hardware_status(self, telemetry: Dict[str, Any]):
        """Check hardware status and alerts."""
        starlink_status = telemetry.get("starlink_status", {})
        alerts = starlink_status.get("alerts", [])

        for alert_type in alerts:
            severity = "critical" if "SHUTDOWN" in alert_type or "STUCK" in alert_type else "warning"
            
            recommendations = {
                "MOTORS_STUCK": "Reboot dish or check for mechanical obstructions",
                "THERMAL_THROTTLE": "Ensure adequate ventilation around dish",
                "THERMAL_SHUTDOWN": "Immediate action required: cool down the dish and check ventilation",
                "MAST_NOT_NEAR_VERTICAL": "Adjust dish mounting to be more vertical",
                "SLOW_ETHERNET_SPEEDS": "Check ethernet cable and connections",
                "SOFTWARE_INSTALL_PENDING": "Allow dish to complete software update",
            }

            self.alerts.append(Alert(
                "hardware",
                severity,
                f"Hardware alert: {alert_type}",
                recommendations.get(alert_type, "Contact support for assistance"),
            ))

    def _check_performance_degradation(self, telemetry: Dict[str, Any]):
        """Check for performance degradation over time."""
        if len(self.telemetry_history) < 10:
            return  # Not enough data

        # Calculate baseline if not set
        if not self.performance_baseline:
            self._establish_baseline()

        metrics = telemetry.get("metrics", {})
        
        # Compare to baseline
        if self.performance_baseline.get("downlink_mbps", 0) > 0:
            current_downlink = metrics.get("downlink_mbps", 0)
            baseline_downlink = self.performance_baseline["downlink_mbps"]
            
            if current_downlink < baseline_downlink * 0.5:
                self.alerts.append(Alert(
                    "degradation",
                    "warning",
                    f"Bandwidth degraded to {current_downlink / baseline_downlink * 100:.0f}% of baseline",
                    "Check for new obstructions or environmental changes",
                ))

    def _check_obstructions(self, telemetry: Dict[str, Any]):
        """Check for obstructions."""
        obstruction_map = telemetry.get("obstruction_map", {})
        
        if obstruction_map.get("obstructed", False):
            fraction = obstruction_map.get("fraction_obstructed", 0)
            
            severity = "critical" if fraction > 0.2 else "warning"
            
            self.alerts.append(Alert(
                "obstruction",
                severity,
                f"Obstruction detected: {fraction * 100:.1f}% of sky view blocked",
                "Remove obstructions or relocate dish to area with clearer sky view",
            ))

            # Analyze wedge data for directional information
            wedges = obstruction_map.get("wedge_fraction_obstructed", [])
            if wedges:
                max_wedge_idx = wedges.index(max(wedges))
                directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                             "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
                if max_wedge_idx < len(directions):
                    direction = directions[max_wedge_idx]
                    logger.info(f"Primary obstruction direction: {direction}")

    def _establish_baseline(self):
        """Establish performance baseline from historical data."""
        if len(self.telemetry_history) < 10:
            return
        
        # Use recent good performance as baseline
        recent_data = list(self.telemetry_history)[-100:]
        
        downlinks = [t.get("metrics", {}).get("downlink_mbps", 0) for t in recent_data]
        uplinks = [t.get("metrics", {}).get("uplink_mbps", 0) for t in recent_data]
        latencies = [t.get("metrics", {}).get("latency_ms", 0) for t in recent_data]
        snrs = [t.get("metrics", {}).get("snr", 0) for t in recent_data]

        self.performance_baseline = {
            "downlink_mbps": float(np.percentile(downlinks, 90)),
            "uplink_mbps": float(np.percentile(uplinks, 90)),
            "latency_ms": float(np.percentile(latencies, 10)),
            "snr": float(np.percentile(snrs, 90)),
        }

        logger.info(f"Established performance baseline: {self.performance_baseline}")

    def _get_overall_status(self) -> str:
        """Determine overall diagnostic status."""
        unacked_alerts = [a for a in self.alerts if not a.acknowledged]
        
        if not unacked_alerts:
            return "healthy"
        
        critical_count = sum(1 for a in unacked_alerts if a.severity == "critical")
        if critical_count > 0:
            return "critical"
        
        warning_count = sum(1 for a in unacked_alerts if a.severity == "warning")
        if warning_count > 2:
            return "degraded"
        
        return "warning"

    def acknowledge_alert(self, alert_index: int) -> bool:
        """
        Acknowledge an alert.

        Args:
            alert_index: Index of alert to acknowledge

        Returns:
            True if alert was acknowledged
        """
        if 0 <= alert_index < len(self.alerts):
            self.alerts[alert_index].acknowledged = True
            logger.info(f"Alert acknowledged: {self.alerts[alert_index].message}")
            return True
        return False

    def clear_acknowledged_alerts(self):
        """Remove all acknowledged alerts."""
        before_count = len(self.alerts)
        self.alerts = [a for a in self.alerts if not a.acknowledged]
        cleared = before_count - len(self.alerts)
        logger.info(f"Cleared {cleared} acknowledged alerts")

    def get_historical_performance(self, hours: int = 24) -> Dict[str, Any]:
        """
        Get historical performance data.

        Args:
            hours: Number of hours to retrieve

        Returns:
            Historical performance data
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_telemetry = [
            t for t in self.telemetry_history
            if datetime.fromisoformat(t["timestamp"]) > cutoff_time
        ]

        if not recent_telemetry:
            return {"error": "No historical data available"}
        
        # Extract time series data
        timestamps = [t["timestamp"] for t in recent_telemetry]
        latencies = [t.get("metrics", {}).get("latency_ms", 0) for t in recent_telemetry]
        downlinks = [t.get("metrics", {}).get("downlink_mbps", 0) for t in recent_telemetry]
        uplinks = [t.get("metrics", {}).get("uplink_mbps", 0) for t in recent_telemetry]
        snrs = [t.get("metrics", {}).get("snr", 0) for t in recent_telemetry]

        return {
            "period_hours": hours,
            "samples": len(recent_telemetry),
            "timestamps": timestamps,
            "latency_ms": {
                "values": latencies,
                "avg": float(np.mean(latencies)),
                "min": float(np.min(latencies)),
                "max": float(np.max(latencies)),
            },
            "downlink_mbps": {
                "values": downlinks,
                "avg": float(np.mean(downlinks)),
                "min": float(np.min(downlinks)),
                "max": float(np.max(downlinks)),
            },
            "uplink_mbps": {
                "values": uplinks,
                "avg": float(np.mean(uplinks)),
                "min": float(np.min(uplinks)),
                "max": float(np.max(uplinks)),
            },
            "snr": {
                "values": snrs,
                "avg": float(np.mean(snrs)),
                "min": float(np.min(snrs)),
                "max": float(np.max(snrs)),
            },
        }

    def generate_diagnostic_report(self, filepath: str):
        """
        Generate comprehensive diagnostic report.

        Args:
            filepath: Path to save report
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "last_diagnostic_run": self.last_diagnostic_run.isoformat() if self.last_diagnostic_run else None,
            "overall_status": self._get_overall_status(),
            "connection_stats": self.connection_manager.get_connection_stats(),
            "performance_baseline": self.performance_baseline,
            "active_alerts": [a.to_dict() for a in self.alerts if not a.acknowledged],
            "all_alerts": [a.to_dict() for a in self.alerts],
            "recent_telemetry": list(self.telemetry_history)[-100:],
        }

        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Diagnostic report saved to {filepath}")
