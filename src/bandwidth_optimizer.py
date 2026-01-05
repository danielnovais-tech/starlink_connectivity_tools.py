"""
Bandwidth optimization for critical communications
"""
import threading
import time
import logging
from typing import Dict, List, Set
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TrafficPriority(Enum):
    """Traffic priority levels"""
    CRITICAL = 0      # Emergency communications, SOS
    HIGH = 1          # Medical data, coordination
    MEDIUM = 2        # General information
    LOW = 3           # Non-essential updates
    BACKGROUND = 4    # Software updates, backups


@dataclass
class TrafficRule:
    """Rule for traffic management"""
    pattern: str  # URL pattern, port, or protocol
    priority: TrafficPriority
    max_bandwidth: float  # Mbps
    burst_allowed: bool


class BandwidthOptimizer:
    """Optimizes bandwidth usage for critical communications"""
    
    def __init__(self, total_bandwidth: float = 100.0):
        self.total_bandwidth = total_bandwidth
        self.available_bandwidth = total_bandwidth
        self.traffic_rules: List[TrafficRule] = []
        self.active_connections: Dict[str, Dict] = {}
        self.crisis_mode = False
        
        # Default rules for crisis scenarios
        self._setup_default_rules()
        
        # Bandwidth allocation lock
        self.lock = threading.RLock()
    
    def _setup_default_rules(self):
        """Setup default traffic rules for crisis scenarios"""
        default_rules = [
            TrafficRule(
                pattern=":443/emergency/",
                priority=TrafficPriority.CRITICAL,
                max_bandwidth=50.0,
                burst_allowed=True
            ),
            TrafficRule(
                pattern=":443/medical/",
                priority=TrafficPriority.HIGH,
                max_bandwidth=30.0,
                burst_allowed=True
            ),
            TrafficRule(
                pattern=":80/",
                priority=TrafficPriority.MEDIUM,
                max_bandwidth=20.0,
                burst_allowed=False
            ),
            TrafficRule(
                pattern=":22",  # SSH
                priority=TrafficPriority.HIGH,
                max_bandwidth=10.0,
                burst_allowed=True
            ),
            TrafficRule(
                pattern="update",  # Software updates
                priority=TrafficPriority.BACKGROUND,
                max_bandwidth=5.0,
                burst_allowed=False
            )
        ]
        
        self.traffic_rules.extend(default_rules)
    
    def enable_crisis_mode(self):
        """Enable crisis mode bandwidth optimization"""
        self.crisis_mode = True
        
        # Reallocate bandwidth for critical services
        for rule in self.traffic_rules:
            if rule.priority == TrafficPriority.CRITICAL:
                rule.max_bandwidth = self.total_bandwidth * 0.6  # 60% for critical
            elif rule.priority == TrafficPriority.HIGH:
                rule.max_bandwidth = self.total_bandwidth * 0.3  # 30% for high
            else:
                rule.max_bandwidth = self.total_bandwidth * 0.1  # 10% for others
        
        logger.info("Crisis mode enabled for bandwidth optimization")
    
    def allocate_bandwidth(self, connection_id: str, 
                          destination: str, 
                          requested_bandwidth: float) -> float:
        """
        Allocate bandwidth based on traffic rules and priority
        
        Returns: allocated bandwidth (may be less than requested)
        """
        with self.lock:
            priority = self._determine_priority(destination)
            max_allowed = self._get_max_bandwidth_for_priority(priority)
            
            # Calculate available for this priority
            allocated_for_priority = sum(
                conn['allocated'] 
                for conn in self.active_connections.values() 
                if conn['priority'] == priority
            )
            
            available_for_priority = max(0, max_allowed - allocated_for_priority)
            
            # Calculate overall available
            total_allocated = sum(conn['allocated'] 
                                for conn in self.active_connections.values())
            overall_available = self.available_bandwidth - total_allocated
            
            # Determine allocation
            allocation = min(
                requested_bandwidth,
                available_for_priority,
                overall_available
            )
            
            if allocation > 0:
                self.active_connections[connection_id] = {
                    'destination': destination,
                    'priority': priority,
                    'allocated': allocation,
                    'requested': requested_bandwidth,
                    'timestamp': time.time()
                }
                
                logger.info(f"Allocated {allocation:.2f}Mbps for {destination} "
                           f"(priority: {priority.name})")
            
            return allocation
    
    def _determine_priority(self, destination: str) -> TrafficPriority:
        """Determine priority based on destination and rules"""
        for rule in self.traffic_rules:
            if rule.pattern in destination:
                return rule.priority
        
        # Default to medium priority
        return TrafficPriority.MEDIUM
    
    def _get_max_bandwidth_for_priority(self, priority: TrafficPriority) -> float:
        """Get maximum bandwidth allowed for a priority level"""
        for rule in self.traffic_rules:
            if rule.priority == priority:
                return rule.max_bandwidth
        return 0.0
    
    def release_bandwidth(self, connection_id: str):
        """Release allocated bandwidth for a connection"""
        with self.lock:
            if connection_id in self.active_connections:
                released = self.active_connections[connection_id]['allocated']
                del self.active_connections[connection_id]
                logger.info(f"Released {released:.2f}Mbps from {connection_id}")
    
    def adjust_total_bandwidth(self, new_total: float):
        """Adjust total available bandwidth"""
        with self.lock:
            self.total_bandwidth = new_total
            self.available_bandwidth = new_total
            
            # Adjust rules proportionally
            for rule in self.traffic_rules:
                rule.max_bandwidth = (rule.max_bandwidth / self.total_bandwidth) * new_total
            
            logger.info(f"Adjusted total bandwidth to {new_total:.2f}Mbps")
    
    def get_bandwidth_report(self) -> Dict:
        """Generate bandwidth usage report"""
        with self.lock:
            report = {
                'total_bandwidth': self.total_bandwidth,
                'crisis_mode': self.crisis_mode,
                'active_connections': len(self.active_connections),
                'timestamp': time.time(),
                'allocations_by_priority': {},
                'total_allocated': 0
            }
            
            # Calculate allocations by priority
            for priority in TrafficPriority:
                allocated = sum(
                    conn['allocated'] 
                    for conn in self.active_connections.values() 
                    if conn['priority'] == priority
                )
                report['allocations_by_priority'][priority.name] = allocated
                report['total_allocated'] += allocated
            
            report['available_bandwidth'] = (
                self.total_bandwidth - report['total_allocated']
            )
            
            return report
    
    def optimize_for_low_bandwidth(self, available_bandwidth: float):
        """
        Optimize settings for low bandwidth scenarios
        Useful when only minimal connectivity is available
        """
        self.adjust_total_bandwidth(available_bandwidth)
        
        # Reduce non-critical allocations
        for rule in self.traffic_rules:
            if rule.priority.value >= TrafficPriority.MEDIUM.value:
                rule.max_bandwidth *= 0.5  # Reduce by 50%
            elif rule.priority == TrafficPriority.BACKGROUND:
                rule.max_bandwidth = 0.1  # Minimal for background
        
        logger.info(f"Optimized for low bandwidth scenario: {available_bandwidth}Mbps")
Bandwidth Optimizer Module

Optimizes bandwidth usage and manages network traffic for Starlink connections.
"""


class BandwidthOptimizer:
    """Optimizes bandwidth usage for Starlink connections."""

    def __init__(self, max_bandwidth=None):
        """
        Initialize the BandwidthOptimizer.

        Args:
            max_bandwidth: Maximum bandwidth in Mbps (None for unlimited)
        """
        self.max_bandwidth = max_bandwidth
        self.current_usage = 0
        self.optimization_enabled = False

    def enable_optimization(self):
        """
        Enable bandwidth optimization.

        Returns:
            bool: True if optimization enabled successfully
        """
        self.optimization_enabled = True
        return True

    def disable_optimization(self):
        """
        Disable bandwidth optimization.

        Returns:
            bool: True if optimization disabled successfully
        """
        self.optimization_enabled = False
        return True

    def set_bandwidth_limit(self, limit):
        """
        Set maximum bandwidth limit.

        Args:
            limit: Bandwidth limit in Mbps

        Returns:
            bool: True if limit set successfully
        """
        self.max_bandwidth = limit
        return True

    def get_current_usage(self):
        """
        Get current bandwidth usage.

        Returns:
            dict: Current bandwidth usage information
        """
        return {
            "current_usage": self.current_usage,
            "max_bandwidth": self.max_bandwidth,
            "optimization_enabled": self.optimization_enabled,
        }

    def optimize(self):
        """
        Perform bandwidth optimization.

        Returns:
            dict: Optimization results
        """
        if not self.optimization_enabled:
            return {"status": "optimization_disabled"}

        # Placeholder implementation
        return {
            "status": "optimized",
            "savings": 0,
        }
