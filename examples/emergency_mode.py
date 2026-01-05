#!/usr/bin/env python3
"""
Emergency Mode Example

Demonstrates how to use the Starlink Connectivity Tools emergency mode
to monitor and recover from connectivity issues in critical situations.

Usage:
    python examples/emergency_mode.py
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
