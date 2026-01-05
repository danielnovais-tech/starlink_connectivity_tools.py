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
Demonstrates how to configure Starlink tools for battery-powered scenarios
with power optimization and reduced consumption.
"""

import sys
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

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
from src.config.settings import Settings


def main():
    """Run low power mode configuration."""
    print("=== Starlink Low Power Mode ===\n")

    # Initialize settings for low power mode
    low_power_config = {
        "connection": {
            "timeout": 45,
            "retry_attempts": 2,
        },
        "power": {
            "default_mode": "low_power",
        },
        "bandwidth": {
            "default_limit": 25,  # Limit to 25 Mbps
            "optimization_enabled": True,
        },
    }
    settings = Settings(custom_config=low_power_config)
    print("Low power configuration loaded")
    print(f"Power mode: {settings.get('power.default_mode')}")
    print(f"Bandwidth limit: {settings.get('bandwidth.default_limit')} Mbps\n")

    # Set up power manager
    power_manager = PowerManager()
    power_manager.enable_low_power_mode()
    print("Power management:")
    power_status = power_manager.get_power_status()
    print(f"  Mode: {power_status['power_mode']}")
    print(f"  Low power enabled: {power_status['low_power_enabled']}")
    print(f"  Power consumption: {power_status['power_consumption']}%")

    # Estimate battery runtime
    battery_capacity = 500  # Wh
    runtime = power_manager.estimate_runtime(battery_capacity)
    print(f"  Estimated runtime (500Wh battery): {runtime:.1f} hours\n")

    # Set up bandwidth optimizer
    bandwidth_optimizer = BandwidthOptimizer(
        max_bandwidth=settings.get("bandwidth.default_limit")
    )
    bandwidth_optimizer.enable_optimization()
    print("Bandwidth optimization:")
    usage = bandwidth_optimizer.get_current_usage()
    print(f"  Optimization enabled: {usage['optimization_enabled']}")
    print(f"  Max bandwidth: {usage['max_bandwidth']} Mbps\n")

    # Connect with low power settings
    connection_manager = ConnectionManager(config=settings.get_all())
    print("Connecting to Starlink in low power mode...")
    if connection_manager.connect():
        print("✓ Connected successfully\n")
    else:
        print("✗ Connection failed\n")

    print("Low power mode is now active!")
    print(f"Power consumption reduced to {power_status['power_consumption']}% of normal.")
    print("Bandwidth is optimized for efficiency.")


if __name__ == "__main__":
    main()
