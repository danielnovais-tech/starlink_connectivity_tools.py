#!/usr/bin/env python3
"""
Venezuela Crisis Scenario Example
Simulates Starlink connectivity optimization for crisis scenarios
based on real challenges faced in Venezuela.
"""

import sys
import os
import time
import json
import logging
from datetime import datetime, timedelta

# Add parent directory to path to allow imports when running directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.connection_manager import SatelliteConnectionManager
from src.bandwidth_optimizer import BandwidthOptimizer, TrafficPriority
from src.power_manager import PowerManager, PowerMode
from src.failover_handler import FailoverHandler
from src.starlink_monitor import StarlinkMonitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('venezuela_scenario.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class VenezuelaCrisisScenario:
    """
    Simulates connectivity challenges and solutions for Venezuela crisis scenario
    """
    
    def __init__(self):
        # Initialize with Venezuela-specific settings
        self.connection_manager = SatelliteConnectionManager(
            enable_starlink=True,
            starlink_host="192.168.100.1"  # Default Starlink router
        )
        
        self.bandwidth_optimizer = BandwidthOptimizer(total_bandwidth=50.0)  # Reduced for crisis
        self.power_manager = PowerManager(total_battery_capacity=300.0)  # Limited power
        self.failover_handler = FailoverHandler()
        self.starlink_monitor = StarlinkMonitor()
        
        # Venezuela-specific parameters
        self.scenario_parameters = {
            'frequent_outages': True,
            'limited_power': True,
            'high_congestion': True,
            'intermittent_connectivity': True,
            'emergency_communications_only': False
        }
        
        # Critical services for Venezuela scenario
        self.critical_services = [
            {
                'name': 'medical_supplies',
                'priority': 'critical',
                'required_bandwidth': 2.0,
                'destinations': ['hospital.org', 'redcross.org']
            },
            {
                'name': 'sos_messages',
                'priority': 'critical',
                'required_bandwidth': 0.5,
                'destinations': ['sos.venezuela', 'emergency.comms']
            },
            {
                'name': 'currency_exchange',
                'priority': 'high',
                'required_bandwidth': 1.0,
                'destinations': ['crypto.exchange', 'remittance.service']
            },
            {
                'name': 'news_information',
                'priority': 'medium',
                'required_bandwidth': 1.0,
                'destinations': ['news.venezuela', 'independent.media']
            }
        ]
        
        # Simulated crisis events
        self.crisis_events = [
            {'type': 'power_outage', 'duration': 3600, 'severity': 'high'},
            {'type': 'network_congestion', 'duration': 1800, 'severity': 'medium'},
            {'type': 'government_restriction', 'duration': 7200, 'severity': 'high'},
            {'type': 'weather_disruption', 'duration': 5400, 'severity': 'medium'},
        ]
        
        logger.info("Venezuela crisis scenario initialized")
    
    def setup_crisis_mode(self):
        """Configure all systems for crisis operations"""
        logger.warning("=== CONFIGURING FOR CRISIS MODE ===")
        
        # Enable crisis mode on all components
        self.connection_manager.enable_crisis_mode({
            'crisis_min_bandwidth': 1.0,   # Very low minimum
            'crisis_max_latency': 1500     # High tolerance
        })
        
        self.bandwidth_optimizer.enable_crisis_mode()
        
        self.power_manager.set_power_mode(PowerMode.CRISIS)
        self.power_manager.optimize_for_battery_life(target_runtime_hours=72)
        
        # Configure Starlink for crisis
        self.starlink_monitor.set_thresholds(
            min_download_speed=1.0,    # Very low threshold
            max_latency=1500,          # High tolerance
            max_packet_loss=30,        # High tolerance
            max_obstruction=15         # High tolerance
        )
        
        # Setup failover for Venezuela-specific challenges
        self._setup_venezuela_failover()
        
        logger.info("Crisis mode configuration complete")
    
    def _setup_venezuela_failover(self):
        """Setup failover connections specific to Venezuela challenges"""
        # Add local mesh network as backup
        self.failover_handler.backup_connections.append({
            'connection_id': 'local_mesh',
            'priority': 2,
            'type': 'wifi_mesh',
            'cost_per_mb': 0.0,
            'max_bandwidth': 10.0,
            'description': 'Local community mesh network'
        })
        
        # Add satellite phone as last resort
        self.failover_handler.backup_connections.append({
            'connection_id': 'sat_phone',
            'priority': 5,
            'type': 'satellite_phone',
            'cost_per_mb': 5.0,
            'max_bandwidth': 0.064,  # 64 kbps
            'description': 'Iridium satellite phone for emergency'
        })
    
    def simulate_crisis_event(self, event_type: str):
        """Simulate a specific crisis event"""
        logger.warning(f"=== SIMULATING CRISIS EVENT: {event_type.upper()} ===")
        
        if event_type == 'power_outage':
            self._simulate_power_outage()
        
        elif event_type == 'network_congestion':
            self._simulate_network_congestion()
        
        elif event_type == 'government_restriction':
            self._simulate_government_restriction()
        
        elif event_type == 'weather_disruption':
            self._simulate_weather_disruption()
        
        else:
            logger.warning(f"Unknown event type: {event_type}")
    
    def _simulate_power_outage(self):
        """Simulate power outage scenario"""
        logger.critical("POWER OUTAGE DETECTED")
        
        # Reduce power consumption
        self.power_manager.set_power_mode(PowerMode.SURVIVAL)
        self.power_manager.schedule_sleep_cycle(
            active_duration=300,    # 5 minutes active
            sleep_duration=1800     # 30 minutes sleep
        )
        
        # Prioritize critical communications only
        self.bandwidth_optimizer.optimize_for_low_bandwidth(5.0)
        
        # Send power outage alert
        self._send_emergency_alert(
            "Power outage detected. Switching to battery power. "
            "Critical communications only."
        )
    
    def _simulate_network_congestion(self):
        """Simulate network congestion (common during crises)"""
        logger.warning("NETWORK CONGESTION DETECTED")
        
        # Reduce bandwidth expectations
        self.connection_manager.minimum_viable_bandwidth = 0.5
        self.starlink_monitor.set_thresholds(min_download_speed=0.5)
        
        # Prioritize text-based communications
        self.bandwidth_optimizer.optimize_for_low_bandwidth(10.0)
        
        # Enable compression for all communications
        self._enable_data_compression()
    
    def _simulate_government_restriction(self):
        """Simulate government-imposed restrictions"""
        logger.critical("GOVERNMENT RESTRICTIONS DETECTED")
        
        # Switch to encrypted communications
        self._enable_encryption()
        
        # Use alternative DNS servers
        self._switch_to_alternative_dns()
        
        # Setup VPN/Proxy for bypass
        self._setup_bypass_mechanisms()
        
        # Alert users
        self._send_emergency_alert(
            "Government restrictions detected. "
            "Encrypted communications enabled. "
            "Using alternative routing."
        )
    
    def _simulate_weather_disruption(self):
        """Simulate weather-related disruptions"""
        logger.warning("WEATHER DISRUPTION DETECTED")
        
        # Increase obstruction tolerance
        self.starlink_monitor.set_thresholds(max_obstruction=25)
        
        # Prepare for potential dish stow
        self._prepare_for_dish_stow()
        
        # Enable weather alerts
        self._enable_weather_monitoring()
    
    def _enable_data_compression(self):
        """Enable data compression for low-bandwidth scenarios"""
        logger.info("Enabling data compression for all communications")
        # In real implementation, would configure compression proxies
    
    def _enable_encryption(self):
        """Enable end-to-end encryption"""
        logger.info("Enabling end-to-end encryption for all communications")
        # In real implementation, would setup VPN/Tor/Encrypted DNS
    
    def _switch_to_alternative_dns(self):
        """Switch to alternative DNS servers"""
        logger.info("Switching to alternative DNS: 1.1.1.1, 8.8.8.8")
    
    def _setup_bypass_mechanisms(self):
        """Setup bypass mechanisms for restrictions"""
        logger.info("Setting up VPN/Proxy bypass mechanisms")
    
    def _prepare_for_dish_stow(self):
        """Prepare Starlink dish for potential stowing"""
        logger.info("Preparing dish for potential stow due to weather")
    
    def _enable_weather_monitoring(self):
        """Enable weather monitoring integration"""
        logger.info("Integrating with weather monitoring services")
    
    def _send_emergency_alert(self, message: str):
        """Send emergency alert"""
        logger.critical(f"EMERGENCY ALERT: {message}")
        # In real implementation, would send via multiple channels
    
    def run_medical_mission(self, duration_hours: int = 6):
        """Simulate a medical aid mission"""
        logger.info(f"=== STARTING MEDICAL MISSION ({duration_hours} hours) ===")
        
        start_time = time.time()
        mission_data = {
            'patients_treated': 0,
            'medical_data_sent': 0,  # MB
            'supply_requests': 0,
            'connectivity_issues': 0
        }
        
        # Setup for medical mission
        self.bandwidth_optimizer.allocate_bandwidth(
            connection_id="medical_mission",
            destination="medical.data",
            requested_bandwidth=15.0
        )
        
        # Connect to Starlink
        logger.info("Connecting to Starlink for medical mission...")
        connected = self.connection_manager.connect("starlink_satellite")
        
        if not connected:
            logger.error("Failed to connect. Attempting failover...")
            self.failover_handler.initiate_failover("Medical mission connectivity failed")
        
        # Run mission
        while time.time() - start_time < duration_hours * 3600:
            try:
                # Simulate medical activities
                self._simulate_patient_treatment(mission_data)
                self._simulate_supply_request(mission_data)
                self._simulate_medical_data_sync(mission_data)
                
                # Check connectivity
                if not self._check_mission_connectivity():
                    mission_data['connectivity_issues'] += 1
                    self._handle_mission_connectivity_issue()
                
                # Update status every 30 minutes
                if int((time.time() - start_time) / 1800) > len(mission_data.get('status_updates', [])):
                    self._send_mission_status(mission_data)
                
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                logger.info("Medical mission interrupted")
                break
            except Exception as e:
                logger.error(f"Mission error: {e}")
                time.sleep(60)
        
        # Mission complete
        self._complete_medical_mission(mission_data)
        
        return mission_data
    
    def _simulate_patient_treatment(self, mission_data: dict):
        """Simulate patient treatment"""
        import random
        if random.random() > 0.7:  # 30% chance per minute
            mission_data['patients_treated'] += 1
            logger.info(f"Patient treated. Total: {mission_data['patients_treated']}")
    
    def _simulate_supply_request(self, mission_data: dict):
        """Simulate medical supply request"""
        import random
        if random.random() > 0.9:  # 10% chance per minute
            mission_data['supply_requests'] += 1
            logger.info(f"Supply request sent. Total: {mission_data['supply_requests']}")
    
    def _simulate_medical_data_sync(self, mission_data: dict):
        """Simulate medical data synchronization"""
        import random
        if random.random() > 0.8:  # 20% chance per minute
            data_size = random.uniform(0.1, 5.0)  # MB
            mission_data['medical_data_sent'] += data_size
            logger.info(f"Medical data sent: {data_size:.2f} MB")
    
    def _check_mission_connectivity(self) -> bool:
        """Check if mission has adequate connectivity"""
        report = self.connection_manager.get_connection_report()
        
        if 'current_metrics' in report:
            metrics = report['current_metrics']
            return (metrics['bandwidth_down'] >= 2.0 and 
                    metrics['latency'] <= 1000)
        
        return False
    
    def _handle_mission_connectivity_issue(self):
        """Handle connectivity issues during mission"""
        logger.warning("Medical mission connectivity issue detected")
        
        # Attempt recovery
        if self.connection_manager.active_connection == "starlink_satellite":
            self.connection_manager.reboot_active_connection()
        else:
            self.failover_handler.initiate_failover("Medical mission connectivity lost")
    
    def _send_mission_status(self, mission_data: dict):
        """Send mission status update"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'patients_treated': mission_data['patients_treated'],
            'medical_data_sent_mb': mission_data['medical_data_sent'],
            'supply_requests': mission_data['supply_requests'],
            'connectivity_issues': mission_data['connectivity_issues'],
            'estimated_completion': "In progress"
        }
        
        logger.info(f"Mission Status: {json.dumps(status, indent=2)}")
    
    def _complete_medical_mission(self, mission_data: dict):
        """Complete the medical mission"""
        logger.info("=== MEDICAL MISSION COMPLETE ===")
        logger.info(f"Patients Treated: {mission_data['patients_treated']}")
        logger.info(f"Medical Data Sent: {mission_data['medical_data_sent']:.2f} MB")
        logger.info(f"Supply Requests: {mission_data['supply_requests']}")
        logger.info(f"Connectivity Issues: {mission_data['connectivity_issues']}")
        
        # Send final report
        final_report = {
            'mission_type': 'medical_aid',
            'duration_hours': 6,
            'summary': mission_data,
            'connectivity_quality': self.connection_manager.get_connection_report(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save report
        with open('medical_mission_report.json', 'w') as f:
            json.dump(final_report, f, indent=2)
        
        logger.info("Mission report saved to medical_mission_report.json")
    
    def run_demonstration(self):
        """Run a complete demonstration of the Venezuela scenario"""
        print("\n" + "="*70)
        print("VENEZUELA CRISIS SCENARIO DEMONSTRATION")
        print("Starlink Connectivity Optimization for Humanitarian Operations")
        print("="*70 + "\n")
        
        # Step 1: Setup crisis mode
        print("1. Setting up crisis mode configuration...")
        self.setup_crisis_mode()
        time.sleep(2)
        
        # Step 2: Establish connectivity
        print("\n2. Establishing satellite connectivity...")
        self.connection_manager.scan_available_connections()
        connected = self.connection_manager.connect("starlink_satellite")
        
        if connected:
            print("   ✓ Connected to Starlink satellite")
        else:
            print("   ✗ Connection failed, attempting failover...")
            self.failover_handler.initiate_failover("Primary connection failed")
        
        # Step 3: Simulate crisis events
        print("\n3. Simulating crisis events...")
        for event in self.crisis_events[:2]:  # First two events
            print(f"   Simulating: {event['type'].replace('_', ' ').title()}")
            self.simulate_crisis_event(event['type'])
            time.sleep(3)
        
        # Step 4: Run medical mission
        print("\n4. Running medical aid mission (simulated)...")
        mission_data = self.run_medical_mission(duration_hours=1)  # 1 hour demo
        
        # Step 5: Generate final report
        print("\n5. Generating final scenario report...")
        
        final_report = {
            'scenario': 'venezuela_crisis',
            'timestamp': datetime.now().isoformat(),
            'mission_results': mission_data,
            'system_status': {
                'connection': self.connection_manager.get_connection_report(),
                'bandwidth': self.bandwidth_optimizer.get_bandwidth_report(),
                'power': self.power_manager.get_power_report(),
                'failover': self.failover_handler.get_failover_status()
            },
            'recommendations': [
                "Maintain battery backup for power outages",
                "Use mesh networking for local communications",
                "Prioritize medical and emergency communications",
                "Monitor weather for dish protection",
                "Regularly test failover connections"
            ]
        }
        
        # Save and display report
        with open('venezuela_scenario_report.json', 'w') as f:
            json.dump(final_report, f, indent=2)
        
        print("\n" + "="*70)
        print("DEMONSTRATION COMPLETE")
        print(f"Report saved to: venezuela_scenario_report.json")
        print("="*70)
        
        # Print summary
        print("\nSUMMARY:")
        print(f"- Patients Treated: {mission_data['patients_treated']}")
        print(f"- Data Transferred: {mission_data['medical_data_sent']:.1f} MB")
        print(f"- Connectivity Issues: {mission_data['connectivity_issues']}")
        
        return final_report


def main():
    """Main execution"""
    print("Venezuela Crisis Connectivity Scenario")
    print("This demonstrates Starlink optimization for humanitarian operations\n")
    
    scenario = VenezuelaCrisisScenario()
    
    try:
        report = scenario.run_demonstration()
        
        # Ask if user wants to see the report
        response = input("\nWould you like to view the full report? (yes/no): ").lower()
        if response == 'yes':
            import json
            print("\n" + "="*70)
            print("FINAL REPORT")
            print("="*70)
            print(json.dumps(report, indent=2))
        
        print("\nThank you for running the Venezuela crisis scenario demonstration.")
        
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
