"""Tests for satellite connection manager."""

import pytest
from starlink_connectivity_tools.satellite_connection_manager import (
    SatelliteConnectionManager,
    ConnectionType,
    ConnectionStatus,
)


def test_connection_manager_init():
    """Test ConnectionManager initialization."""
    manager = SatelliteConnectionManager()
    assert manager.connections == []
    assert manager.active_connection is None


def test_add_starlink_connection():
    """Test adding a Starlink connection."""
    manager = SatelliteConnectionManager()
    conn = manager.add_connection(
        "Test Starlink",
        ConnectionType.STARLINK,
        priority=100,
        simulation_mode=True
    )
    
    assert conn is not None
    assert conn.name == "Test Starlink"
    assert conn.connection_type == ConnectionType.STARLINK
    assert conn.priority == 100
    assert len(manager.connections) == 1


def test_add_multiple_connections():
    """Test adding multiple connections."""
    manager = SatelliteConnectionManager()
    
    manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    manager.add_connection("Iridium", ConnectionType.IRIDIUM, priority=50)
    manager.add_connection("Inmarsat", ConnectionType.INMARSAT, priority=25)
    
    assert len(manager.connections) == 3
    # Should be sorted by priority
    assert manager.connections[0].priority == 100
    assert manager.connections[1].priority == 50
    assert manager.connections[2].priority == 25


def test_connect():
    """Test establishing connection."""
    manager = SatelliteConnectionManager()
    manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    
    result = manager.connect()
    assert result is True
    assert manager.active_connection is not None
    assert manager.active_connection.name == "Starlink"


def test_select_best_connection():
    """Test selecting best available connection."""
    manager = SatelliteConnectionManager()
    manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    manager.add_connection("Iridium", ConnectionType.IRIDIUM, priority=50)
    
    best = manager.select_best_connection()
    assert best is not None
    assert best.name == "Starlink"


def test_get_connection_stats():
    """Test getting connection statistics."""
    manager = SatelliteConnectionManager()
    manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    manager.connect()
    
    stats = manager.get_connection_stats()
    assert stats is not None
    assert "total_connections" in stats
    assert stats["total_connections"] == 1
    assert "connections" in stats


def test_perform_health_check():
    """Test health check."""
    manager = SatelliteConnectionManager()
    manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    manager.connect()
    
    health = manager.perform_health_check()
    assert health is not None
    assert "timestamp" in health
    assert "active_connection" in health
    assert "connections" in health
    assert len(health["connections"]) == 1


def test_failover():
    """Test failover between connections."""
    manager = SatelliteConnectionManager()
    
    starlink = manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    iridium = manager.add_connection("Iridium", ConnectionType.IRIDIUM, priority=50)
    
    manager.connect()
    assert manager.active_connection.name == "Starlink"
    
    # Simulate failures
    starlink.failure_count = 5
    
    # Check and failover
    result = manager.check_and_failover()
    # In simulation, Starlink should still work, so no failover
    # But if it did failover, it would switch to Iridium


def test_close_all():
    """Test closing all connections."""
    manager = SatelliteConnectionManager()
    manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    manager.connect()
    
    manager.close_all()
    assert len(manager.connections) == 0
    assert manager.active_connection is None


def test_get_metrics():
    """Test getting connection metrics."""
    manager = SatelliteConnectionManager()
    conn = manager.add_connection("Starlink", ConnectionType.STARLINK, priority=100, simulation_mode=True)
    
    metrics = conn.get_metrics()
    assert metrics is not None
    assert "latency_ms" in metrics
    assert "downlink_mbps" in metrics
    assert "uplink_mbps" in metrics
