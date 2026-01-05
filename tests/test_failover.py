"""Unit tests for the FailoverHandler class."""

import unittest
import time
from unittest.mock import Mock, patch
from starlink_connectivity_tools import FailoverHandler
from starlink_connectivity_tools.failover import ConnectionState


class TestFailoverHandler(unittest.TestCase):
    """Test cases for FailoverHandler functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.handler = FailoverHandler(
            failure_threshold=3,
            check_interval=0.1  # Short interval for testing
        )
    
    def test_initialization(self):
        """Test FailoverHandler initialization."""
        self.assertEqual(self.handler.failure_threshold, 3)
        self.assertEqual(self.handler.check_interval, 0.1)
        self.assertEqual(self.handler.get_current_state(), ConnectionState.PRIMARY)
        self.assertEqual(self.handler.get_failure_count(), 0)
    
    def test_should_failover_with_healthy_connection(self):
        """Test should_failover returns False when connection is healthy."""
        # Mock health check to always return True (healthy)
        self.handler.health_check_callback = Mock(return_value=True)
        
        # Wait for check interval
        time.sleep(0.15)
        
        # Should not trigger failover when connection is healthy
        self.assertFalse(self.handler.should_failover())
        self.assertEqual(self.handler.get_failure_count(), 0)
    
    def test_should_failover_increments_failure_count(self):
        """Test failure count increments on unhealthy connection."""
        # Mock health check to always return False (unhealthy)
        self.handler.health_check_callback = Mock(return_value=False)
        
        # Check multiple times
        time.sleep(0.15)
        self.handler.should_failover()
        self.assertEqual(self.handler.get_failure_count(), 1)
        
        time.sleep(0.15)
        self.handler.should_failover()
        self.assertEqual(self.handler.get_failure_count(), 2)
    
    def test_should_failover_triggers_at_threshold(self):
        """Test failover triggers when failure threshold is reached."""
        # Mock health check to always return False
        self.handler.health_check_callback = Mock(return_value=False)
        
        # Trigger failures up to threshold
        for i in range(self.handler.failure_threshold):
            time.sleep(0.15)
            result = self.handler.should_failover()
            
            if i < self.handler.failure_threshold - 1:
                self.assertFalse(result)
            else:
                self.assertTrue(result)
    
    def test_initiate_failover_success(self):
        """Test successful failover initiation."""
        result = self.handler.initiate_failover("Primary connection lost")
        
        self.assertTrue(result)
        self.assertEqual(self.handler.get_current_state(), ConnectionState.BACKUP)
        self.assertEqual(self.handler.get_failure_count(), 0)  # Reset after failover
    
    def test_initiate_failover_already_on_backup(self):
        """Test failover when already on backup connection."""
        # First failover
        self.handler.initiate_failover("Primary failed")
        
        # Second failover attempt should fail
        result = self.handler.initiate_failover("Attempting again")
        
        self.assertFalse(result)
        self.assertEqual(self.handler.get_current_state(), ConnectionState.BACKUP)
    
    def test_failover_history_recording(self):
        """Test that failover events are recorded in history."""
        reason = "Test failover"
        self.handler.initiate_failover(reason)
        
        history = self.handler.get_failover_history()
        
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['reason'], reason)
        self.assertEqual(history[0]['from_state'], 'primary')
        self.assertEqual(history[0]['to_state'], 'backup')
        self.assertIn('timestamp', history[0])
    
    def test_reset_handler(self):
        """Test resetting the handler to initial state."""
        # Cause some failures
        self.handler.health_check_callback = Mock(return_value=False)
        time.sleep(0.15)
        self.handler.should_failover()
        
        # Perform failover
        self.handler.initiate_failover("Test")
        
        # Reset
        self.handler.reset()
        
        self.assertEqual(self.handler.get_current_state(), ConnectionState.PRIMARY)
        self.assertEqual(self.handler.get_failure_count(), 0)
    
    def test_health_check_callback_exception_handling(self):
        """Test that exceptions in health check callback are handled."""
        # Mock health check to raise an exception
        self.handler.health_check_callback = Mock(side_effect=Exception("Network error"))
        
        time.sleep(0.15)
        result = self.handler.should_failover()
        
        # Should treat exception as failure
        self.assertEqual(self.handler.get_failure_count(), 1)
    
    def test_check_interval_respected(self):
        """Test that check interval is respected."""
        self.handler.health_check_callback = Mock(return_value=False)
        
        # First check should work
        time.sleep(0.15)
        self.handler.should_failover()
        first_count = self.handler.get_failure_count()
        
        # Immediate second check should be skipped
        result = self.handler.should_failover()
        self.assertFalse(result)
        self.assertEqual(self.handler.get_failure_count(), first_count)
        
        # After waiting, check should work again
        time.sleep(0.15)
        self.handler.should_failover()
        self.assertEqual(self.handler.get_failure_count(), first_count + 1)
    
    def test_failure_count_resets_on_recovery(self):
        """Test that failure count resets when connection recovers."""
        # Simulate failures
        self.handler.health_check_callback = Mock(return_value=False)
        time.sleep(0.15)
        self.handler.should_failover()
        time.sleep(0.15)
        self.handler.should_failover()
        
        self.assertEqual(self.handler.get_failure_count(), 2)
        
        # Simulate recovery
        self.handler.health_check_callback = Mock(return_value=True)
        time.sleep(0.15)
        self.handler.should_failover()
        
        # Failure count should be reset
        self.assertEqual(self.handler.get_failure_count(), 0)


class TestConnectionState(unittest.TestCase):
    """Test cases for ConnectionState enum."""
    
    def test_connection_state_values(self):
        """Test ConnectionState enum values."""
        self.assertEqual(ConnectionState.PRIMARY.value, "primary")
        self.assertEqual(ConnectionState.BACKUP.value, "backup")
        self.assertEqual(ConnectionState.FAILED.value, "failed")


if __name__ == "__main__":
    unittest.main()
