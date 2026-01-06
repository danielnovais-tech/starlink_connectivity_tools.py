#!/usr/bin/env python3
"""Power outage and network congestion simulation."""

import time
import random
from datetime import datetime

from starlink_connectivity_tools import (
    SatelliteConnectionManager,
    CrisisMonitor,
    DiagnosticsEngine,
)
from starlink_connectivity_tools.satellite_connection_manager import ConnectionType
from starlink_connectivity_tools.crisis_monitor import ScenarioType


def simulate_power_and_network_challenges():
    """
    Simulate challenges common in crisis scenarios:
    - Power outages requiring rapid reconnection
    - Network congestion during peak usage
    - Multiple simultaneous issues
    - Recovery testing
    """
    print("=" * 70)
    print("Power Outage & Network Congestion Simulation")
    print("=" * 70)
    print("\nScenario: Disaster response coordination center")
    print("Challenges:")
    print("  • Intermittent power supply")
    print("  • Network congestion during crisis")
    print("  • Multiple teams competing for bandwidth")
    print("  • Equipment failures")
    print("\n" + "=" * 70 + "\n")

    # Setup
    manager = SatelliteConnectionManager()
    
    manager.add_connection(
        "Starlink Primary",
        ConnectionType.STARLINK,
        priority=100,
        simulation_mode=True
    )
    
    manager.add_connection(
        "Starlink Secondary",
        ConnectionType.STARLINK,
        priority=90,
        simulation_mode=True
    )
    
    manager.add_connection(
        "Iridium Fallback",
        ConnectionType.IRIDIUM,
        priority=50
    )

    monitor = CrisisMonitor(manager, scenario=ScenarioType.DISASTER)
    monitor.auto_recovery_enabled = True
    diagnostics = DiagnosticsEngine(manager)

    # Connect
    print("Establishing initial connection...")
    if not manager.connect():
        print("✗ Failed to establish connection\n")
        return

    print(f"✓ Connected via {manager.get_active_connection().name}\n")

    # Simulation
    events = [
        {"type": "power_outage", "duration": 10, "description": "Complete power loss"},
        {"type": "network_congestion", "duration": 15, "description": "Heavy network load"},
        {"type": "normal", "duration": 20, "description": "Normal operations"},
        {"type": "equipment_failure", "duration": 5, "description": "Equipment malfunction"},
        {"type": "peak_usage", "duration": 12, "description": "Peak usage period"},
    ]

    iteration = 0
    event_idx = 0

    try:
        for event in events * 2:  # Run through events twice
            iteration += 1
            print(f"\n{'='*70}")
            print(f"Event {iteration}: {event['description']}")
            print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
            print('='*70)

            if event['type'] == "power_outage":
                print("\n⚡ POWER OUTAGE DETECTED")
                print("   Simulating connection loss and recovery...")
                
                # Simulate disconnection
                active = manager.get_active_connection()
                if active:
                    active.failure_count += 5  # Force failure
                
                time.sleep(2)
                
                # Attempt recovery
                print("   Attempting to reconnect...")
                if manager.auto_recover():
                    print("   ✓ Auto-recovery successful")
                elif manager.check_and_failover():
                    print(f"   🔄 Failed over to {manager.get_active_connection().name}")
                else:
                    print("   ✗ Recovery failed - manual intervention needed")

            elif event['type'] == "network_congestion":
                print("\n🌐 NETWORK CONGESTION")
                print("   High traffic load - bandwidth limited")
                print("   Multiple teams accessing network simultaneously")

            elif event['type'] == "equipment_failure":
                print("\n🔧 EQUIPMENT FAILURE")
                print("   Hardware issue detected")
                
                # Trigger failover
                if manager.check_and_failover():
                    print(f"   🔄 Switched to {manager.get_active_connection().name}")

            elif event['type'] == "peak_usage":
                print("\n📊 PEAK USAGE PERIOD")
                print("   Maximum concurrent users")

            # Monitor health
            health = monitor.check_health()
            
            active_conn = manager.get_active_connection()
            if active_conn:
                metrics = active_conn.metrics
                print(f"\nConnection: {active_conn.name}")
                print(f"  Status: {health['status'].upper()}")
                print(f"  Latency: {metrics.get('latency_ms', 0):.1f} ms")
                print(f"  Downlink: {metrics.get('downlink_mbps', 0):.1f} Mbps")
                print(f"  Uplink: {metrics.get('uplink_mbps', 0):.1f} Mbps")
                print(f"  Failures: {active_conn.failure_count}")

            # Show issues
            if health['active_issues']:
                print(f"\n⚠ Issues ({len(health['active_issues'])}):")
                for issue in health['active_issues'][:3]:
                    print(f"  • [{issue['severity'].upper()}] {issue['description']}")
                    if issue['occurrence_count'] > 1:
                        print(f"    (occurred {issue['occurrence_count']} times)")

            # Diagnostics
            if iteration % 3 == 0:
                print("\n--- Diagnostics ---")
                diag = diagnostics.run_full_diagnostic()
                if diag['alerts']:
                    for alert in diag['alerts'][:2]:
                        print(f"  • {alert['message']}")
                else:
                    print("  ✓ No alerts")

            # Wait for event duration
            for i in range(event['duration']):
                time.sleep(1)
                # Mini health check
                if i % 5 == 0:
                    h = monitor.check_health()
                    if h['status'] == 'critical':
                        print(f"  [!] Critical status at T+{i}s")

    except KeyboardInterrupt:
        print("\n\nSimulation interrupted")

    finally:
        # Final report
        print("\n" + "=" * 70)
        print("Simulation Complete - Final Report")
        print("=" * 70)

        report = monitor.get_performance_report(hours=1)
        
        if "error" not in report:
            print(f"\nPerformance Metrics:")
            print(f"  Samples: {report['samples']}")
            print(f"  Latency: {report['latency_ms']['avg']:.1f} ms avg, {report['latency_ms']['max']:.1f} ms max")
            print(f"  Bandwidth: {report['downlink_mbps']['avg']:.1f} Mbps avg")
            print(f"\nReliability:")
            print(f"  Total issues: {report['total_issues']}")
            print(f"  Resolved: {report['resolved_issues']}")
            print(f"  Active: {report['active_issues']}")

        # Connection stats
        stats = manager.get_connection_stats()
        print(f"\nConnection Statistics:")
        for name, data in stats['connections'].items():
            print(f"  {name}:")
            print(f"    Status: {data['status']}")
            print(f"    Failures: {data['failure_count']}")

        # Export
        monitor.export_data("power_network_simulation.json", hours=1)
        diagnostics.generate_diagnostic_report("power_network_diagnostics.json")
        print(f"\n✓ Data exported")

        manager.close_all()
        print("\nSimulation ended.")


if __name__ == "__main__":
    simulate_power_and_network_challenges()
