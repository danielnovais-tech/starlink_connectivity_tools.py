"""
Tests for ConnectionManager module.
"""

import unittest
from src.connection_manager import ConnectionManager


class TestConnectionManager(unittest.TestCase):
    """Test cases for ConnectionManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = ConnectionManager()

    def test_initialization(self):
        """Test ConnectionManager initialization."""
        self.assertIsNotNone(self.manager)
        self.assertFalse(self.manager.connected)
        self.assertEqual(self.manager.connection_status, "disconnected")

    def test_initialization_with_config(self):
        """Test ConnectionManager initialization with config."""
        config = {"timeout": 30}
        manager = ConnectionManager(config=config)
        self.assertEqual(manager.config, config)

    def test_connect(self):
        """Test connection establishment."""
        result = self.manager.connect()
        self.assertTrue(result)
        self.assertTrue(self.manager.connected)
        self.assertEqual(self.manager.connection_status, "connected")

    def test_disconnect(self):
        """Test disconnection."""
        self.manager.connect()
        result = self.manager.disconnect()
        self.assertTrue(result)
        self.assertFalse(self.manager.connected)
        self.assertEqual(self.manager.connection_status, "disconnected")

    def test_get_status(self):
        """Test getting connection status."""
        status = self.manager.get_status()
        self.assertIsInstance(status, dict)
        self.assertIn("connected", status)
        self.assertIn("status", status)
        self.assertFalse(status["connected"])

    def test_get_status_when_connected(self):
        """Test getting status when connected."""
        self.manager.connect()
        status = self.manager.get_status()
        self.assertTrue(status["connected"])
        self.assertEqual(status["status"], "connected")

    def test_reconnect(self):
        """Test reconnection."""
        self.manager.connect()
        result = self.manager.reconnect()
        self.assertTrue(result)
        self.assertTrue(self.manager.connected)
        self.assertEqual(self.manager.connection_status, "connected")


if __name__ == "__main__":
    unittest.main()
