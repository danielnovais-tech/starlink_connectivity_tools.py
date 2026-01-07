"""Crisis-optimized monitoring with adjustable thresholds and automatic recovery."""

import numpy as np
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from enum import Enum
from collections import deque
from loguru import logger

from .satellite_connection_manager import SatelliteConnectionManager


class ScenarioType(Enum):
    """Pre-configured crisis scenarios."""

    NORMAL = "normal"
    HUMANITARIAN = "humanitarian"
    MEDICAL = "medical"
    DISASTER = "disaster"
    CONFLICT = "conflict"
    CUSTOM = "custom"


class IssueType(Enum):
    """Types of detected issues."""

    HIGH_LATENCY = "high_latency"
    LOW_BANDWIDTH = "low_bandwidth"
    OBSTRUCTION = "obstruction"
    DISCONNECTION = "disconnection"
    SIGNAL_DEGRADATION = "signal_degradation"
    HARDWARE_ALERT = "hardware_alert"


class Issue:
    """Represents a detected issue."""

    def __init__(
        self,
        issue_type: IssueType,
        severity: str,
        description: str,
        detected_at: datetime,
        metrics: Optional[Dict[str, Any]] = None,
    ):
        """Initialize an issue."""
        self.issue_type = issue_type
        self.severity = severity  # "critical", "warning", "info"
        self.description = description
        self.detected_at = detected_at
        self.metrics = metrics or {}
        self.resolved_at: Optional[datetime] = None
        self.resolution_action: Optional[str] = None
        self.occurrence_count = 1

    def is_resolved(self) -> bool:
        """Check if issue is resolved."""
        return self.resolved_at is not None

    def mark_resolved(self, action: str):
        """Mark issue as resolved."""
        self.resolved_at = datetime.now()
        self.resolution_action = action


class CrisisMonitor:
    """Crisis-optimized monitoring with automatic issue detection and recovery."""

    # Threshold presets for different scenarios
    SCENARIO_THRESHOLDS = {
        ScenarioType.NORMAL: {
            "max_latency_ms": 100,
            "min_downlink_mbps": 20,
            "min_uplink_mbps": 5,
            "max_obstruction_percent": 0.05,
            "min_snr": 7.0,
        },
        ScenarioType.HUMANITARIAN: {
            "max_latency_ms": 200,
            "min_downlink_mbps": 10,
            "min_uplink_mbps": 2,
            "max_obstruction_percent": 0.15,
            "min_snr": 5.0,
        },
        ScenarioType.MEDICAL: {
            "max_latency_ms": 150,
            "min_downlink_mbps": 15,
            "min_uplink_mbps": 5,
            "max_obstruction_percent": 0.10,
            "min_snr": 6.0,
        },
        ScenarioType.DISASTER: {
            "max_latency_ms": 300,
            "min_downlink_mbps": 5,
            "min_uplink_mbps": 1,
            "max_obstruction_percent": 0.25,
            "min_snr": 4.0,
        },
        ScenarioType.CONFLICT: {
            "max_latency_ms": 250,
            "min_downlink_mbps": 8,
            "min_uplink_mbps": 2,
            "max_obstruction_percent": 0.20,
            "min_snr": 4.5,
        },
    }

    def __init__(
        self,
        connection_manager: SatelliteConnectionManager,
        scenario: ScenarioType = ScenarioType.NORMAL,
    ):
        """
        Initialize crisis monitor.

        Args:
            connection_manager: Satellite connection manager instance
            scenario: Crisis scenario type for threshold configuration
        """
        self.connection_manager = connection_manager
        self.scenario = scenario
        self.thresholds = self.SCENARIO_THRESHOLDS[scenario].copy()

        self.active_issues: List[Issue] = []
        self.resolved_issues: List[Issue] = []
        self.performance_history: deque = deque(maxlen=1000)

        self.monitoring = False
        self.monitor_interval = 10  # seconds
        self.auto_recovery_enabled = True
        self.issue_persistence_threshold = (
            3  # Number of consecutive detections before action
        )

        self.callbacks: Dict[str, List[Callable]] = {
            "issue_detected": [],
            "issue_resolved": [],
            "recovery_attempted": [],
        }

    def set_scenario(self, scenario: ScenarioType):
        """Update monitoring scenario and thresholds."""
        self.scenario = scenario
        self.thresholds = self.SCENARIO_THRESHOLDS[scenario].copy()
        logger.info(f"Monitoring scenario updated to: {scenario.value}")

    def set_custom_thresholds(self, thresholds: Dict[str, Any]):
        """Set custom monitoring thresholds."""
        self.thresholds.update(thresholds)
        self.scenario = ScenarioType.CUSTOM
        logger.info(f"Custom thresholds applied: {thresholds}")

    def register_callback(self, event: str, callback: Callable):
        """Register a callback for monitoring events."""
        if event in self.callbacks:
            self.callbacks[event].append(callback)
            logger.debug(f"Registered callback for event: {event}")

    def check_health(self) -> Dict[str, Any]:
        """
        Perform health check and detect issues.

        Returns:
            Health check results with detected issues
        """
        health_status = self.connection_manager.perform_health_check()
        active_conn = self.connection_manager.get_active_connection()

        if not active_conn:
            issue = Issue(
                IssueType.DISCONNECTION,
                "critical",
                "No active connection available",
                datetime.now(),
            )
            self._add_issue(issue)
            return {
                "status": "critical",
                "issues": [self._issue_to_dict(i) for i in self.active_issues],
                "health": health_status,
            }

        metrics = active_conn.metrics
        detected_issues = []

        # Check latency
        if metrics.get("latency_ms", 0) > self.thresholds["max_latency_ms"]:
            issue = Issue(
                IssueType.HIGH_LATENCY,
                (
                    "warning"
                    if metrics["latency_ms"] < self.thresholds["max_latency_ms"] * 1.5
                    else "critical"
                ),
                f"High latency: {metrics['latency_ms']:.1f}ms (threshold: {self.thresholds['max_latency_ms']}ms)",
                datetime.now(),
                metrics,
            )
            detected_issues.append(issue)

        # Check bandwidth
        if metrics.get("downlink_mbps", 0) < self.thresholds["min_downlink_mbps"]:
            issue = Issue(
                IssueType.LOW_BANDWIDTH,
                "warning",
                f"Low downlink: {metrics['downlink_mbps']:.1f} Mbps (threshold: {self.thresholds['min_downlink_mbps']} Mbps)",
                datetime.now(),
                metrics,
            )
            detected_issues.append(issue)

        # Check obstructions
        if metrics.get("obstructed", False):
            obstruction_pct = metrics.get("obstruction_percent", 0)
            if obstruction_pct > self.thresholds["max_obstruction_percent"]:
                issue = Issue(
                    IssueType.OBSTRUCTION,
                    (
                        "critical"
                        if obstruction_pct
                        > self.thresholds["max_obstruction_percent"] * 2
                        else "warning"
                    ),
                    f"Obstruction detected: {obstruction_pct*100:.1f}% (threshold: {self.thresholds['max_obstruction_percent']*100:.1f}%)",
                    datetime.now(),
                    metrics,
                )
                detected_issues.append(issue)

        # Check SNR
        if metrics.get("snr", 0) < self.thresholds["min_snr"]:
            issue = Issue(
                IssueType.SIGNAL_DEGRADATION,
                "warning",
                f"Low SNR: {metrics['snr']:.1f} dB (threshold: {self.thresholds['min_snr']} dB)",
                datetime.now(),
                metrics,
            )
            detected_issues.append(issue)

        # Process detected issues
        for issue in detected_issues:
            self._add_issue(issue)

        # Store performance data
        self.performance_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "connection": active_conn.name,
                "metrics": metrics.copy(),
                "issues": len(self.active_issues),
            }
        )

        return {
            "status": self._determine_overall_status(),
            "active_issues": [self._issue_to_dict(i) for i in self.active_issues],
            "resolved_issues_count": len(self.resolved_issues),
            "health": health_status,
            "metrics": metrics,
        }

    def _add_issue(self, issue: Issue):
        """Add or update an issue."""
        # Check if similar issue already exists
        existing = next(
            (
                i
                for i in self.active_issues
                if i.issue_type == issue.issue_type and not i.is_resolved()
            ),
            None,
        )

        if existing:
            existing.occurrence_count += 1
            existing.detected_at = datetime.now()
            logger.debug(
                f"Issue {issue.issue_type.value} occurred again (count: {existing.occurrence_count})"
            )

            # Trigger recovery if persistence threshold reached
            if (
                existing.occurrence_count >= self.issue_persistence_threshold
                and self.auto_recovery_enabled
            ):
                self._attempt_recovery(existing)
        else:
            self.active_issues.append(issue)
            logger.warning(f"New issue detected: {issue.description}")
            self._trigger_callbacks("issue_detected", issue)

    def _attempt_recovery(self, issue: Issue):
        """Attempt automatic recovery for an issue."""
        logger.info(
            f"Attempting recovery for persistent issue: {issue.issue_type.value}"
        )

        recovery_actions = {
            IssueType.HIGH_LATENCY: self._recover_high_latency,
            IssueType.LOW_BANDWIDTH: self._recover_low_bandwidth,
            IssueType.OBSTRUCTION: self._recover_obstruction,
            IssueType.DISCONNECTION: self._recover_disconnection,
            IssueType.SIGNAL_DEGRADATION: self._recover_signal_degradation,
        }

        recovery_func = recovery_actions.get(issue.issue_type)
        if recovery_func:
            success = recovery_func(issue)
            self._trigger_callbacks(
                "recovery_attempted", {"issue": issue, "success": success}
            )

            if success:
                issue.mark_resolved("automatic_recovery")
                self.resolved_issues.append(issue)
                self.active_issues.remove(issue)
                self._trigger_callbacks("issue_resolved", issue)

    def _recover_high_latency(self, issue: Issue) -> bool:
        """Attempt to recover from high latency."""
        # Try failover to better connection
        logger.info("Attempting failover to reduce latency")
        return self.connection_manager.check_and_failover()

    def _recover_low_bandwidth(self, issue: Issue) -> bool:
        """Attempt to recover from low bandwidth."""
        # Try connection recovery or failover
        logger.info("Attempting connection recovery for low bandwidth")
        return (
            self.connection_manager.auto_recover()
            or self.connection_manager.check_and_failover()
        )

    def _recover_obstruction(self, issue: Issue) -> bool:
        """Attempt to recover from obstruction."""
        # Can't automatically fix obstruction, but can try failover
        logger.warning("Obstruction detected - manual intervention may be required")
        return self.connection_manager.check_and_failover()

    def _recover_disconnection(self, issue: Issue) -> bool:
        """Attempt to recover from disconnection."""
        logger.info("Attempting to reestablish connection")
        return (
            self.connection_manager.auto_recover() or self.connection_manager.connect()
        )

    def _recover_signal_degradation(self, issue: Issue) -> bool:
        """Attempt to recover from signal degradation."""
        logger.info("Attempting recovery from signal degradation")
        return self.connection_manager.auto_recover()

    def _determine_overall_status(self) -> str:
        """Determine overall system status based on active issues."""
        if not self.active_issues:
            return "healthy"

        critical_count = sum(1 for i in self.active_issues if i.severity == "critical")
        if critical_count > 0:
            return "critical"

        warning_count = sum(1 for i in self.active_issues if i.severity == "warning")
        if warning_count > 2:
            return "degraded"

        return "warning"

    def _issue_to_dict(self, issue: Issue) -> Dict[str, Any]:
        """Convert issue to dictionary."""
        return {
            "type": issue.issue_type.value,
            "severity": issue.severity,
            "description": issue.description,
            "detected_at": issue.detected_at.isoformat(),
            "resolved_at": issue.resolved_at.isoformat() if issue.resolved_at else None,
            "occurrence_count": issue.occurrence_count,
            "metrics": issue.metrics,
        }

    def _trigger_callbacks(self, event: str, data: Any):
        """Trigger registered callbacks for an event."""
        for callback in self.callbacks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Error in callback for {event}: {e}")

    def get_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """
        Generate performance report for specified time period.

        Args:
            hours: Number of hours to include in report

        Returns:
            Performance report dictionary
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_history = [
            h
            for h in self.performance_history
            if datetime.fromisoformat(h["timestamp"]) > cutoff_time
        ]

        if not recent_history:
            return {"error": "No data available for specified period"}

        # Calculate statistics
        latencies = [h["metrics"].get("latency_ms", 0) for h in recent_history]
        downlinks = [h["metrics"].get("downlink_mbps", 0) for h in recent_history]
        uplinks = [h["metrics"].get("uplink_mbps", 0) for h in recent_history]

        report = {
            "period_hours": hours,
            "samples": len(recent_history),
            "latency_ms": {
                "avg": float(np.mean(latencies)),
                "min": float(np.min(latencies)),
                "max": float(np.max(latencies)),
                "p50": float(np.percentile(latencies, 50)),
                "p95": float(np.percentile(latencies, 95)),
            },
            "downlink_mbps": {
                "avg": float(np.mean(downlinks)),
                "min": float(np.min(downlinks)),
                "max": float(np.max(downlinks)),
            },
            "uplink_mbps": {
                "avg": float(np.mean(uplinks)),
                "min": float(np.min(uplinks)),
                "max": float(np.max(uplinks)),
            },
            "total_issues": len(self.resolved_issues) + len(self.active_issues),
            "resolved_issues": len(self.resolved_issues),
            "active_issues": len(self.active_issues),
        }

        return report

    def export_data(self, filepath: str, hours: int = 24):
        """
        Export performance data to file.

        Args:
            filepath: Path to export file
            hours: Number of hours of data to export
        """
        import json

        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_history = [
            h
            for h in self.performance_history
            if datetime.fromisoformat(h["timestamp"]) > cutoff_time
        ]

        export_data = {
            "exported_at": datetime.now().isoformat(),
            "period_hours": hours,
            "scenario": self.scenario.value,
            "thresholds": self.thresholds,
            "performance_history": recent_history,
            "active_issues": [self._issue_to_dict(i) for i in self.active_issues],
            "resolved_issues": [self._issue_to_dict(i) for i in self.resolved_issues],
        }

        with open(filepath, "w") as f:
            json.dump(export_data, f, indent=2)

        logger.info(f"Exported {len(recent_history)} samples to {filepath}")
