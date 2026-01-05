"""
Tests for the StarlinkConnectivity class.
"""
import pytest
from starlink_connectivity_tools.connectivity import StarlinkConnectivity


class TestStarlinkConnectivity:
    """Test cases for StarlinkConnectivity class."""

    def test_init_without_dish_id(self):
        """Test initialization without dish_id."""
        conn = StarlinkConnectivity()
        assert conn.dish_id is None
        assert not conn.is_connected()

    def test_init_with_dish_id(self):
        """Test initialization with dish_id."""
        dish_id = "DISH-12345"
        conn = StarlinkConnectivity(dish_id=dish_id)
        assert conn.dish_id == dish_id
        assert not conn.is_connected()

    def test_connect_without_dish_id(self):
        """Test connect fails without dish_id."""
        conn = StarlinkConnectivity()
        result = conn.connect()
        assert result is False
        assert not conn.is_connected()

    def test_connect_with_dish_id(self):
        """Test connect succeeds with dish_id."""
        conn = StarlinkConnectivity(dish_id="DISH-12345")
        result = conn.connect()
        assert result is True
        assert conn.is_connected()

    def test_disconnect(self):
        """Test disconnect functionality."""
        conn = StarlinkConnectivity(dish_id="DISH-12345")
        conn.connect()
        assert conn.is_connected()
        
        result = conn.disconnect()
        assert result is True
        assert not conn.is_connected()

    def test_get_status_not_connected(self):
        """Test get_status when not connected."""
        conn = StarlinkConnectivity(dish_id="DISH-12345")
        status = conn.get_status()
        
        assert status["dish_id"] == "DISH-12345"
        assert status["connected"] is False

    def test_get_status_connected(self):
        """Test get_status when connected."""
        conn = StarlinkConnectivity(dish_id="DISH-12345")
        conn.connect()
        status = conn.get_status()
        
        assert status["dish_id"] == "DISH-12345"
        assert status["connected"] is True
