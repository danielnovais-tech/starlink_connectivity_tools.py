#!/usr/bin/env python3
"""
Emergency Mode Example for Starlink Connectivity Tools

This script demonstrates how to monitor a Starlink dish for emergency
conditions and take appropriate actions such as:
- Checking connectivity status
- Detecting obstructions and signal issues
- Stowing the dish during emergencies
- Monitoring thermal and mechanical issues

Usage:
    python examples/emergency_mode.py
"""

import sys
import time
from pathlib import Path

# Add parent directory to path to import the library
sys.path.insert(0, str(Path(__file__).parent.parent))

from starlink_connectivity_tools import StarlinkDish, StarlinkConnectionError, StarlinkEmergencyError


def format_bytes(bytes_value: float) -> str:
    """Format bytes per second to human-readable format."""
    if bytes_value >= 1e9:
        return f"{bytes_value / 1e9:.2f} Gbps"
    elif bytes_value >= 1e6:
        return f"{bytes_value / 1e6:.2f} Mbps"
    elif bytes_value >= 1e3:
        return f"{bytes_value / 1e3:.2f} Kbps"
    else:
        return f"{bytes_value:.2f} bps"


def print_status(status: dict):
    """Print formatted status information."""
    print("\n" + "=" * 60)
    print("STARLINK DISH STATUS")
    print("=" * 60)
    print(f"Uptime:                  {status['uptime']} seconds")
    print(f"Connected Satellites:    {status['connected_satellites']}")
    print(f"Downlink Throughput:     {format_bytes(status['downlink_throughput_bps'])}")
    print(f"Uplink Throughput:       {format_bytes(status['uplink_throughput_bps'])}")
    print(f"Ping Latency:            {status['pop_ping_latency_ms']:.2f} ms")
    print(f"Obstructed:              {'YES ⚠️' if status['obstructed'] else 'NO ✓'}")
    print(f"Obstruction Percentage:  {status['obstruction_percentage']:.2f}%")
    print(f"Stowed:                  {'YES' if status['stowed'] else 'NO'}")
    print(f"Heating:                 {'YES' if status['heating'] else 'NO'}")
    print(f"Motor Stuck:             {'YES ⚠️' if status['motor_stuck'] else 'NO ✓'}")
    print(f"Thermal Throttle:        {'YES ⚠️' if status['thermal_throttle'] else 'NO ✓'}")
    print(f"Unexpected Outages:      {status['unexpected_outages']}")
    print("=" * 60)


def handle_emergency(dish: StarlinkDish, condition: str):
    """Handle emergency conditions."""
    print(f"\n{'!' * 60}")
    print(f"⚠️  EMERGENCY CONDITION DETECTED: {condition}")
    print(f"{'!' * 60}")
    
    if condition == "MOTOR_STUCK":
        print("\n🔧 Action: Motor is stuck. Attempting to reboot dish...")
        dish.reboot()
        print("   Please check dish physically if issue persists.")
        
    elif condition == "HIGH_OBSTRUCTION":
        print("\n🌲 Action: High obstruction detected.")
        print("   Please check for obstacles blocking the dish's view of the sky.")
        print("   Consider relocating the dish to a clearer location.")
        
    elif condition == "THERMAL_THROTTLE":
        print("\n🌡️  Action: Thermal throttling detected.")
        print("   The dish is too hot and limiting performance.")
        print("   Ensure proper ventilation around the dish.")
        
    elif condition == "HIGH_LATENCY":
        print("\n🐌 Action: High latency detected.")
        print("   Network performance may be degraded.")
        print("   This could be due to weather or network congestion.")
    
    # Ask user if they want to stow the dish
    try:
        response = input("\n🛡️  Do you want to stow the dish for protection? (y/n): ").strip().lower()
        if response == 'y':
            dish.stow()
            print("\n✓ Dish has been stowed to emergency position.")
            print("  Run this script again and choose to unstow when conditions improve.")
    except (KeyboardInterrupt, EOFError):
        print("\n\nOperation cancelled by user.")


def monitor_mode(dish: StarlinkDish, duration: int = 30, interval: int = 5):
    """
    Continuously monitor the dish for emergency conditions.
    
    Args:
        dish: StarlinkDish instance
        duration: Total monitoring duration in seconds
        interval: Check interval in seconds
    """
    print(f"\n🔍 Starting emergency monitoring mode...")
    print(f"   Monitoring for {duration} seconds with {interval}-second intervals")
    print(f"   Press Ctrl+C to stop monitoring\n")
    
    start_time = time.time()
    check_count = 0
    
    try:
        while (time.time() - start_time) < duration:
            check_count += 1
            print(f"\n--- Check #{check_count} ---")
            
            # Check for emergency conditions
            emergency = dish.check_emergency_conditions()
            
            if emergency:
                handle_emergency(dish, emergency)
                break
            else:
                status = dish.get_status()
                print(f"✓ All systems normal")
                print(f"  Satellites: {status['connected_satellites']}, "
                      f"Latency: {status['pop_ping_latency_ms']:.1f}ms, "
                      f"Obstructions: {status['obstruction_percentage']:.1f}%")
            
            # Wait for next check
            if (time.time() - start_time) < duration:
                print(f"\n⏳ Waiting {interval} seconds until next check...")
                time.sleep(interval)
        
        print(f"\n✓ Monitoring completed successfully after {check_count} checks.")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Monitoring stopped by user after {check_count} checks.")


def main():
    """Main function to demonstrate emergency mode operations."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║   STARLINK CONNECTIVITY TOOLS - EMERGENCY MODE EXAMPLE       ║
╚══════════════════════════════════════════════════════════════╝

This example demonstrates emergency mode functionality:
1. Connect to Starlink dish
2. Check current status
3. Monitor for emergency conditions
4. Take protective actions when needed
""")
    
    try:
        # Use context manager for automatic connection/disconnection
        with StarlinkDish() as dish:
            # Get and display current status
            print("\n📊 Fetching current dish status...")
            status = dish.get_status()
            print_status(status)
            
            # Check if dish is already stowed
            if status['stowed']:
                print("\n⚠️  Dish is currently STOWED (emergency position)")
                response = input("Do you want to unstow the dish? (y/n): ").strip().lower()
                if response == 'y':
                    dish.unstow()
                    print("\n✓ Dish has been unstowed and returned to normal operation.")
                else:
                    print("\nDish remains in stowed position.")
                    return
            
            # Immediate emergency check
            print("\n🔍 Checking for emergency conditions...")
            emergency = dish.check_emergency_conditions()
            
            if emergency:
                handle_emergency(dish, emergency)
            else:
                print("✓ No emergency conditions detected.")
                
                # Ask if user wants to enter monitoring mode
                print("\n" + "-" * 60)
                response = input("Enter continuous monitoring mode? (y/n): ").strip().lower()
                
                if response == 'y':
                    monitor_mode(dish, duration=30, interval=5)
                else:
                    print("\nExiting emergency mode.")
            
    except StarlinkConnectionError as e:
        print(f"\n❌ Connection Error: {e}")
        print("   Make sure the Starlink dish is reachable at 192.168.100.1")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user.")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
    
    print("\n✓ Emergency mode example completed successfully.\n")


if __name__ == "__main__":
    main()
