"""
Emergency Mode Example

This example demonstrates how to use the Starlink connectivity tools
in emergency mode, prioritizing critical communications and optimizing
for reliability over performance.
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.connection_manager import ConnectionManager
from src.bandwidth_optimizer import BandwidthOptimizer
from src.failover_handler import FailoverHandler
from src.diagnostics import Diagnostics


def main():
    """Run emergency mode example."""
    print("Initializing Emergency Mode...")
    
    # Initialize components
    connection = ConnectionManager()
    bandwidth = BandwidthOptimizer()
    failover = FailoverHandler()
    diagnostics = Diagnostics()
    
    # Connect to Starlink
    print("Establishing connection...")
    connection.connect()
    
    # Set bandwidth optimization for emergency mode
    print("Optimizing for emergency communications...")
    bandwidth.set_priority('emergency_calls', priority=1)
    bandwidth.set_priority('data', priority=3)
    bandwidth.optimize()
    
    # Enable failover monitoring
    print("Enabling failover monitoring...")
    failover.detect_failure()
    
    # Run diagnostics
    print("Running diagnostics...")
    diagnostics.run_diagnostics()
    health = diagnostics.get_system_health()
    print(f"System Health: {health}")
    
    print("\nEmergency mode active. Critical communications prioritized.")


if __name__ == "__main__":
    main()
