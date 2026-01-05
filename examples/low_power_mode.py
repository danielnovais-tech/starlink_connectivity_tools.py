#!/usr/bin/env python3
"""
Low Power Mode Example

Demonstrates low power operation for extended battery runtime.
Shows how to minimize power consumption while maintaining connectivity.
"""

import sys
import time
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.connection_manager import ConnectionManager
from src.power_manager import PowerManager, PowerMode
from src.bandwidth_optimizer import BandwidthOptimizer
from src.starlink_monitor import StarlinkMonitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_low_power_mode(battery_capacity_wh: float = 1000.0, target_hours: float = 12.0):
    """
    Setup low power mode configuration.
    
    Args:
        battery_capacity_wh: Available battery capacity in watt-hours
        target_hours: Target runtime in hours
    """
    logger.info("="*60)
    logger.info("LOW POWER MODE SETUP")
    logger.info("="*60)
    
    # Initialize components
    connection_manager = ConnectionManager()
    power_manager = PowerManager()
    bandwidth_optimizer = BandwidthOptimizer()
    monitor = StarlinkMonitor()
    
    # Display configuration
    logger.info(f"\n📋 Configuration:")
    logger.info(f"   Battery Capacity: {battery_capacity_wh}Wh")
    logger.info(f"   Target Runtime: {target_hours} hours")
    
    # Step 1: Connect to Starlink
    logger.info("\n1. Establishing connection...")
    if connection_manager.connect():
        logger.info("✓ Connected to Starlink")
    else:
        logger.warning("✗ Connection failed")
        return
    
    # Step 2: Optimize power mode for target runtime
    logger.info(f"\n2. Optimizing power for {target_hours}h runtime...")
    
    recommended_mode = power_manager.optimize_for_battery(
        target_hours, battery_capacity_wh
    )
    
    logger.info(f"   Recommended mode: {recommended_mode.value}")
    power_manager.set_power_mode(recommended_mode)
    
    power_status = power_manager.get_power_status()
    actual_runtime = power_manager.estimate_runtime(battery_capacity_wh)
    
    logger.info(f"✓ Power mode set to: {power_status['current_mode']}")
    logger.info(f"   Current power: {power_status['current_power_watts']}W")
    logger.info(f"   Max power: {power_status['max_power_watts']}W")
    logger.info(f"   Estimated runtime: {actual_runtime:.1f} hours")
    logger.info(f"   Efficiency: {power_status['power_efficiency']:.1f}%")
    
    # Step 3: Set low power bandwidth profile
    logger.info("\n3. Configuring bandwidth...")
    bandwidth_optimizer.set_profile("low_power")
    
    optimization = bandwidth_optimizer.optimize_bandwidth()
    logger.info(f"✓ Bandwidth profile: {optimization['profile']}")
    logger.info(f"   Download limit: {optimization['download_limit']} Mbps")
    logger.info(f"   Upload limit: {optimization['upload_limit']} Mbps")
    logger.info(f"   QoS enabled: {optimization['qos_active']}")
    
    # Step 4: Check connectivity
    logger.info("\n4. Checking connectivity metrics...")
    metrics = monitor.get_current_metrics()
    
    logger.info(f"✓ Connection metrics:")
    logger.info(f"   Signal quality: {metrics['signal_quality']}%")
    logger.info(f"   Satellites: {metrics['satellites_visible']}")
    logger.info(f"   Latency: {metrics['latency_ms']} ms")
    logger.info(f"   Download: {metrics['download_mbps']} Mbps")
    logger.info(f"   Upload: {metrics['upload_mbps']} Mbps")
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("LOW POWER MODE ACTIVE")
    logger.info("="*60)
    logger.info("\n🔋 Power Configuration:")
    logger.info(f"   Mode: {power_status['current_mode']}")
    logger.info(f"   Consumption: {power_status['current_power_watts']}W")
    logger.info(f"   Runtime: {actual_runtime:.1f}h (target: {target_hours}h)")
    logger.info(f"   Features: {', '.join(power_status['features_enabled'])}")
    
    logger.info("\n📊 Bandwidth Configuration:")
    logger.info(f"   Profile: {optimization['profile']}")
    logger.info(f"   Limits: {optimization['download_limit']} Mbps down / {optimization['upload_limit']} Mbps up")
    
    logger.info("\n📡 Connection Status:")
    logger.info(f"   Quality: {metrics['signal_quality']}%")
    logger.info(f"   Satellites: {metrics['satellites_visible']}")
    
    # Recommendations
    recommendations = power_manager.get_power_recommendations()
    if recommendations:
        logger.info("\n💡 Recommendations:")
        for rec in recommendations:
            logger.info(f"   • {rec}")
    
    logger.info("\n" + "="*60)
    
    return {
        'connection_manager': connection_manager,
        'power_manager': power_manager,
        'bandwidth_optimizer': bandwidth_optimizer,
        'monitor': monitor
    }


def monitor_low_power_operation(components: dict, duration_seconds: int = 60):
    """
    Monitor system operation in low power mode.
    
    Args:
        components: Dictionary of initialized components
        duration_seconds: Monitoring duration
    """
    logger.info("\n" + "="*60)
    logger.info("MONITORING LOW POWER OPERATION")
    logger.info("="*60)
    
    monitor = components['monitor']
    power_manager = components['power_manager']
    
    logger.info(f"\nMonitoring for {duration_seconds} seconds...")
    logger.info("Press Ctrl+C to stop\n")
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration_seconds:
            elapsed = int(time.time() - start_time)
            
            # Get current metrics
            metrics = monitor.get_current_metrics()
            power_status = power_manager.get_power_status()
            alerts = monitor.check_alerts()
            
            # Display status
            logger.info(f"[T+{elapsed}s] Status:")
            logger.info(f"  🔋 Power: {power_status['current_power_watts']}W "
                       f"({power_status['current_mode']})")
            logger.info(f"  📡 Signal: {metrics['signal_quality']}% | "
                       f"Sats: {metrics['satellites_visible']}")
            logger.info(f"  📶 Speed: ⬇️{metrics['download_mbps']:.1f} / "
                       f"⬆️{metrics['upload_mbps']:.1f} Mbps")
            logger.info(f"  ⏱️  Latency: {metrics['latency_ms']} ms")
            
            if alerts:
                logger.warning(f"  ⚠️  Alerts: {len(alerts)}")
                for alert in alerts[:2]:  # Show first 2 alerts
                    logger.warning(f"     - {alert['message']}")
            
            # Log power usage
            power_manager.log_power_usage()
            
            logger.info("")
            time.sleep(15)
    
    except KeyboardInterrupt:
        logger.info("\nMonitoring stopped by user")
    
    logger.info(f"\n✓ Monitoring complete")


def compare_power_modes():
    """Compare different power modes."""
    logger.info("\n" + "="*60)
    logger.info("POWER MODE COMPARISON")
    logger.info("="*60)
    
    power_manager = PowerManager()
    battery_capacity = 1000.0  # 1000Wh
    
    modes = [PowerMode.NORMAL, PowerMode.ECO, PowerMode.LOW_POWER, PowerMode.EMERGENCY]
    
    logger.info(f"\nBattery Capacity: {battery_capacity}Wh\n")
    logger.info(f"{'Mode':<15} {'Power (W)':<12} {'Runtime (h)':<15} {'Features'}")
    logger.info("-" * 60)
    
    for mode in modes:
        power_manager.set_power_mode(mode)
        status = power_manager.get_power_status()
        runtime = power_manager.estimate_runtime(battery_capacity)
        features = ', '.join(status['features_enabled'][:2]) + "..."
        
        logger.info(f"{mode.value:<15} "
                   f"{status['current_power_watts']:<12.1f} "
                   f"{runtime:<15.1f} "
                   f"{features}")
    
    logger.info("\n" + "="*60)


def main():
    """Main entry point."""
    logger.info("\n" + "🔋 "*20)
    logger.info("Low Power Mode Example - Starlink Connectivity Tools")
    logger.info("🔋 "*20 + "\n")
    
    try:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--battery', type=float, default=1000.0,
                          help='Battery capacity in Wh (default: 1000)')
        parser.add_argument('--target-hours', type=float, default=12.0,
                          help='Target runtime in hours (default: 12)')
        parser.add_argument('--monitor', action='store_true',
                          help='Monitor operation after setup')
        parser.add_argument('--compare', action='store_true',
                          help='Compare power modes')
        parser.add_argument('--duration', type=int, default=60,
                          help='Monitoring duration in seconds (default: 60)')
        args = parser.parse_args()
        
        if args.compare:
            compare_power_modes()
        else:
            # Setup low power mode
            components = setup_low_power_mode(args.battery, args.target_hours)
            
            if components and args.monitor:
                time.sleep(2)
                monitor_low_power_operation(components, args.duration)
        
        logger.info("\n✓ Low power mode example completed successfully\n")
        
    except KeyboardInterrupt:
        logger.info("\n\nExample interrupted by user")
    except Exception as e:
        logger.error(f"\nError: {e}")
        raise
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
