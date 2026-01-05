"""
Low Power Mode Example

This example demonstrates how to use the Starlink connectivity tools
in low power mode, optimizing for energy efficiency while maintaining
connectivity.
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.connection_manager import ConnectionManager
from src.power_manager import PowerManager
from src.bandwidth_optimizer import BandwidthOptimizer
from src.diagnostics import Diagnostics


def main():
    """Run low power mode example."""
    print("Initializing Low Power Mode...")
    
    # Initialize components
    connection = ConnectionManager()
    power = PowerManager()
    bandwidth = BandwidthOptimizer()
    diagnostics = Diagnostics()
    
    # Connect to Starlink
    print("Establishing connection...")
    connection.connect()
    
    # Enable low power mode
    print("Enabling low power mode...")
    power.enable_low_power_mode()
    
    # Optimize bandwidth for low power operation
    print("Optimizing bandwidth for power efficiency...")
    bandwidth.adjust_bandwidth(target=50)  # Reduce bandwidth to 50% for power savings
    bandwidth.optimize()
    
    # Monitor power consumption
    print(f"Current power mode: {power.power_mode}")
    print(f"Power consumption: {power.get_power_consumption()}W")
    
    # Run diagnostics to ensure connection is stable
    print("Running diagnostics...")
    diagnostics.run_diagnostics()
    health = diagnostics.get_system_health()
    print(f"System Health: {health}")
    
    print("\nLow power mode active. Energy consumption optimized.")


if __name__ == "__main__":
    main()
