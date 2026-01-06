"""
Bandwidth Optimizer
Manages bandwidth allocation and traffic prioritization
"""

import logging
from typing import Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)


class TrafficPriority(Enum):
    """Traffic priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class BandwidthOptimizer:
    """Optimizes bandwidth allocation across services"""
    
    def __init__(self, total_bandwidth: float = 100.0):
        self.total_bandwidth = total_bandwidth
        self.available_bandwidth = total_bandwidth
        self.allocations: Dict[str, Dict[str, Any]] = {}
        self.crisis_mode = False
        
        logger.info(f"BandwidthOptimizer initialized with {total_bandwidth} Mbps")
    
    def enable_crisis_mode(self):
        """Enable crisis mode for bandwidth optimization"""
        self.crisis_mode = True
        logger.warning("Bandwidth optimizer crisis mode enabled")
    
    def allocate_bandwidth(self, connection_id: str, destination: str, 
                          requested_bandwidth: float) -> bool:
        """Allocate bandwidth for a specific connection"""
        if requested_bandwidth <= self.available_bandwidth:
            self.allocations[connection_id] = {
                'destination': destination,
                'allocated': requested_bandwidth,
                'priority': TrafficPriority.MEDIUM
            }
            self.available_bandwidth -= requested_bandwidth
            logger.info(f"Allocated {requested_bandwidth} Mbps to {connection_id}")
            return True
        else:
            logger.warning(f"Insufficient bandwidth for {connection_id}")
            return False
    
    def optimize_for_low_bandwidth(self, target_bandwidth: float):
        """Optimize for low bandwidth scenarios"""
        logger.info(f"Optimizing for low bandwidth: {target_bandwidth} Mbps")
        # In a real implementation, this would reallocate bandwidth
        self.total_bandwidth = target_bandwidth

        # Ensure available_bandwidth remains consistent with existing allocations
        allocated_bandwidth = sum(
            allocation.get("allocated", 0.0)
            for allocation in self.allocations.values()
        )

        if allocated_bandwidth >= self.total_bandwidth:
            # All bandwidth (or more) is already allocated; nothing is available
            logger.warning(
                "Allocated bandwidth (%.2f Mbps) exceeds or equals new total bandwidth "
                "(%.2f Mbps). Setting available_bandwidth to 0.",
                allocated_bandwidth,
                self.total_bandwidth,
            )
            self.available_bandwidth = 0.0
        else:
            # Available bandwidth is whatever remains under the new total, but not negative
            remaining = self.total_bandwidth - allocated_bandwidth
            self.available_bandwidth = min(self.available_bandwidth, remaining)
    
    def get_bandwidth_report(self) -> Dict[str, Any]:
        """Get bandwidth allocation report"""
        return {
            'total_bandwidth': self.total_bandwidth,
            'available_bandwidth': self.available_bandwidth,
            'crisis_mode': self.crisis_mode,
            'active_allocations': len(self.allocations),
            'allocations': self.allocations
        }
