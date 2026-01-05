"""
Low Power Operation Example

This example demonstrates how to optimize satellite connectivity equipment
for extended battery life in remote or off-grid locations.

Scenario: Operating a satellite terminal in a remote location with limited
battery capacity, needing to maintain connectivity for 24+ hours.
"""

import sys
import time
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.power_manager import PowerManager, PowerMode

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def demonstrate_low_power_operation():
    """
    Demonstrate low power operation for 24-hour battery life
    """
    print("=" * 60)
    print("LOW POWER OPERATION EXAMPLE")
    print("Optimizing for 24-hour battery life")
    print("=" * 60)
    
    # Initialize power manager with typical battery capacity
    # Typical satellite terminal battery: 500 Wh
    power_manager = PowerManager(total_battery_capacity=500.0)
    
    print("\n1. INITIAL POWER STATUS")
    print("-" * 40)
    report = power_manager.get_power_report()
    print(f"Battery capacity: {report['battery_capacity_wh']:.1f} Wh")
    print(f"Battery level: {report['battery_percent']:.1f}%")
    print(f"Current power mode: {report['power_mode']}")
    print(f"Total power consumption: {report['total_power_consumption_w']:.1f} W")
    print(f"Estimated runtime: {report['estimated_runtime_hours']:.1f} hours")
    
    print("\n2. COMPONENT POWER BREAKDOWN")
    print("-" * 40)
    for component, info in report['components'].items():
        status = "ACTIVE" if info['is_active'] else "SLEEP"
        print(f"{component:20s}: {info['current_power_w']:5.1f} W [{status}]")
    
    # Optimize for 24-hour battery life
    print("\n3. OPTIMIZING FOR 24-HOUR BATTERY LIFE")
    print("-" * 40)
    print("Calling: power_manager.optimize_for_battery_life(target_runtime_hours=24)")
    
    power_manager.optimize_for_battery_life(target_runtime_hours=24)
    
    # Show updated status
    print("\n4. OPTIMIZED POWER STATUS")
    print("-" * 40)
    report = power_manager.get_power_report()
    print(f"New power mode: {report['power_mode']}")
    print(f"Total power consumption: {report['total_power_consumption_w']:.1f} W")
    print(f"Estimated runtime: {report['estimated_runtime_hours']:.1f} hours")
    print(f"Power reduction: {103.0 - report['total_power_consumption_w']:.1f} W saved")
    
    print("\n5. OPTIMIZED COMPONENT POWER")
    print("-" * 40)
    for component, info in report['components'].items():
        status = "ACTIVE" if info['is_active'] else "SLEEP"
        print(f"{component:20s}: {info['current_power_w']:5.1f} W [{status}]")
    
    # Demonstrate different scenarios
    print("\n6. TESTING DIFFERENT TARGET RUNTIMES")
    print("-" * 40)
    
    scenarios = [12, 24, 48, 72]
    for target_hours in scenarios:
        # Reset to normal mode
        power_manager = PowerManager(total_battery_capacity=500.0)
        power_manager.optimize_for_battery_life(target_runtime_hours=target_hours)
        
        report = power_manager.get_power_report()
        print(f"Target: {target_hours:3d}h -> "
              f"Mode: {report['power_mode']:12s} | "
              f"Power: {report['total_power_consumption_w']:5.1f}W | "
              f"Runtime: {report['estimated_runtime_hours']:5.1f}h")
    
    # Demonstrate manual power mode control
    print("\n7. MANUAL POWER MODE CONTROL")
    print("-" * 40)
    
    power_manager = PowerManager(total_battery_capacity=500.0)
    
    for mode in [PowerMode.NORMAL, PowerMode.CONSERVATION, 
                 PowerMode.CRISIS, PowerMode.SURVIVAL]:
        power_manager.set_power_mode(mode)
        report = power_manager.get_power_report()
        print(f"Mode: {mode.value:12s} | "
              f"Power: {report['total_power_consumption_w']:5.1f}W | "
              f"Runtime: {report['estimated_runtime_hours']:5.1f}h")
    
    # Demonstrate component management
    print("\n8. COMPONENT MANAGEMENT FOR POWER SAVINGS")
    print("-" * 40)
    
    power_manager = PowerManager(total_battery_capacity=500.0)
    power_manager.set_power_mode(PowerMode.CONSERVATION)
    
    print("Current active components:")
    report = power_manager.get_power_report()
    print(f"  Active: {', '.join(report['active_components'])}")
    print(f"  Power: {report['total_power_consumption_w']:.1f}W")
    
    # Disable non-essential components
    print("\nDisabling non-essential components (cellular_modem, compute_unit)...")
    power_manager.disable_component('cellular_modem')
    power_manager.disable_component('compute_unit')
    
    report = power_manager.get_power_report()
    print(f"  Active: {', '.join(report['active_components'])}")
    print(f"  Power: {report['total_power_consumption_w']:.1f}W")
    print(f"  Runtime: {report['estimated_runtime_hours']:.1f}h")
    
    # Demonstrate scheduled sleep cycles
    print("\n9. SCHEDULED SLEEP CYCLES")
    print("-" * 40)
    print("For extreme power conservation, schedule sleep/wake cycles:")
    print("  Example: Active for 5 minutes, sleep for 30 minutes")
    print("  This can extend battery life by 5-6x")
    
    power_manager = PowerManager(total_battery_capacity=500.0)
    power_manager.set_power_mode(PowerMode.CONSERVATION)
    
    # Note: We're not actually running the sleep cycle in this demo
    # as it would require waiting. Just showing the API.
    print("\nCode example:")
    print("  power_manager.schedule_sleep_cycle(")
    print("      active_duration=300,   # 5 minutes active")
    print("      sleep_duration=1800    # 30 minutes sleep")
    print("  )")
    
    # Calculate theoretical runtime with sleep cycles
    active_power = power_manager.get_total_power_consumption()
    power_manager.set_power_mode(PowerMode.SURVIVAL)
    sleep_power = power_manager.get_total_power_consumption()
    
    # 5 min active, 30 min sleep = 35 min cycle
    # Average power = (5*active + 30*sleep) / 35
    avg_power = (5 * active_power + 30 * sleep_power) / 35
    theoretical_runtime = 500.0 / avg_power
    
    print(f"\n  Active power: {active_power:.1f}W")
    print(f"  Sleep power: {sleep_power:.1f}W")
    print(f"  Average power with cycles: {avg_power:.1f}W")
    print(f"  Theoretical runtime: {theoretical_runtime:.1f}h")
    
    print("\n" + "=" * 60)
    print("LOW POWER OPERATION DEMONSTRATION COMPLETE")
    print("=" * 60)


def main():
    """Main execution"""
    try:
        demonstrate_low_power_operation()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        logger.error(f"Demo error: {e}", exc_info=True)
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
