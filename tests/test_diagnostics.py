"""Tests for diagnostics engine."""

import pytest
from starlink_connectivity_tools.satellite_connection_manager import (
    SatelliteConnectionManager,
    ConnectionType,
)
from starlink_connectivity_tools.diagnostics import DiagnosticsEngine


def test_diagnostics_init():
    """Test DiagnosticsEngine initialization."""
    manager = SatelliteConnectionManager()
    diagnostics = DiagnosticsEngine(manager)
    
    assert diagnostics.connection_manager is manager
    assert diagnostics.alerts == []
    assert len(diagnostics.telemetry_history) == 0


def test_run_full_diagnostic():
    """Test running full diagnostic."""
    manager = SatelliteConnectionManager()
    manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    manager.connect()
    
    diagnostics = DiagnosticsEngine(manager)
    report = diagnostics.run_full_diagnostic()
    
    assert report is not None
    assert "status" in report
    assert "connection" in report
    assert "telemetry" in report
    assert "alerts" in report


def test_collect_telemetry():
    """Test telemetry collection."""
    manager = SatelliteConnectionManager()
    conn = manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    manager.connect()
    
    diagnostics = DiagnosticsEngine(manager)
    telemetry = diagnostics._collect_telemetry(conn)
    
    assert telemetry is not None
    assert "timestamp" in telemetry
    assert "connection_name" in telemetry
    assert "metrics" in telemetry


def test_acknowledge_alert():
    """Test acknowledging alerts."""
    manager = SatelliteConnectionManager()
    diagnostics = DiagnosticsEngine(manager)
    
    from starlink_connectivity_tools.diagnostics import Alert
    alert = Alert("test", "warning", "Test alert", "Test recommendation")
    diagnostics.alerts.append(alert)
    
    result = diagnostics.acknowledge_alert(0)
    assert result is True
    assert diagnostics.alerts[0].acknowledged is True


def test_clear_acknowledged_alerts():
    """Test clearing acknowledged alerts."""
    manager = SatelliteConnectionManager()
    diagnostics = DiagnosticsEngine(manager)
    
    from starlink_connectivity_tools.diagnostics import Alert
    alert1 = Alert("test1", "warning", "Test 1", "Recommendation 1")
    alert2 = Alert("test2", "warning", "Test 2", "Recommendation 2")
    
    alert1.acknowledged = True
    diagnostics.alerts.extend([alert1, alert2])
    
    diagnostics.clear_acknowledged_alerts()
    assert len(diagnostics.alerts) == 1
    assert diagnostics.alerts[0] == alert2


def test_get_historical_performance():
    """Test getting historical performance."""
    manager = SatelliteConnectionManager()
    manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    manager.connect()
    
    diagnostics = DiagnosticsEngine(manager)
    
    # Collect some telemetry
    for _ in range(10):
        diagnostics.run_full_diagnostic()
    
    history = diagnostics.get_historical_performance(hours=1)
    
    assert history is not None
    assert "samples" in history
    assert history["samples"] >= 10


def test_generate_diagnostic_report(tmp_path):
    """Test generating diagnostic report."""
    manager = SatelliteConnectionManager()
    manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    manager.connect()
    
    diagnostics = DiagnosticsEngine(manager)
    diagnostics.run_full_diagnostic()
    
    report_file = tmp_path / "test_report.json"
    diagnostics.generate_diagnostic_report(str(report_file))
    
    assert report_file.exists()


def test_establish_baseline():
    """Test establishing performance baseline."""
    manager = SatelliteConnectionManager()
    manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    manager.connect()
    
    diagnostics = DiagnosticsEngine(manager)
    
    # Collect enough data for baseline
    for _ in range(15):
        diagnostics.run_full_diagnostic()
    
    # Baseline should be established
    diagnostics._establish_baseline()
    
    assert len(diagnostics.performance_baseline) > 0
    assert "downlink_mbps" in diagnostics.performance_baseline
