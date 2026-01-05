"""
Bandwidth optimization module for Starlink connectivity.

This module provides classes and methods for managing bandwidth allocation
across Starlink connections with support for prioritization.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BandwidthAllocation:
    """Represents a bandwidth allocation for a connection."""
    
    connection_id: str
    destination: str
    requested_bandwidth: float  # Mbps
    allocated_bandwidth: float = 0.0  # Mbps
    priority: int = 0  # Higher number = higher priority
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "pending"
    
    def __repr__(self):
        return (f"BandwidthAllocation(connection_id='{self.connection_id}', "
                f"destination='{self.destination}', "
                f"requested={self.requested_bandwidth}Mbps, "
                f"allocated={self.allocated_bandwidth}Mbps, "
                f"priority={self.priority}, status='{self.status}')")


class BandwidthOptimizer:
    """
    Bandwidth optimizer for Starlink connections.
    
    Manages bandwidth allocation across multiple connections with support for
    prioritization, ensuring critical connections (like medical emergencies)
    receive necessary bandwidth.
    """
    
    def __init__(self, total_bandwidth: float = 100.0):
        """
        Initialize the bandwidth optimizer.
        
        Args:
            total_bandwidth: Total available bandwidth in Mbps (default: 100.0)
        """
        self.total_bandwidth = total_bandwidth
        self.available_bandwidth = total_bandwidth
        self.allocations: Dict[str, BandwidthAllocation] = {}
        
    def allocate_bandwidth(
        self,
        connection_id: str,
        destination: str,
        requested_bandwidth: float,
        priority: int = 0
    ) -> BandwidthAllocation:
        """
        Allocate bandwidth for a connection.
        
        Args:
            connection_id: Unique identifier for the connection
            destination: Destination address or identifier
            requested_bandwidth: Requested bandwidth in Mbps
            priority: Priority level (higher = more important, default: 0)
            
        Returns:
            BandwidthAllocation object containing allocation details
            
        Example:
            >>> optimizer = BandwidthOptimizer()
            >>> allocation = optimizer.allocate_bandwidth(
            ...     connection_id="medical_evac",
            ...     destination="medical.data",
            ...     requested_bandwidth=10.0
            ... )
        """
        # Check if allocation already exists for this connection
        if connection_id in self.allocations:
            # Update existing allocation
            existing = self.allocations[connection_id]
            self.available_bandwidth += existing.allocated_bandwidth
            
        # Create new allocation
        allocation = BandwidthAllocation(
            connection_id=connection_id,
            destination=destination,
            requested_bandwidth=requested_bandwidth,
            priority=priority
        )
        
        # Determine how much bandwidth to allocate
        if requested_bandwidth <= self.available_bandwidth:
            # Full allocation available
            allocation.allocated_bandwidth = requested_bandwidth
            allocation.status = "allocated"
            self.available_bandwidth -= requested_bandwidth
        else:
            # Partial or no allocation - might need to reallocate from lower priority
            allocation.allocated_bandwidth = self.available_bandwidth
            allocation.status = "partial" if self.available_bandwidth > 0 else "queued"
            self.available_bandwidth = 0
            
        # Store the allocation
        self.allocations[connection_id] = allocation
        
        return allocation
    
    def release_bandwidth(self, connection_id: str) -> bool:
        """
        Release bandwidth allocated to a connection.
        
        Args:
            connection_id: Connection identifier to release
            
        Returns:
            True if bandwidth was released, False if connection not found
        """
        if connection_id in self.allocations:
            allocation = self.allocations[connection_id]
            self.available_bandwidth += allocation.allocated_bandwidth
            del self.allocations[connection_id]
            return True
        return False
    
    def get_allocation(self, connection_id: str) -> Optional[BandwidthAllocation]:
        """
        Get allocation details for a connection.
        
        Args:
            connection_id: Connection identifier
            
        Returns:
            BandwidthAllocation object or None if not found
        """
        return self.allocations.get(connection_id)
    
    def get_all_allocations(self) -> Dict[str, BandwidthAllocation]:
        """
        Get all current bandwidth allocations.
        
        Returns:
            Dictionary of all allocations keyed by connection_id
        """
        return self.allocations.copy()
    
    def get_available_bandwidth(self) -> float:
        """
        Get currently available bandwidth.
        
        Returns:
            Available bandwidth in Mbps
        """
        return self.available_bandwidth
    
    def __repr__(self):
        return (f"BandwidthOptimizer(total={self.total_bandwidth}Mbps, "
                f"available={self.available_bandwidth}Mbps, "
                f"allocations={len(self.allocations)})")
