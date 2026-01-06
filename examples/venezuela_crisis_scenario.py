#!/usr/bin/env python3
"""Venezuela crisis scenario simulation."""

import time
import random
from datetime import datetime

from starlink_connectivity_tools import (
    StarlinkAPI,
    SatelliteConnectionManager,
    CrisisMonitor,
    DiagnosticsEngine,
)
from starlink_connectivity_tools.satellite_connection_manager import ConnectionType
from starlink_connectivity_tools.crisis_monitor import ScenarioType


def simulate_venezuela_crisis():
    """
    Simulate a crisis scenario in Venezuela with realistic challenges:
    - Intermittent power outages
    - Network restrictions
    - Bandwidth throttling
    - Signal interference
    """
    print("=" * 70)
    print("Venezuela Crisis Scenario Simulation")
    print("=" * 70)
    print("\nScenario: Humanitarian aid coordination in remote area")
    print("Challenges:")
    print("  • Intermittent power supply")
    print("  • Government network restrictions")
    print("  • Limited backup connectivity")
    print("  • Environmental obstructions")
    print("\n" + "=" * 70 + "\n")

    # Setup connection manager with multiple fallback options
    manager = SatelliteConnectionManager()
    
    # Primary Starlink connection
    manager.add_connection(
        "Starlink Primary",
        ConnectionType.STARLINK,
        priority=100,
        simulation_mode=True
    )
    
    # Backup satellite connections
    manager.add_connection(
        "Iridium Backup",
        ConnectionType.IRIDIUM,
        priority=50
    )
    
    manager.add_connection(
        "Inmarsat Emergency",
        ConnectionType.INMARSAT,
        priority=25
    )

    # Setup crisis monitor with conflict scenario thresholds
    monitor = CrisisMonitor(manager, scenario=ScenarioType.CONFLICT)
    
    # Enable automatic recovery
    monitor.auto_recovery_enabled = True
    
    # Setup diagnostics
    diagnostics = DiagnosticsEngine(manager)

    # Connect
    print("Establishing initial connection...")
    if manager.connect():
        print(f"✓ Connected via {manager.get_active_connection().name}\n")
    else:
        print("✗ Failed to establish connection\n")
        return

    # Simulation loop
    simulation_duration = 120  # 2 minutes
    start_time = time.time()
    iteration = 0

    try:
        while (time.time() - start_time) < simulation_duration:
            iteration += 1
            print(f"\n--- Iteration {iteration} ({int(time.time() - start_time)}s elapsed) ---")

            # Simulate random challenges
            challenge = random.choice([
                "normal",
                "power_fluctuation",
                "network_restriction",
                "obstruction",
                "signal_degradation"
            ])

            if challenge == "power_fluctuation":
                print("⚠ CHALLENGE: Power fluctuation detected")
                print("   Impact: Temporary connection loss")
                # Simulate reconnection
                time.sleep(2)
                manager.check_and_failover()

            elif challenge == "network_restriction":
                print("⚠ CHALLENGE: Network restriction imposed")
                print("   Impact: Bandwidth throttling")
                # Monitor will detect low bandwidth

            elif challenge == "obstruction":
                print("⚠ CHALLENGE: Physical obstruction (tree branch)")
                print("   Impact: Degraded signal quality")

            elif challenge == "signal_degradation":
                print("⚠ CHALLENGE: Atmospheric interference")
                print("   Impact: Increased latency and packet loss")

            # Perform health check
            health = monitor.check_health()
            
            print(f"\nStatus: {health['status'].upper()}")
            
            active_conn = manager.get_active_connection()
            if active_conn:
                metrics = active_conn.metrics
                print(f"Connection: {active_conn.name}")
                print(f"  Latency: {metrics.get('latency_ms', 0):.1f} ms")
                print(f"  Downlink: {metrics.get('downlink_mbps', 0):.1f} Mbps")
                print(f"  Uplink: {metrics.get('uplink_mbps', 0):.1f} Mbps")

            # Display active issues
            if health['active_issues']:
                print(f"\nActive Issues ({len(health['active_issues'])}):")
                for issue in health['active_issues']:
                    print(f"  • [{issue['severity'].upper()}] {issue['description']}")
            else:
                print("\n✓ No active issues")

            # Run diagnostics periodically
            if iteration % 5 == 0:
                print("\nRunning diagnostics...")
                diag_result = diagnostics.run_full_diagnostic()
                if diag_result['alerts']:
                    print(f"Diagnostic Alerts ({len(diag_result['alerts'])}):")
                    for alert in diag_result['alerts']:
                        print(f"  • [{alert['severity'].upper()}] {alert['message']}")

            # Check for automatic failover
            if manager.check_and_failover():
                new_conn = manager.get_active_connection()
                print(f"\n🔄 FAILOVER: Switched to {new_conn.name}")

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user")

    finally:
        # Generate final report
        print("\n" + "=" * 70)
        print("Simulation Complete - Generating Report")
        print("=" * 70)

        report = monitor.get_performance_report(hours=1)
        
        if "error" not in report:
            print(f"\nPerformance Summary:")
            print(f"  Samples collected: {report['samples']}")
            print(f"\n  Latency:")
            print(f"    Average: {report['latency_ms']['avg']:.1f} ms")
            print(f"    Min: {report['latency_ms']['min']:.1f} ms")
            print(f"    Max: {report['latency_ms']['max']:.1f} ms")
            print(f"\n  Bandwidth:")
            print(f"    Downlink avg: {report['downlink_mbps']['avg']:.1f} Mbps")
            print(f"    Uplink avg: {report['uplink_mbps']['avg']:.1f} Mbps")
            print(f"\n  Issues:")
            print(f"    Total: {report['total_issues']}")
            print(f"    Resolved: {report['resolved_issues']}")
            print(f"    Active: {report['active_issues']}")

        # Export data
        export_file = "venezuela_crisis_simulation.json"
        monitor.export_data(export_file, hours=1)
        print(f"\n✓ Full data exported to {export_file}")
        
        # Generate diagnostic report
        diag_file = "venezuela_crisis_diagnostics.json"
        diagnostics.generate_diagnostic_report(diag_file)
        print(f"✓ Diagnostic report saved to {diag_file}")

        manager.close_all()
        print("\nSimulation ended.")


if __name__ == "__main__":
    simulate_venezuela_crisis()
