"""Tests for Starlink API integration."""

import pytest
from starlink_connectivity_tools.starlink_api import StarlinkAPI


def test_starlink_api_init():
    """Test StarlinkAPI initialization."""
    api = StarlinkAPI(simulation_mode=True)
    assert api.simulation_mode is True
    assert api.target == "192.168.100.1:9200"


def test_get_status_simulation():
    """Test getting status in simulation mode."""
    api = StarlinkAPI(simulation_mode=True)
    status = api.get_status()
    
    assert status is not None
    assert "uptime" in status
    assert "state" in status
    assert "ping_latency_ms" in status
    assert "downlink_throughput_bps" in status
    assert "uplink_throughput_bps" in status
    assert status["state"] == "CONNECTED"


def test_get_obstruction_map_simulation():
    """Test getting obstruction map in simulation mode."""
    api = StarlinkAPI(simulation_mode=True)
    obs_map = api.get_obstruction_map()
    
    assert obs_map is not None
    assert "obstructed" in obs_map
    assert "fraction_obstructed" in obs_map
    assert obs_map["fraction_obstructed"] < 1.0


def test_reboot_simulation():
    """Test reboot command in simulation mode."""
    api = StarlinkAPI(simulation_mode=True)
    result = api.reboot()
    assert result is True


def test_stow_unstow_simulation():
    """Test stow/unstow commands in simulation mode."""
    api = StarlinkAPI(simulation_mode=True)
    
    assert api.stow() is True
    assert api.unstow() is True


def test_get_history_simulation():
    """Test getting history in simulation mode."""
    api = StarlinkAPI(simulation_mode=True)
    history = api.get_history(samples=100)
    
    assert history is not None
    assert "pop_ping_latency_ms" in history
    assert "downlink_throughput_bps" in history
    assert len(history["pop_ping_latency_ms"]) == 100


def test_parse_state():
    """Test state parsing."""
    api = StarlinkAPI(simulation_mode=True)
    
    assert api._parse_state(0) == "UNKNOWN"
    assert api._parse_state(1) == "BOOTING"
    assert api._parse_state(2) == "STOWED"
    assert api._parse_state(3) == "SEARCHING"
    assert api._parse_state(4) == "CONNECTED"


def test_parse_alerts():
    """Test alert parsing."""
    api = StarlinkAPI(simulation_mode=True)
    
    alerts = api._parse_alerts(1)
    assert "MOTORS_STUCK" in alerts
    
    alerts = api._parse_alerts(2)
    assert "THERMAL_THROTTLE" in alerts
    
    alerts = api._parse_alerts(3)
    assert "MOTORS_STUCK" in alerts
    assert "THERMAL_THROTTLE" in alerts


def test_close():
    """Test closing API connection."""
    api = StarlinkAPI(simulation_mode=True)
    api.close()  # Should not raise an error
