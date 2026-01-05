#!/usr/bin/env python3
"""
Emergency Mode Example - Updated with Starlink

Demonstrates emergency mode operation for critical communications.
Optimizes power and bandwidth for extended operation during emergencies.
"""

import sys
import time
import logging

# Add parent directory to path
sys.path.insert(0, '/home/runner/work/starlink_connectivity_tools.py/starlink_connectivity_tools.py')

from src.connection_manager import ConnectionManager
from src.power_manager import PowerManager, PowerMode
from src.bandwidth_optimizer import BandwidthOptimizer
from src.starlink_monitor import StarlinkMonitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def activate_emergency_mode():
    """Activate emergency mode configuration."""
    logger.info("="*60)
    logger.info("ACTIVATING EMERGENCY MODE")
    logger.info("="*60)
    
    # Initialize components
    connection_manager = ConnectionManager()
    power_manager = PowerManager()
    bandwidth_optimizer = BandwidthOptimizer()
    monitor = StarlinkMonitor()
    
    # Step 1: Check Starlink connection
    logger.info("\n1. Checking Starlink connection...")
    if connection_manager.connect():
        logger.info("✓ Connected to Starlink")
    else:
        logger.warning("✗ Starlink unavailable, using fallback")
    
    # Step 2: Set emergency power mode
    logger.info("\n2. Setting emergency power mode...")
    power_manager.set_power_mode(PowerMode.EMERGENCY)
    
    power_status = power_manager.get_power_status()
    logger.info(f"✓ Power mode: {power_status['current_mode']}")
    logger.info(f"  Current power: {power_status['current_power_watts']}W")
    logger.info(f"  Max power: {power_status['max_power_watts']}W")
    
    # Estimate battery runtime
    battery_capacity = 1000  # 1000Wh battery
    runtime = power_manager.estimate_runtime(battery_capacity)
    logger.info(f"  Estimated runtime: {runtime:.1f} hours")
    
    # Step 3: Set low power bandwidth profile
    logger.info("\n3. Setting low power bandwidth profile...")
    bandwidth_optimizer.set_profile("low_power")
    
    optimization = bandwidth_optimizer.optimize_bandwidth()
    logger.info(f"✓ Bandwidth profile: {optimization['profile']}")
    logger.info(f"  Download limit: {optimization['download_limit']} Mbps")
    logger.info(f"  Upload limit: {optimization['upload_limit']} Mbps")
    
    # Step 4: Monitor Starlink metrics
    logger.info("\n4. Monitoring Starlink metrics...")
    metrics = monitor.get_current_metrics()
    logger.info(f"✓ Signal quality: {metrics['signal_quality']}%")
    logger.info(f"  Satellites: {metrics['satellites_visible']}")
    logger.info(f"  Latency: {metrics['latency_ms']} ms")
    
    # Check for alerts
    alerts = monitor.check_alerts()
    if alerts:
        logger.warning(f"\n⚠️  Active alerts: {len(alerts)}")
        for alert in alerts:
            logger.warning(f"  - {alert['message']}")
    else:
        logger.info("\n✓ No alerts - System operating normally")
    
    # Step 5: Summary
    logger.info("\n" + "="*60)
    logger.info("EMERGENCY MODE ACTIVATED")
    logger.info("="*60)
    logger.info("\nConfiguration Summary:")
    logger.info(f"  - Power Mode: {power_status['current_mode']}")
    logger.info(f"  - Power Consumption: {power_status['current_power_watts']}W")
    logger.info(f"  - Battery Runtime: {runtime:.1f} hours")
    logger.info(f"  - Bandwidth Profile: {optimization['profile']}")
    logger.info(f"  - Connection: Starlink")
    logger.info(f"  - Signal Quality: {metrics['signal_quality']}%")
    logger.info("\nEmergency mode is optimized for:")
    logger.info("  ✓ Extended battery life")
    logger.info("  ✓ Critical communications only")
    logger.info("  ✓ Minimal power consumption")
    logger.info("  ✓ Essential services prioritized")
    logger.info("\n" + "="*60)


def simulate_emergency_operation(duration_seconds: int = 30):
    """
    Simulate emergency mode operation.
    
    Args:
        duration_seconds: How long to simulate
    """
    logger.info(f"\nSimulating emergency operation for {duration_seconds} seconds...")
    
    monitor = StarlinkMonitor()
    start_time = time.time()
    
    while time.time() - start_time < duration_seconds:
        metrics = monitor.get_current_metrics()
        alerts = monitor.check_alerts()
        
        # Log status
        elapsed = int(time.time() - start_time)
        logger.info(f"\n[T+{elapsed}s] Status Update:")
        logger.info(f"  Signal: {metrics['signal_quality']}% | "
                   f"Latency: {metrics['latency_ms']}ms | "
                   f"Satellites: {metrics['satellites_visible']}")
        
        if alerts:
            for alert in alerts:
                logger.warning(f"  ⚠️  {alert['message']}")
        
        time.sleep(10)
    
    logger.info("\nEmergency operation simulation complete")


def main():
    """Main entry point."""
    logger.info("\n" + "🚨 "*15)
    logger.info("Emergency Mode Example - Starlink Connectivity Tools")
    logger.info("🚨 "*15 + "\n")
    
    try:
        # Activate emergency mode
        activate_emergency_mode()
        
        # Optionally run simulation
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--simulate', action='store_true',
                          help='Run emergency mode simulation')
        parser.add_argument('--duration', type=int, default=30,
                          help='Simulation duration in seconds')
        args = parser.parse_args()
        
        if args.simulate:
            simulate_emergency_operation(args.duration)
        
        logger.info("\n✓ Emergency mode example completed successfully\n")
        
    except KeyboardInterrupt:
        logger.info("\n\nEmergency mode interrupted by user")
    except Exception as e:
        logger.error(f"\nError in emergency mode: {e}")
        raise


if __name__ == "__main__":
    main()
