#!/usr/bin/env python3
"""
Emergency Mode Example

Demonstrates how to use the Starlink Connectivity Tools emergency mode
to monitor and recover from connectivity issues in critical situations.

Usage:
    python examples/emergency_mode.py
Example: Emergency mode operation for crisis scenarios
Inspired by Venezuela connectivity challenges
"""

import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from starlink_connectivity_tools import StarlinkDish, EmergencyMode


def main():
    """Main function demonstrating emergency mode usage."""
    
    print("=" * 70)
    print("Starlink Emergency Mode Example")
    print("=" * 70)
    print()
    
    # Create a Starlink dish instance
    print("Step 1: Initializing Starlink dish connection...")
    dish = StarlinkDish(host="192.168.100.1")
    
    # Use context manager for automatic connection handling
    with dish:
        print("\nStep 2: Creating emergency mode handler...")
        emergency = EmergencyMode(dish)
        
        print("\nStep 3: Performing initial connectivity check...")
        initial_assessment = emergency.check_connectivity()
        
        if initial_assessment:
            print("\n--- Initial Assessment ---")
            print(f"Operational: {initial_assessment['operational']}")
            print(f"Obstructed: {initial_assessment['obstructed']}")
            print(f"Signal Quality: {initial_assessment['signal_quality']}")
            print(f"Latency: {initial_assessment['latency']} ms")
            print(f"Active Alerts: {len(initial_assessment['alerts'])}")
            
            if initial_assessment['alerts']:
                print("\nActive Alerts:")
                for alert in initial_assessment['alerts']:
                    print(f"  - {alert}")
        
        # Activate emergency mode if there are issues
        if initial_assessment and (
            not initial_assessment['operational'] or 
            initial_assessment['alerts'] or
            initial_assessment['obstructed']
        ):
            print("\n" + "!" * 70)
            print("! CONNECTIVITY ISSUES DETECTED - ACTIVATING EMERGENCY MODE")
            print("!" * 70)
            emergency.activate()
            
            print("\nStep 4: Attempting automatic recovery...")
            recovery_success = emergency.attempt_recovery()
            
            if recovery_success:
                print("\n✓ Recovery successful!")
            else:
                print("\n✗ Recovery unsuccessful - manual intervention required")
        else:
            print("\n✓ Connectivity appears stable - no emergency intervention needed")
        
        # Optional: Monitor connectivity for a period
        print("\nStep 5: Monitoring connectivity (30 seconds)...")
        print("(Checking every 10 seconds)")
        emergency.monitor(duration=30, interval=10)
        
        # Deactivate emergency mode if it was activated
        if emergency.emergency_active:
            emergency.deactivate()
        
        # Print summary
        print("\n")
        emergency.print_summary()
    
    print("\nExample completed. Connection to dish closed.")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExample interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError running example: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
import time
import json
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmergencyConnectivitySystem:
    """
    Complete emergency connectivity system for crisis scenarios
    """
    
    def __init__(self, config_file: str = None):
        # Import components
        from src.connection_manager import SatelliteConnectionManager
        from src.bandwidth_optimizer import BandwidthOptimizer, TrafficPriority
        from src.failover_handler import FailoverHandler
        from src.power_manager import PowerManager, PowerMode
        from src.diagnostics import ConnectivityDiagnostics
        
        # Store class references for later use
        self.PowerMode = PowerMode
        
        # Initialize components
        self.connection_manager = SatelliteConnectionManager(config_file)
        self.bandwidth_optimizer = BandwidthOptimizer(total_bandwidth=100.0)
        self.failover_handler = FailoverHandler()
        self.power_manager = PowerManager(total_battery_capacity=500.0)
        self.diagnostics = ConnectivityDiagnostics()
        
        # Emergency settings
        self.emergency_mode = False
        self.critical_services = [
            "emergency.comms",
            "medical.data",
            "sos.messages",
            "coord.central"
        ]
        
        # Status tracking
        self.operation_start = datetime.now()
        self.connection_uptime = 0
        self.data_transferred = 0  # MB
        
        logger.info("Emergency Connectivity System initialized")
    
    def enable_emergency_mode(self):
        """Enable full emergency mode"""
        logger.warning("=== ENABLING EMERGENCY MODE ===")
        
        self.emergency_mode = True
        
        # Configure all components for emergency
        self.connection_manager.enable_crisis_mode({
            'crisis_min_bandwidth': 1.0,
            'crisis_max_latency': 1000
        })
        
        self.bandwidth_optimizer.enable_crisis_mode()
        
        self.power_manager.set_power_mode(self.PowerMode.CRISIS)
        self.power_manager.optimize_for_battery_life(target_runtime_hours=48)
        
        logger.info("Emergency mode enabled across all systems")
    
    def establish_connectivity(self):
        """Establish initial connectivity with fallback options"""
        logger.info("Establishing satellite connectivity...")
        
        # Scan for available connections
        connections = self.connection_manager.scan_available_connections()
        
        if not connections:
            logger.error("No satellite connections available!")
            return False
        
        # Try to connect to best available
        connected = False
        for conn_id in connections:
            if self.connection_manager.connect(conn_id):
                connected = True
                break
        
        if not connected:
            logger.error("Failed to connect to any satellite")
            logger.info("Attempting failover to backup connections...")
            
            # Try failover
            if self.failover_handler.initiate_failover(
                reason="Satellite connection failed"
            ):
                connected = True
        
        return connected
    
    def send_emergency_message(self, 
                              message: str, 
                              priority: str = "critical") -> bool:
        """
        Send emergency message with guaranteed delivery attempt
        """
        logger.info(f"Sending emergency message: {message[:50]}...")
        
        # Allocate bandwidth for emergency message
        connection_id = f"emergency_msg_{datetime.now().timestamp()}"
        allocated = self.bandwidth_optimizer.allocate_bandwidth(
            connection_id=connection_id,
            destination="emergency.comms",
            requested_bandwidth=5.0  # 5 Mbps for emergency
        )
        
        if allocated < 1.0:
            logger.warning("Insufficient bandwidth, using minimal allocation")
        
        try:
            # Simulate message transmission
            # In real implementation, would use actual messaging protocol
            time.sleep(2)  # Simulate transmission time
            
            # Update data transferred
            message_size_mb = len(message.encode()) / (1024 * 1024)
            self.data_transferred += message_size_mb
            
            logger.info(f"Emergency message sent ({message_size_mb:.2f} MB)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send emergency message: {e}")
            return False
            
        finally:
            # Always release bandwidth
            self.bandwidth_optimizer.release_bandwidth(connection_id)
    
    def run_medical_data_sync(self, data_path: str) -> bool:
        """
        Synchronize medical data with priority bandwidth
        """
        logger.info(f"Synchronizing medical data: {data_path}")
        
        # Allocate high-priority bandwidth
        connection_id = f"medical_sync_{datetime.now().timestamp()}"
        allocated = self.bandwidth_optimizer.allocate_bandwidth(
            connection_id=connection_id,
            destination="medical.data",
            requested_bandwidth=10.0
        )
        
        if allocated < 2.0:
            logger.warning("Limited bandwidth for medical data")
        
        try:
            # Simulate data sync
            # In real implementation, would transfer actual files
            time.sleep(5)
            
            # Update data transferred
            # Simulated data size
            data_size_mb = 50.0
            self.data_transferred += data_size_mb
            
            logger.info(f"Medical data synchronized ({data_size_mb:.2f} MB)")
            return True
            
        except Exception as e:
            logger.error(f"Medical data sync failed: {e}")
            return False
            
        finally:
            self.bandwidth_optimizer.release_bandwidth(connection_id)
    
    def monitor_and_maintain(self, duration_minutes: int = 60):
        """
        Monitor and maintain connectivity for specified duration
        """
        logger.info(f"Starting monitoring for {duration_minutes} minutes")
        
        end_time = time.time() + (duration_minutes * 60)
        check_interval = 30  # seconds
        
        while time.time() < end_time:
            try:
                # Run diagnostics
                diagnostic = self.diagnostics.run_full_diagnostic()
                
                # Check connection health
                if self.connection_manager.active_connection:
                    metrics = self.connection_manager.metrics[
                        self.connection_manager.active_connection
                    ]
                    
                    healthy = self.failover_handler.check_connection_health(
                        latency=metrics.latency,
                        packet_loss=metrics.packet_loss
                    )
                    
                    if not healthy and self.failover_handler.should_failover():
                        logger.warning("Connection unhealthy, attempting failover...")
                        self.failover_handler.initiate_failover(
                            reason="Connection degraded"
                        )
                
                # Check power status
                power_report = self.power_manager.get_power_report()
                if power_report['estimated_runtime_hours'] < 12:
                    logger.warning(f"Low battery: {power_report['estimated_runtime_hours']:.1f}h")
                    self.power_manager.optimize_for_battery_life(target_runtime_hours=24)
                
                # Generate status report
                self._generate_status_report()
                
                # Sleep until next check
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logger.info("Monitoring interrupted by user")
                break
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(check_interval)
    
    def _generate_status_report(self):
        """Generate and log system status report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'emergency_mode': self.emergency_mode,
            'operation_duration_hours': (
                datetime.now() - self.operation_start
            ).total_seconds() / 3600,
            'data_transferred_mb': self.data_transferred,
            'connection': self.connection_manager.get_connection_report(),
            'bandwidth': self.bandwidth_optimizer.get_bandwidth_report(),
            'failover': self.failover_handler.get_failover_status(),
            'power': self.power_manager.get_power_report()
        }
        
        # Log summary
        logger.info("=== SYSTEM STATUS ===")
        logger.info(f"Uptime: {report['operation_duration_hours']:.1f}h")
        logger.info(f"Data transferred: {report['data_transferred_mb']:.2f} MB")
        
        if 'current_metrics' in report['connection']:
            metrics = report['connection']['current_metrics']
            logger.info(f"Bandwidth: {metrics['bandwidth_down']:.1f}/{metrics['bandwidth_up']:.1f} Mbps")
            logger.info(f"Latency: {metrics['latency']:.1f} ms")
        
        logger.info(f"Battery: {report['power']['battery_percent']:.1f}%")
        logger.info(f"Estimated runtime: {report['power']['estimated_runtime_hours']:.1f}h")
        
        return report
    
    def shutdown(self):
        """Graceful shutdown of all systems"""
        logger.info("Initiating system shutdown...")
        
        # Shutdown components in order
        self.connection_manager.shutdown()
        self.power_manager.set_power_mode(self.PowerMode.SURVIVAL)
        
        # Generate final report
        final_report = self._generate_status_report()
        
        # Save report to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f"emergency_report_{timestamp}.json", 'w') as f:
            json.dump(final_report, f, indent=2, default=str)
        
        logger.info("Emergency Connectivity System shutdown complete")


def main():
    """Main execution for emergency connectivity system"""
    print("=" * 60)
    print("EMERGENCY SATELLITE CONNECTIVITY SYSTEM")
    print("Inspired by Venezuela Crisis Scenario")
    print("=" * 60)
    
    # Initialize system
    system = EmergencyConnectivitySystem()
    
    try:
        # Enable emergency mode
        system.enable_emergency_mode()
        
        # Establish connectivity
        if not system.establish_connectivity():
            print("Failed to establish connectivity. Exiting.")
            return
        
        print("Connectivity established!")
        
        # Send emergency SOS
        print("\nSending emergency SOS message...")
        system.send_emergency_message(
            "SOS: Emergency connectivity established. "
            "Medical team requires immediate evac. "
            "Coordinates: 10.1234, -66.5678. "
            "45 injured, 3 critical. Send supplies."
        )
        
        # Sync medical data
        print("\nSynchronizing medical data...")
        system.run_medical_data_sync("/data/medical/patient_records.csv")
        
        # Monitor for 10 minutes (in demo) or longer in real scenario
        print("\nStarting system monitoring...")
        print("Press Ctrl+C to stop monitoring and shutdown")
        system.monitor_and_maintain(duration_minutes=10)
        
    except KeyboardInterrupt:
        print("\n\nShutdown requested by user")
    except Exception as e:
        print(f"\n\nSystem error: {e}")
    finally:
        # Always shutdown gracefully
        system.shutdown()
        print("\nSystem shutdown complete.")
"""
Emergency Mode Example

Demonstrates how to configure Starlink tools for emergency scenarios
with automatic failover and optimized connectivity.
"""

import sys
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.connection_manager import ConnectionManager
from src.failover_handler import FailoverHandler
from src.diagnostics import Diagnostics
from src.config.settings import Settings


def main():
    """Run emergency mode configuration."""
    print("=== Starlink Emergency Mode ===\n")

    # Initialize settings for emergency mode
    emergency_config = {
        "connection": {
            "timeout": 60,
            "retry_attempts": 5,
            "retry_delay": 3,
        },
        "failover": {
            "enabled": True,
            "auto_failover": True,
            "health_check_interval": 30,
        },
    }
    settings = Settings(custom_config=emergency_config)
    print("Emergency configuration loaded")
    print(f"Timeout: {settings.get('connection.timeout')}s")
    print(f"Retry attempts: {settings.get('connection.retry_attempts')}")
    print(f"Auto-failover: {settings.get('failover.auto_failover')}\n")

    # Set up connection manager
    connection_manager = ConnectionManager(config=settings.get_all())
    print("Connecting to Starlink...")
    if connection_manager.connect():
        print("✓ Connected successfully\n")
    else:
        print("✗ Connection failed\n")

    # Configure failover with backup connections
    failover = FailoverHandler()
    failover.enable_failover()
    failover.add_backup_connection({"type": "cellular", "priority": 1})
    failover.add_backup_connection({"type": "satellite_backup", "priority": 2})
    print("Failover configured:")
    status = failover.get_status()
    print(f"  Failover enabled: {status['failover_enabled']}")
    print(f"  Backup connections: {status['backup_count']}")
    print(f"  Current connection: {status['current_connection']}\n")

    # Run diagnostics
    diagnostics = Diagnostics()
    print("Running health check...")
    health = diagnostics.run_health_check()
    print(f"Health status: {health['status']}\n")

    print("Emergency mode is now active!")
    print("The system will automatically failover if the primary connection fails.")


if __name__ == "__main__":
    main()
