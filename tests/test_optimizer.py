"""
Unit tests for the Starlink Connectivity Tools library.

Tests cover bandwidth allocation, optimization, and use cases including
medical emergency communications.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from starlink_connectivity import BandwidthOptimizer
from starlink_connectivity.optimizer import BandwidthAllocation


class TestBandwidthOptimizer(unittest.TestCase):
    """Test cases for BandwidthOptimizer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = BandwidthOptimizer(total_bandwidth=100.0)

    def test_initialization(self):
        """Test optimizer initialization."""
        self.assertEqual(self.optimizer.total_bandwidth, 100.0)
        self.assertEqual(self.optimizer.available_bandwidth, 100.0)
        self.assertEqual(len(self.optimizer.allocations), 0)

    def test_allocate_bandwidth_basic(self):
        """Test basic bandwidth allocation."""
        allocation = self.optimizer.allocate_bandwidth(
            connection_id="test_conn", destination="test.dest", requested_bandwidth=10.0
        )

        self.assertIsInstance(allocation, BandwidthAllocation)
        self.assertEqual(allocation.connection_id, "test_conn")
        self.assertEqual(allocation.destination, "test.dest")
        self.assertEqual(allocation.requested_bandwidth, 10.0)
        self.assertEqual(allocation.allocated_bandwidth, 10.0)
        self.assertEqual(allocation.status, "allocated")
        self.assertEqual(self.optimizer.available_bandwidth, 90.0)

    def test_medical_emergency_allocation(self):
        """Test medical emergency use case allocation."""
        # Prioritize medical data transmission
        allocation = self.optimizer.allocate_bandwidth(
            connection_id="medical_evac",
            destination="medical.data",
            requested_bandwidth=10.0,
        )

        self.assertEqual(allocation.connection_id, "medical_evac")
        self.assertEqual(allocation.destination, "medical.data")
        self.assertEqual(allocation.requested_bandwidth, 10.0)
        self.assertEqual(allocation.allocated_bandwidth, 10.0)
        self.assertEqual(allocation.status, "allocated")

    def test_multiple_allocations(self):
        """Test multiple bandwidth allocations."""
        alloc1 = self.optimizer.allocate_bandwidth("conn1", "dest1", 20.0)
        alloc2 = self.optimizer.allocate_bandwidth("conn2", "dest2", 30.0)
        alloc3 = self.optimizer.allocate_bandwidth("conn3", "dest3", 15.0)

        self.assertEqual(alloc1.allocated_bandwidth, 20.0)
        self.assertEqual(alloc2.allocated_bandwidth, 30.0)
        self.assertEqual(alloc3.allocated_bandwidth, 15.0)
        self.assertEqual(self.optimizer.available_bandwidth, 35.0)
        self.assertEqual(len(self.optimizer.allocations), 3)

    def test_insufficient_bandwidth(self):
        """Test allocation when insufficient bandwidth available."""
        # Allocate most of the bandwidth
        self.optimizer.allocate_bandwidth("conn1", "dest1", 95.0)

        # Try to allocate more than available
        allocation = self.optimizer.allocate_bandwidth("conn2", "dest2", 20.0)

        self.assertEqual(allocation.allocated_bandwidth, 5.0)  # Only 5 Mbps left
        self.assertEqual(allocation.status, "partial")
        self.assertEqual(self.optimizer.available_bandwidth, 0)

    def test_no_bandwidth_available(self):
        """Test allocation when no bandwidth available."""
        # Use all bandwidth
        self.optimizer.allocate_bandwidth("conn1", "dest1", 100.0)

        # Try to allocate when none available
        allocation = self.optimizer.allocate_bandwidth("conn2", "dest2", 10.0)

        self.assertEqual(allocation.allocated_bandwidth, 0)
        self.assertEqual(allocation.status, "queued")

    def test_release_bandwidth(self):
        """Test releasing bandwidth allocation."""
        self.optimizer.allocate_bandwidth("conn1", "dest1", 30.0)
        self.assertEqual(self.optimizer.available_bandwidth, 70.0)

        result = self.optimizer.release_bandwidth("conn1")

        self.assertTrue(result)
        self.assertEqual(self.optimizer.available_bandwidth, 100.0)
        self.assertEqual(len(self.optimizer.allocations), 0)

    def test_release_nonexistent_connection(self):
        """Test releasing a connection that doesn't exist."""
        result = self.optimizer.release_bandwidth("nonexistent")
        self.assertFalse(result)

    def test_get_allocation(self):
        """Test retrieving allocation details."""
        original = self.optimizer.allocate_bandwidth("conn1", "dest1", 25.0)
        retrieved = self.optimizer.get_allocation("conn1")

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.connection_id, original.connection_id)
        self.assertEqual(retrieved.allocated_bandwidth, original.allocated_bandwidth)

    def test_get_nonexistent_allocation(self):
        """Test retrieving allocation that doesn't exist."""
        allocation = self.optimizer.get_allocation("nonexistent")
        self.assertIsNone(allocation)

    def test_get_all_allocations(self):
        """Test retrieving all allocations."""
        self.optimizer.allocate_bandwidth("conn1", "dest1", 10.0)
        self.optimizer.allocate_bandwidth("conn2", "dest2", 20.0)
        self.optimizer.allocate_bandwidth("conn3", "dest3", 15.0)

        all_allocations = self.optimizer.get_all_allocations()

        self.assertEqual(len(all_allocations), 3)
        self.assertIn("conn1", all_allocations)
        self.assertIn("conn2", all_allocations)
        self.assertIn("conn3", all_allocations)

    def test_update_existing_allocation(self):
        """Test updating an existing allocation."""
        # Create initial allocation
        self.optimizer.allocate_bandwidth("conn1", "dest1", 20.0)
        self.assertEqual(self.optimizer.available_bandwidth, 80.0)

        # Update the same connection with different bandwidth
        updated = self.optimizer.allocate_bandwidth("conn1", "dest1", 30.0)

        self.assertEqual(updated.allocated_bandwidth, 30.0)
        self.assertEqual(self.optimizer.available_bandwidth, 70.0)
        self.assertEqual(
            len(self.optimizer.allocations), 1
        )  # Still only one allocation

    def test_allocation_with_priority(self):
        """Test allocation with priority setting."""
        allocation = self.optimizer.allocate_bandwidth(
            connection_id="high_priority",
            destination="critical.dest",
            requested_bandwidth=15.0,
            priority=10,
        )

        self.assertEqual(allocation.priority, 10)

    def test_get_available_bandwidth(self):
        """Test getting available bandwidth."""
        self.assertEqual(self.optimizer.get_available_bandwidth(), 100.0)

        self.optimizer.allocate_bandwidth("conn1", "dest1", 40.0)
        self.assertEqual(self.optimizer.get_available_bandwidth(), 60.0)

    def test_medical_emergency_scenario(self):
        """Test complete medical emergency scenario."""
        # Medical evacuation
        medical = self.optimizer.allocate_bandwidth(
            connection_id="medical_evac",
            destination="medical.data",
            requested_bandwidth=10.0,
        )

        # Telemedicine consultation
        telemedicine = self.optimizer.allocate_bandwidth(
            connection_id="telemedicine",
            destination="hospital.video",
            requested_bandwidth=5.0,
            priority=5,
        )

        # Patient monitoring
        monitoring = self.optimizer.allocate_bandwidth(
            connection_id="monitoring",
            destination="vitals.stream",
            requested_bandwidth=2.0,
            priority=5,
        )

        # Verify all allocations
        self.assertEqual(medical.allocated_bandwidth, 10.0)
        self.assertEqual(telemedicine.allocated_bandwidth, 5.0)
        self.assertEqual(monitoring.allocated_bandwidth, 2.0)

        # Verify total allocation
        total_allocated = sum(
            a.allocated_bandwidth for a in self.optimizer.get_all_allocations().values()
        )
        self.assertEqual(total_allocated, 17.0)

        # Release medical evacuation
        self.optimizer.release_bandwidth("medical_evac")
        self.assertEqual(len(self.optimizer.allocations), 2)


class TestBandwidthAllocation(unittest.TestCase):
    """Test cases for BandwidthAllocation class."""

    def test_allocation_creation(self):
        """Test creating a bandwidth allocation."""
        allocation = BandwidthAllocation(
            connection_id="test", destination="test.dest", requested_bandwidth=10.0
        )

        self.assertEqual(allocation.connection_id, "test")
        self.assertEqual(allocation.destination, "test.dest")
        self.assertEqual(allocation.requested_bandwidth, 10.0)
        self.assertEqual(allocation.allocated_bandwidth, 0.0)
        self.assertEqual(allocation.priority, 0)
        self.assertEqual(allocation.status, "pending")

    def test_allocation_repr(self):
        """Test string representation of allocation."""
        allocation = BandwidthAllocation(
            connection_id="test",
            destination="test.dest",
            requested_bandwidth=10.0,
            allocated_bandwidth=8.0,
            priority=5,
            status="allocated",
        )

        repr_str = repr(allocation)
        self.assertIn("test", repr_str)
        self.assertIn("test.dest", repr_str)
        self.assertIn("10.0", repr_str)
        self.assertIn("8.0", repr_str)


if __name__ == "__main__":
    unittest.main()
