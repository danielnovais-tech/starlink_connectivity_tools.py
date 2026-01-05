"""
Low Power Mode Example

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
