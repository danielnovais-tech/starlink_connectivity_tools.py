"""Tests for crisis monitor."""

import pytest
from starlink_connectivity_tools.satellite_connection_manager import (
    SatelliteConnectionManager,
    ConnectionType,
)
from starlink_connectivity_tools.crisis_monitor import (
    CrisisMonitor,
    ScenarioType,
    IssueType,
)


def test_crisis_monitor_init():
    """Test CrisisMonitor initialization."""
    manager = SatelliteConnectionManager()
    monitor = CrisisMonitor(manager, scenario=ScenarioType.NORMAL)

    assert monitor.scenario == ScenarioType.NORMAL
    assert monitor.thresholds is not None
    assert monitor.auto_recovery_enabled is True


def test_scenario_thresholds():
    """Test different scenario thresholds."""
    manager = SatelliteConnectionManager()

    normal = CrisisMonitor(manager, scenario=ScenarioType.NORMAL)
    assert normal.thresholds["max_latency_ms"] == 100

    disaster = CrisisMonitor(manager, scenario=ScenarioType.DISASTER)
    assert disaster.thresholds["max_latency_ms"] == 300


def test_set_scenario():
    """Test changing scenario."""
    manager = SatelliteConnectionManager()
    monitor = CrisisMonitor(manager, scenario=ScenarioType.NORMAL)

    monitor.set_scenario(ScenarioType.MEDICAL)
    assert monitor.scenario == ScenarioType.MEDICAL
    assert monitor.thresholds["max_latency_ms"] == 150


def test_set_custom_thresholds():
    """Test setting custom thresholds."""
    manager = SatelliteConnectionManager()
    monitor = CrisisMonitor(manager)

    custom = {"max_latency_ms": 250, "min_downlink_mbps": 15}
    monitor.set_custom_thresholds(custom)

    assert monitor.scenario == ScenarioType.CUSTOM
    assert monitor.thresholds["max_latency_ms"] == 250
    assert monitor.thresholds["min_downlink_mbps"] == 15


def test_check_health():
    """Test health check."""
    manager = SatelliteConnectionManager()
    manager.add_connection(
        "Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True
    )
    manager.connect()

    monitor = CrisisMonitor(manager, scenario=ScenarioType.NORMAL)
    health = monitor.check_health()

    assert health is not None
    assert "status" in health
    assert "active_issues" in health
    assert "health" in health


def test_performance_report():
    """Test performance report generation."""
    manager = SatelliteConnectionManager()
    manager.add_connection(
        "Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True
    )
    manager.connect()

    monitor = CrisisMonitor(manager)

    # Collect some data
    for _ in range(10):
        monitor.check_health()

    report = monitor.get_performance_report(hours=1)

    assert report is not None
    assert "samples" in report
    assert report["samples"] >= 10


def test_export_data(tmp_path):
    """Test data export."""
    manager = SatelliteConnectionManager()
    manager.add_connection(
        "Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True
    )
    manager.connect()

    monitor = CrisisMonitor(manager)
    monitor.check_health()

    export_file = tmp_path / "test_export.json"
    monitor.export_data(str(export_file), hours=1)

    assert export_file.exists()


def test_register_callback():
    """Test callback registration."""
    manager = SatelliteConnectionManager()
    monitor = CrisisMonitor(manager)

    called = []

    def callback(data):
        called.append(data)

    monitor.register_callback("issue_detected", callback)
    assert len(monitor.callbacks["issue_detected"]) == 1


def test_determine_overall_status():
    """Test overall status determination."""
    manager = SatelliteConnectionManager()
    monitor = CrisisMonitor(manager)

    # No issues - should be healthy
    status = monitor._determine_overall_status()
    assert status == "healthy"
