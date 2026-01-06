#!/usr/bin/env python3
"""Medical mission simulation with connectivity optimization."""

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


def simulate_medical_mission():
    """
    Simulate a medical mission scenario with critical connectivity requirements:
    - Telemedicine consultations requiring low latency
    - Medical record uploads requiring stable bandwidth
    - Emergency communication needs
    - Reliability over speed
    """
    print("=" * 70)
    print("Medical Mission Simulation")
    print("=" * 70)
    print("\nScenario: Remote medical clinic in rural area")
    print("Requirements:")
    print("  • Stable connection for telemedicine (latency < 150ms)")
    print("  • Reliable bandwidth for medical imaging transfer (>10 Mbps)")
    print("  • Redundant connections for emergency communications")
    print("  • Automatic failover to ensure continuous operation")
    print("\n" + "=" * 70 + "\n")

    # Setup connection manager
    manager = SatelliteConnectionManager()
    
    # Primary Starlink for high bandwidth
    manager.add_connection(
        "Starlink Medical Primary",
        ConnectionType.STARLINK,
        priority=100,
        simulation_mode=True
    )
    
    # Backup connections
    manager.add_connection(
        "Inmarsat Medical Backup",
        ConnectionType.INMARSAT,
        priority=75
    )
    
    manager.add_connection(
        "Thuraya Emergency",
        ConnectionType.THURAYA,
        priority=50
    )

    # Setup crisis monitor with medical scenario
    monitor = CrisisMonitor(manager, scenario=ScenarioType.MEDICAL)
    
    # Adjust thresholds for medical requirements
    monitor.set_custom_thresholds({
        "max_latency_ms": 150,  # Critical for video consultations
        "min_downlink_mbps": 10,  # For medical imaging
        "min_uplink_mbps": 5,  # For video streaming
    })
    
    monitor.auto_recovery_enabled = True
    
    # Setup diagnostics
    diagnostics = DiagnosticsEngine(manager)

    # Connect
    print("Establishing connection for medical services...")
    if manager.connect():
        print(f"✓ Connected via {manager.get_active_connection().name}\n")
    else:
        print("✗ Failed to establish connection - CRITICAL\n")
        return

    # Simulation of medical activities
    activities = [
        "Video consultation with specialist",
        "Uploading X-ray images",
        "Downloading patient medical records",
        "Emergency consultation",
        "Routine patient monitoring",
        "Training session with remote doctors",
    ]

    simulation_duration = 120  # 2 minutes
    start_time = time.time()
    activity_count = 0

    try:
        while (time.time() - start_time) < simulation_duration:
            activity_count += 1
            
            # Select random medical activity
            activity = random.choice(activities)
            print(f"\n{'='*70}")
            print(f"Medical Activity {activity_count}: {activity}")
            print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
            print('='*70)

            # Simulate activity-specific requirements
            if "Video consultation" in activity or "Emergency" in activity:
                print("📞 Critical activity - requires low latency and stable connection")
                required_latency = 150
                required_bandwidth = 5
            elif "Uploading" in activity or "X-ray" in activity:
                print("📤 Upload activity - requires high uplink bandwidth")
                required_latency = 300
                required_bandwidth = 10
            elif "Downloading" in activity:
                print("📥 Download activity - requires high downlink bandwidth")
                required_latency = 300
                required_bandwidth = 15
            else:
                print("📊 Routine activity - standard requirements")
                required_latency = 500
                required_bandwidth = 2

            # Perform health check
            health = monitor.check_health()
            
            active_conn = manager.get_active_connection()
            if active_conn:
                metrics = active_conn.metrics
                latency = metrics.get('latency_ms', 0)
                downlink = metrics.get('downlink_mbps', 0)
                uplink = metrics.get('uplink_mbps', 0)
                
                print(f"\nConnection Status: {active_conn.name}")
                print(f"  Latency: {latency:.1f} ms (required: < {required_latency} ms)")
                print(f"  Downlink: {downlink:.1f} Mbps")
                print(f"  Uplink: {uplink:.1f} Mbps")
                
                # Check if requirements are met
                if latency <= required_latency and downlink >= required_bandwidth:
                    print("✓ Connection meets requirements - proceeding")
                else:
                    print("⚠ Connection does not meet requirements")
                    if manager.check_and_failover():
                        print(f"🔄 Failed over to {manager.get_active_connection().name}")

            # Display health status
            print(f"\nOverall Health: {health['status'].upper()}")
            
            if health['active_issues']:
                print(f"Active Issues ({len(health['active_issues'])}):")
                for issue in health['active_issues'][:3]:  # Show top 3
                    print(f"  • [{issue['severity'].upper()}] {issue['description']}")
            
            # Periodic diagnostics
            if activity_count % 4 == 0:
                print("\n--- Running Diagnostics ---")
                diag = diagnostics.run_full_diagnostic()
                
                if diag['alerts']:
                    print(f"Alerts ({len(diag['alerts'])}):")
                    for alert in diag['alerts'][:2]:  # Show top 2
                        print(f"  • {alert['message']}")
                        print(f"    → {alert['recommendation']}")
                else:
                    print("✓ All systems operational")

            # Simulate activity duration
            time.sleep(random.uniform(8, 15))

    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user")

    finally:
        # Generate medical mission report
        print("\n" + "=" * 70)
        print("Medical Mission Complete - Generating Report")
        print("=" * 70)

        report = monitor.get_performance_report(hours=1)
        
        if "error" not in report:
            print(f"\nMission Performance Summary:")
            print(f"  Total activities: {activity_count}")
            print(f"  Monitoring samples: {report['samples']}")
            
            print(f"\n  Connection Quality:")
            print(f"    Latency avg: {report['latency_ms']['avg']:.1f} ms")
            print(f"    Latency P95: {report['latency_ms']['p95']:.1f} ms")
            print(f"    Bandwidth avg: {report['downlink_mbps']['avg']:.1f} Mbps")
            
            # Calculate reliability
            uptime_pct = (report['samples'] - report['active_issues']) / report['samples'] * 100
            print(f"\n  Reliability:")
            print(f"    Uptime: {uptime_pct:.1f}%")
            print(f"    Total issues: {report['total_issues']}")
            print(f"    Auto-resolved: {report['resolved_issues']}")

        # Get connection statistics
        stats = manager.get_connection_stats()
        print(f"\n  Connection Usage:")
        for conn_name, conn_stats in stats['connections'].items():
            if conn_stats.get('last_check'):
                print(f"    {conn_name}: {conn_stats['status']}")

        # Export data
        export_file = "medical_mission_data.json"
        monitor.export_data(export_file, hours=1)
        print(f"\n✓ Mission data exported to {export_file}")
        
        diag_file = "medical_mission_diagnostics.json"
        diagnostics.generate_diagnostic_report(diag_file)
        print(f"✓ Diagnostic report saved to {diag_file}")

        manager.close_all()
        print("\nMedical mission simulation ended.")


if __name__ == "__main__":
    simulate_medical_mission()
