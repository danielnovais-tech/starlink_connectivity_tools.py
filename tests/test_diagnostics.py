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
    manager.add_connection(
        "Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True
    )
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
    conn = manager.add_connection(
        "Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True
    )
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
    manager.add_connection(
        "Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True
    )
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
    manager.add_connection(
        "Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True
    )
    manager.connect()

    diagnostics = DiagnosticsEngine(manager)
    diagnostics.run_full_diagnostic()

    report_file = tmp_path / "test_report.json"
    diagnostics.generate_diagnostic_report(str(report_file))

    assert report_file.exists()


def test_establish_baseline():
    """Test establishing performance baseline."""
    manager = SatelliteConnectionManager()
    manager.add_connection(
        "Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True
    )
    manager.connect()

    diagnostics = DiagnosticsEngine(manager)

    # Collect enough data for baseline
    for _ in range(15):
        diagnostics.run_full_diagnostic()

    # Baseline should be established
    diagnostics._establish_baseline()

    assert len(diagnostics.performance_baseline) > 0
    assert "downlink_mbps" in diagnostics.performance_baseline
    def test_diagnostics_init():
        """Test Diagnostics initialization."""
        diagnostics = Diagnostics()
        assert diagnostics.starlink_endpoint == "192.168.100.1"
        assert diagnostics.diagnostic_history == []


    def test_diagnostics_custom_endpoint():
        """Test Diagnostics initialization with custom endpoint."""
        diagnostics = Diagnostics(starlink_endpoint="10.0.0.1")
        assert diagnostics.starlink_endpoint == "10.0.0.1"


    def test_run_full_diagnostic():
        """Test running full diagnostic."""
        diagnostics = Diagnostics()
        result = diagnostics.run_full_diagnostic()
        
        assert "timestamp" in result
        assert "connectivity" in result
        assert "starlink_status" in result
        assert "network_performance" in result
        assert "hardware_status" in result
        assert "overall_health" in result
        assert len(diagnostics.diagnostic_history) == 1


    def test_check_connectivity():
        """Test connectivity check."""
        diagnostics = Diagnostics()
        result = diagnostics.check_connectivity()
        
        assert "router_reachable" in result
        assert "internet_accessible" in result
        assert "dns_working" in result
        assert "timestamp" in result


    def test_check_starlink_status():
        """Test Starlink status check."""
        diagnostics = Diagnostics()
        result = diagnostics.check_starlink_status()
        
        assert "dish_connected" in result
        assert "satellites_visible" in result
        assert "signal_quality" in result
        assert "downlink_throughput_mbps" in result
        assert "uplink_throughput_mbps" in result


    def test_check_network_performance():
        """Test network performance check."""
        diagnostics = Diagnostics()
        result = diagnostics.check_network_performance()
        
        assert "latency_ms" in result
        assert "jitter_ms" in result
        assert "packet_loss_percent" in result
        assert "download_speed_mbps" in result
        assert "upload_speed_mbps" in result


    def test_check_hardware_status():
        """Test hardware status check."""
        diagnostics = Diagnostics()
        result = diagnostics.check_hardware_status()
        
        assert "dish_temperature" in result
        assert "dish_motors" in result
        assert "power_supply" in result


    def test_get_obstruction_map():
        """Test obstruction map retrieval."""
        diagnostics = Diagnostics()
        result = diagnostics.get_obstruction_map()
        
        assert "has_obstructions" in result
        assert "obstruction_percentage" in result
        assert "recommended_action" in result


    def test_test_speed():
        """Test speed test."""
        diagnostics = Diagnostics()
        result = diagnostics.test_speed()
        
        assert "download_mbps" in result
        assert "upload_mbps" in result
        assert "latency_ms" in result
        assert "server" in result


    def test_get_diagnostic_report():
        """Test diagnostic report generation."""
        diagnostics = Diagnostics()
        report = diagnostics.get_diagnostic_report()
        
        assert isinstance(report, str)
        assert "Starlink Connectivity Diagnostic Report" in report
        assert "Overall Health" in report


    def test_get_troubleshooting_steps():
        """Test troubleshooting steps generation."""
        diagnostics = Diagnostics()
        steps = diagnostics.get_troubleshooting_steps()
        
        assert isinstance(steps, list)
        assert len(steps) > 0


    def test_connectivity_diagnostics_init():
        """Test ConnectivityDiagnostics initialization."""
        diag = ConnectivityDiagnostics()
        assert diag.diagnostic_history == []
        assert diag.max_history == 100


    def test_connectivity_diagnostics_run_full():
        """Test ConnectivityDiagnostics full diagnostic run."""
        diag = ConnectivityDiagnostics()
        result = diag.run_full_diagnostic()
        
        assert "timestamp" in result
        assert "tests" in result
        assert "summary" in result
        assert len(diag.diagnostic_history) == 1


    def test_connectivity_diagnostics_get_history():
        """Test getting diagnostic history."""
        diag = ConnectivityDiagnostics()
        
        for _ in range(5):
            diag.run_full_diagnostic()
        
        history = diag.get_diagnostic_history(limit=3)
        assert len(history) == 3


    def test_connectivity_diagnostics_history_limit():
        """Test diagnostic history limit enforcement."""
        diag = ConnectivityDiagnostics()
        
        for _ in range(110):
            diag.run_full_diagnostic()
        
        assert len(diag.diagnostic_history) <= diag.max_history


    def test_connectivity_diagnostics_get_historical():
        """Test getting historical diagnostics."""
        diag = ConnectivityDiagnostics()
        diag.run_full_diagnostic()
        
        history = diag.get_historical_diagnostics(hours=24)
        assert isinstance(history, list)


    def test_connectivity_diagnostics_health_report():
        """Test health report generation."""
        diag = ConnectivityDiagnostics()
        diag.run_full_diagnostic()
        
        report = diag.generate_health_report()
        
        assert "current_status" in report
        assert "health_over_last_24h" in report
        assert "common_issues" in report
        assert "timestamp" in report


    def test_starlink_diagnostics_init():
        """Test StarlinkDiagnostics initialization."""
        diag = StarlinkDiagnostics()
        assert diag.logs == []
        assert diag.alerts == []
        assert diag.test_results == []
        assert diag.health_status == "unknown"


    def test_starlink_diagnostics_health_check():
        """Test health check."""
        diag = StarlinkDiagnostics()
        result = diag.run_health_check()
        
        assert "status" in result
        assert "tests_passed" in result
        assert "tests_failed" in result
        assert diag.health_status == result["status"]


    def test_starlink_diagnostics_connectivity_test():
        """Test connectivity test."""
        diag = StarlinkDiagnostics()
        result = diag.test_connectivity()
        
        assert result["test"] == "connectivity"
        assert "status" in result
        assert "latency" in result
        assert len(diag.test_results) == 1


    def test_starlink_diagnostics_bandwidth_test():
        """Test bandwidth test."""
        diag = StarlinkDiagnostics()
        result = diag.test_bandwidth()
        
        assert result["test"] == "bandwidth"
        assert "download_speed" in result
        assert "upload_speed" in result


    def test_starlink_diagnostics_signal_strength():
        """Test signal strength retrieval."""
        diag = StarlinkDiagnostics()
        result = diag.get_signal_strength()
        
        assert "signal_strength" in result
        assert "quality" in result
        assert "satellites_visible" in result


    def test_starlink_diagnostics_log_event():
        """Test event logging."""
        diag = StarlinkDiagnostics()
        event = {"type": "test", "message": "Test event"}
        
        diag.log_event(event)
        assert len(diag.logs) == 1
        assert diag.logs[0] == event


    def test_starlink_diagnostics_test_history():
        """Test test history retrieval."""
        diag = StarlinkDiagnostics()
        diag.test_connectivity()
        diag.test_bandwidth()
        
        history = diag.get_test_history()
        assert len(history) == 2


    def test_starlink_diagnostics_clear_history():
        """Test clearing test history."""
        diag = StarlinkDiagnostics()
        diag.test_connectivity()
        
        result = diag.clear_test_history()
        assert result is True
        assert len(diag.test_results) == 0


    def test_starlink_diagnostics_system_info():
        """Test system info retrieval."""
        diag = StarlinkDiagnostics()
        diag.test_connectivity()
        
        info = diag.get_system_info()
        
        assert "health_status" in info
        assert "total_tests_run" in info
        assert info["total_tests_run"] == 1