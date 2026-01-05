#!/usr/bin/env python3
"""
Venezuela Scenario - NEW: Specific scenario

Demonstrates Starlink connectivity optimization for challenging scenarios
like those in Venezuela, with focus on power management, internet censorship
workarounds, and reliable emergency communications.
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
from src.failover_handler import FailoverHandler
from src.starlink_monitor import StarlinkMonitor
from src.diagnostics import Diagnostics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_venezuela_scenario():
    """
    Setup optimized configuration for Venezuela scenario.
    
    Key considerations:
    - Unreliable power grid (frequent outages)
    - Need for battery operation
    - Priority on critical communications
    - Internet censorship bypass
    - High latency fallback connections
    """
    logger.info("="*70)
    logger.info("VENEZUELA SCENARIO - Starlink Connectivity Setup")
    logger.info("="*70)
    
    # Initialize components
    connection_manager = ConnectionManager()
    power_manager = PowerManager()
    bandwidth_optimizer = BandwidthOptimizer()
    failover_handler = FailoverHandler(
        primary_connection="starlink",
        backup_connections=["cellular_4g", "satellite_backup"]
    )
    monitor = StarlinkMonitor()
    diagnostics = Diagnostics()
    
    # Scenario: Preparing for power outage
    logger.info("\n📋 SCENARIO: Preparing for anticipated power grid outage")
    logger.info("-" * 70)
    
    # Step 1: Establish Starlink connection
    logger.info("\n1️⃣  Establishing Starlink connection...")
    if connection_manager.connect():
        logger.info("✅ Starlink connected successfully")
        health = connection_manager.check_starlink_health()
        logger.info(f"   Signal Quality: {health['signal_quality']}%")
        logger.info(f"   Obstructed: {health['obstructed']}")
        logger.info(f"   Uptime: {health['uptime']} seconds")
    else:
        logger.error("❌ Failed to connect to Starlink")
        return
    
    # Step 2: Optimize for battery operation
    logger.info("\n2️⃣  Optimizing for battery operation...")
    
    # Assume 500Wh battery capacity (typical for Venezuela scenario)
    battery_capacity_wh = 500
    target_runtime_hours = 8  # Target: 8 hours runtime
    
    logger.info(f"   Battery capacity: {battery_capacity_wh}Wh")
    logger.info(f"   Target runtime: {target_runtime_hours} hours")
    
    recommended_mode = power_manager.optimize_for_battery(
        target_runtime_hours, battery_capacity_wh
    )
    power_manager.set_power_mode(recommended_mode)
    
    power_status = power_manager.get_power_status()
    actual_runtime = power_manager.estimate_runtime(battery_capacity_wh)
    
    logger.info(f"✅ Power mode set to: {power_status['current_mode']}")
    logger.info(f"   Current consumption: {power_status['current_power_watts']}W")
    logger.info(f"   Estimated runtime: {actual_runtime:.1f} hours")
    
    # Step 3: Configure bandwidth for essential services
    logger.info("\n3️⃣  Configuring bandwidth priorities...")
    
    bandwidth_optimizer.set_profile("low_power")
    
    # Prioritize critical applications
    critical_apps = [
        ("messaging", 10),  # Highest priority
        ("email", 9),
        ("news", 8),
        ("voip", 7),
    ]
    
    for app, priority in critical_apps:
        bandwidth_optimizer.prioritize_traffic(app, priority)
        logger.info(f"   ✓ {app}: Priority {priority}/10")
    
    optimization = bandwidth_optimizer.optimize_bandwidth()
    logger.info(f"✅ Bandwidth optimized")
    logger.info(f"   Profile: {optimization['profile']}")
    logger.info(f"   Download limit: {optimization['download_limit']} Mbps")
    logger.info(f"   Upload limit: {optimization['upload_limit']} Mbps")
    
    # Step 4: Configure failover for resilience
    logger.info("\n4️⃣  Configuring failover resilience...")
    
    failover_status = failover_handler.get_status()
    logger.info(f"✅ Failover configured")
    logger.info(f"   Primary: {failover_status['primary_connection']}")
    logger.info(f"   Backups: {', '.join(failover_handler.backup_connections)}")
    logger.info(f"   Current: {failover_status['current_connection']}")
    
    # Step 5: Run diagnostics
    logger.info("\n5️⃣  Running connectivity diagnostics...")
    
    diag_results = diagnostics.run_full_diagnostic()
    logger.info(f"✅ Diagnostics complete")
    logger.info(f"   Overall health: {diag_results['overall_health']}")
    logger.info(f"   Internet accessible: {diag_results['connectivity']['internet_accessible']}")
    logger.info(f"   Latency: {diag_results['network_performance']['latency_ms']} ms")
    logger.info(f"   Packet loss: {diag_results['network_performance']['packet_loss_percent']}%")
    
    # Step 6: Monitor for issues
    logger.info("\n6️⃣  Checking for issues...")
    
    alerts = monitor.check_alerts()
    if alerts:
        logger.warning(f"⚠️  Found {len(alerts)} alerts:")
        for alert in alerts:
            severity_icon = "🔴" if alert['severity'] == 'critical' else "🟡"
            logger.warning(f"   {severity_icon} {alert['message']}")
    else:
        logger.info("✅ No alerts - all systems nominal")
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("VENEZUELA SCENARIO CONFIGURATION COMPLETE")
    logger.info("="*70)
    logger.info("\n📊 Configuration Summary:")
    logger.info(f"   • Connection: Starlink (with failover)")
    logger.info(f"   • Power Mode: {power_status['current_mode']}")
    logger.info(f"   • Battery Runtime: {actual_runtime:.1f} hours")
    logger.info(f"   • Bandwidth: {optimization['profile']} profile")
    logger.info(f"   • Critical Services: Prioritized")
    logger.info(f"   • Failover: Enabled")
    logger.info(f"   • Health Status: {diag_results['overall_health']}")
    
    logger.info("\n🎯 Optimizations Applied:")
    logger.info("   ✅ Extended battery life for power outages")
    logger.info("   ✅ Censorship bypass via Starlink")
    logger.info("   ✅ Critical communications prioritized")
    logger.info("   ✅ Automatic failover to backup connections")
    logger.info("   ✅ Continuous monitoring and alerts")
    
    logger.info("\n💡 Recommendations:")
    recommendations = bandwidth_optimizer.get_recommendations()
    power_recommendations = power_manager.get_power_recommendations()
    troubleshooting = diagnostics.get_troubleshooting_steps()
    
    all_recommendations = recommendations + power_recommendations
    if all_recommendations:
        for rec in all_recommendations:
            logger.info(f"   • {rec}")
    else:
        logger.info("   • Configuration is optimal")
    
    logger.info("\n" + "="*70)
    
    return {
        'connection_manager': connection_manager,
        'power_manager': power_manager,
        'bandwidth_optimizer': bandwidth_optimizer,
        'failover_handler': failover_handler,
        'monitor': monitor,
        'diagnostics': diagnostics
    }


def simulate_power_outage(components: dict, duration_seconds: int = 60):
    """
    Simulate a power outage scenario.
    
    Args:
        components: Dictionary of initialized components
        duration_seconds: Simulation duration
    """
    logger.info("\n" + "⚡"*35)
    logger.info("SIMULATING POWER OUTAGE")
    logger.info("⚡"*35)
    
    monitor = components['monitor']
    power_manager = components['power_manager']
    failover_handler = components['failover_handler']
    
    battery_capacity = 500  # Wh
    battery_remaining = battery_capacity
    
    logger.info(f"\n🔋 Starting on battery power")
    logger.info(f"   Initial charge: {battery_capacity}Wh\n")
    
    start_time = time.time()
    update_interval = 15  # seconds
    
    while time.time() - start_time < duration_seconds:
        elapsed = time.time() - start_time
        
        # Update battery
        power_status = power_manager.get_power_status()
        power_consumed = (power_status['current_power_watts'] * update_interval) / 3600
        battery_remaining -= power_consumed
        battery_percent = (battery_remaining / battery_capacity) * 100
        
        # Get metrics
        metrics = monitor.get_current_metrics()
        alerts = monitor.check_alerts()
        
        logger.info(f"[T+{int(elapsed)}s] Status:")
        logger.info(f"  🔋 Battery: {battery_percent:.1f}% ({battery_remaining:.1f}Wh)")
        logger.info(f"  ⚡ Power: {power_status['current_power_watts']}W")
        logger.info(f"  📡 Signal: {metrics['signal_quality']}%")
        logger.info(f"  🛰️  Sats: {metrics['satellites_visible']}")
        logger.info(f"  📶 Speed: ⬇️{metrics['download_mbps']:.1f} ⬆️{metrics['upload_mbps']:.1f} Mbps")
        
        if alerts:
            logger.warning(f"  ⚠️  Alerts: {len(alerts)}")
        
        # Check failover status
        failover_result = failover_handler.monitor_and_failover()
        if failover_result['action_taken']:
            logger.warning(f"  🔄 Failover action: {failover_result['action_taken']}")
        
        logger.info("")
        time.sleep(update_interval)
    
    runtime_achieved = duration_seconds / 3600
    logger.info(f"\n✅ Power outage simulation complete")
    logger.info(f"   Runtime achieved: {runtime_achieved:.2f} hours")
    logger.info(f"   Battery remaining: {battery_percent:.1f}%")


def main():
    """Main entry point."""
    logger.info("\n" + "🇻🇪 "*20)
    logger.info("Venezuela Scenario - Starlink Connectivity Optimization")
    logger.info("🇻🇪 "*20 + "\n")
    
    try:
        # Setup scenario
        components = setup_venezuela_scenario()
        
        # Check for simulation flag
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--simulate-outage', action='store_true',
                          help='Simulate power outage scenario')
        parser.add_argument('--duration', type=int, default=60,
                          help='Simulation duration in seconds (default: 60)')
        args = parser.parse_args()
        
        if args.simulate_outage:
            time.sleep(2)  # Pause before simulation
            simulate_power_outage(components, args.duration)
        
        logger.info("\n✅ Venezuela scenario example completed successfully\n")
        
    except KeyboardInterrupt:
        logger.info("\n\nScenario interrupted by user")
    except Exception as e:
        logger.error(f"\nError in scenario: {e}")
        raise


if __name__ == "__main__":
    main()
