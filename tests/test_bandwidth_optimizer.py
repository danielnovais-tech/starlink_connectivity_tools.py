"""
Tests for BandwidthOptimizer module.
"""

import unittest
from src.bandwidth_optimizer import BandwidthOptimizer


class TestBandwidthOptimizer(unittest.TestCase):
    """Test cases for BandwidthOptimizer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = BandwidthOptimizer()

    def test_initialization(self):
        """Test BandwidthOptimizer initialization."""
        self.assertIsNotNone(self.optimizer)
        self.assertIsNone(self.optimizer.max_bandwidth)
        self.assertEqual(self.optimizer.current_usage, 0)
        self.assertFalse(self.optimizer.optimization_enabled)

    def test_initialization_with_bandwidth(self):
        """Test initialization with max bandwidth."""
        optimizer = BandwidthOptimizer(max_bandwidth=100)
        self.assertEqual(optimizer.max_bandwidth, 100)

    def test_enable_optimization(self):
        """Test enabling optimization."""
        result = self.optimizer.enable_optimization()
        self.assertTrue(result)
        self.assertTrue(self.optimizer.optimization_enabled)

    def test_disable_optimization(self):
        """Test disabling optimization."""
        self.optimizer.enable_optimization()
        result = self.optimizer.disable_optimization()
        self.assertTrue(result)
        self.assertFalse(self.optimizer.optimization_enabled)

    def test_set_bandwidth_limit(self):
        """Test setting bandwidth limit."""
        result = self.optimizer.set_bandwidth_limit(50)
        self.assertTrue(result)
        self.assertEqual(self.optimizer.max_bandwidth, 50)

    def test_get_current_usage(self):
        """Test getting current usage."""
        usage = self.optimizer.get_current_usage()
        self.assertIsInstance(usage, dict)
        self.assertIn("current_usage", usage)
        self.assertIn("max_bandwidth", usage)
        self.assertIn("optimization_enabled", usage)

    def test_optimize_when_disabled(self):
        """Test optimization when disabled."""
        result = self.optimizer.optimize()
        self.assertEqual(result["status"], "optimization_disabled")

    def test_optimize_when_enabled(self):
        """Test optimization when enabled."""
        self.optimizer.enable_optimization()
        result = self.optimizer.optimize()
        self.assertEqual(result["status"], "optimized")
        self.assertIn("savings", result)


if __name__ == "__main__":
    unittest.main()
