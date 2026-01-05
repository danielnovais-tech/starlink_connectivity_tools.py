"""
Bandwidth Optimizer
Manages bandwidth allocation and traffic prioritization
"""

import logging
from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


class TrafficPriority(Enum):
    """Traffic priority levels"""
    CRITICAL = 1      # Emergency services, SOS
    HIGH = 2          # Medical data, essential services
    MEDIUM = 3        # General communications
    LOW = 4           # Background tasks, updates
    BACKGROUND = 5    # Non-essential transfers


@dataclass
class BandwidthAllocation:
    """Represents a bandwidth allocation"""
    connection_id: str
    destination: str
    allocated_bandwidth: float  # Mbps
    requested_bandwidth: float  # Mbps
    priority: TrafficPriority
    timestamp: datetime
    active: bool = True


class BandwidthOptimizer:
    """
    Optimizes bandwidth allocation across connections
    """
    
    def __init__(self, total_bandwidth: float = 100.0):
        """
        Initialize bandwidth optimizer
        
        Args:
            total_bandwidth: Total available bandwidth in Mbps
        """
        self.total_bandwidth = total_bandwidth
        self.available_bandwidth = total_bandwidth
        self.allocations: Dict[str, BandwidthAllocation] = {}
        self.crisis_mode = False
        
        # Crisis mode priority destinations
        self.critical_destinations = {
            "emergency.comms",
            "medical.data",
            "sos.messages",
            "coord.central"
        }
        
        logger.info(f"BandwidthOptimizer initialized with {total_bandwidth} Mbps")
    
    def enable_crisis_mode(self):
        """
        Enable crisis mode - prioritize critical traffic only
        """
        self.crisis_mode = True
        logger.warning("Bandwidth crisis mode enabled - critical traffic only")
        
        # Release non-critical allocations
        self._release_non_critical_allocations()
    
    def _release_non_critical_allocations(self):
        """Release bandwidth from non-critical connections"""
        to_release = []
        
        for conn_id, allocation in self.allocations.items():
            if allocation.destination not in self.critical_destinations:
                to_release.append(conn_id)
        
        for conn_id in to_release:
            logger.info(f"Releasing non-critical allocation: {conn_id}")
            self.release_bandwidth(conn_id)
    
    def _determine_priority(self, destination: str) -> TrafficPriority:
        """
        Determine priority based on destination
        
        Args:
            destination: Destination identifier
            
        Returns:
            TrafficPriority for the destination
        """
        if destination in self.critical_destinations:
            return TrafficPriority.CRITICAL
        elif "medical" in destination.lower():
            return TrafficPriority.HIGH
        elif "emergency" in destination.lower():
            return TrafficPriority.CRITICAL
        else:
            return TrafficPriority.MEDIUM
    
    def allocate_bandwidth(self,
                          connection_id: str,
                          destination: str,
                          requested_bandwidth: float) -> float:
        """
        Allocate bandwidth for a connection
        
        Args:
            connection_id: Unique identifier for the connection
            destination: Destination identifier
            requested_bandwidth: Requested bandwidth in Mbps
            
        Returns:
            Actually allocated bandwidth in Mbps
        """
        priority = self._determine_priority(destination)
        
        # In crisis mode, only allow critical traffic
        if self.crisis_mode and priority not in [TrafficPriority.CRITICAL, TrafficPriority.HIGH]:
            logger.warning(f"Denying non-critical allocation in crisis mode: {connection_id}")
            return 0.0
        
        # Determine allocation amount
        if requested_bandwidth <= self.available_bandwidth:
            allocated = requested_bandwidth
        else:
            # Allocate what's available
            allocated = self.available_bandwidth
            logger.warning(f"Partial allocation for {connection_id}: {allocated}/{requested_bandwidth} Mbps")
        
        # Ensure minimum for critical traffic
        if priority == TrafficPriority.CRITICAL and allocated < 1.0:
            # Try to free up bandwidth from lower priority
            self._free_bandwidth_for_critical(1.0 - allocated)
            allocated = min(1.0, self.available_bandwidth)
        
        if allocated > 0:
            allocation = BandwidthAllocation(
                connection_id=connection_id,
                destination=destination,
                allocated_bandwidth=allocated,
                requested_bandwidth=requested_bandwidth,
                priority=priority,
                timestamp=datetime.now()
            )
            
            self.allocations[connection_id] = allocation
            self.available_bandwidth -= allocated
            
            logger.info(f"Allocated {allocated:.2f} Mbps for {connection_id} ({destination})")
        
        return allocated
    
    def _free_bandwidth_for_critical(self, amount_needed: float):
        """
        Free up bandwidth by releasing lower priority allocations
        
        Args:
            amount_needed: Amount of bandwidth to free in Mbps
        """
        freed = 0.0
        to_release = []
        
        # Sort by priority (lower priority first)
        sorted_allocations = sorted(
            self.allocations.items(),
            key=lambda x: x[1].priority.value,
            reverse=True
        )
        
        for conn_id, allocation in sorted_allocations:
            if allocation.priority in [TrafficPriority.CRITICAL, TrafficPriority.HIGH]:
                continue
            
            to_release.append(conn_id)
            freed += allocation.allocated_bandwidth
            
            if freed >= amount_needed:
                break
        
        for conn_id in to_release:
            logger.info(f"Preempting {conn_id} for critical traffic")
            self.release_bandwidth(conn_id)
    
    def release_bandwidth(self, connection_id: str):
        """
        Release bandwidth allocation
        
        Args:
            connection_id: Connection to release
        """
        if connection_id in self.allocations:
            allocation = self.allocations[connection_id]
            self.available_bandwidth += allocation.allocated_bandwidth
            del self.allocations[connection_id]
            
            logger.info(f"Released {allocation.allocated_bandwidth:.2f} Mbps from {connection_id}")
    
    def get_bandwidth_report(self) -> dict:
        """
        Get current bandwidth status report
        
        Returns:
            Dictionary with bandwidth information
        """
        return {
            'total_bandwidth': self.total_bandwidth,
            'available_bandwidth': self.available_bandwidth,
            'allocated_bandwidth': self.total_bandwidth - self.available_bandwidth,
            'active_allocations': len(self.allocations),
            'crisis_mode': self.crisis_mode
        }
