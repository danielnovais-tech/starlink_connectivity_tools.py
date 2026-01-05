#!/usr/bin/env python3
"""
Venezuela Scenario Example

This example demonstrates using Starlink connectivity tools to monitor
internet connectivity in Venezuela, where reliable internet access can be
challenging in many regions.

The scenario simulates:
- Checking Starlink availability in Venezuelan cities
- Monitoring connection quality over time
- Analyzing connectivity statistics
- Demonstrating the impact of Starlink on connectivity in underserved areas

Usage:
    python examples/venezuela_scenario.py
"""

import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from starlink_connectivity_tools import StarlinkConnectivity, check_availability


def main():
    """Run the Venezuela connectivity scenario."""
    
    print("=" * 80)
    print("STARLINK CONNECTIVITY TOOLS - VENEZUELA SCENARIO")
    print("=" * 80)
    print()
    print("This example demonstrates monitoring Starlink connectivity in Venezuela,")
    print("where access to reliable internet is crucial for communication, education,")
    print("and economic opportunities.")
    print()
    
    # Venezuelan cities to check
    locations = [
        "Caracas, Venezuela",
        "Maracaibo, Venezuela",
        "Valencia, Venezuela",
        "Barquisimeto, Venezuela"
    ]
    
    print("Step 1: Checking Starlink Availability")
    print("-" * 80)
    
    available_locations = []
    for location in locations:
        if check_availability(location):
            available_locations.append(location)
        print()
    
    if not available_locations:
        print("Unfortunately, Starlink is not available in any of the checked locations.")
        print("Please check again later or try different locations.")
        return
    
    # Select first available location for monitoring
    selected_location = available_locations[0]
    
    print()
    print("Step 2: Monitoring Connection Quality")
    print("-" * 80)
    print(f"Selected location: {selected_location}")
    print()
    print("Monitoring connection for 30 seconds with 3-second intervals...")
    print("(In a real scenario, you might monitor for hours or days)")
    print()
    
    # Initialize connectivity monitor
    monitor = StarlinkConnectivity(location=selected_location)
    
    # Monitor connection for 30 seconds
    metrics = monitor.monitor_connection(duration_seconds=30, interval_seconds=3)
    
    # Display statistics
    print()
    print("Step 3: Analyzing Results")
    monitor.print_statistics()
    
    print()
    print("=" * 80)
    print("SCENARIO INSIGHTS")
    print("=" * 80)
    print()
    print("For Venezuela, Starlink connectivity provides:")
    print("  • Access to uncensored global internet")
    print("  • Reliable connectivity in areas with poor infrastructure")
    print("  • Low latency suitable for video calls and remote work")
    print("  • Independence from traditional ISP infrastructure")
    print()
    print("This technology can be particularly valuable in:")
    print("  • Rural and remote areas")
    print("  • Regions with unreliable traditional internet service")
    print("  • Emergency situations and disaster recovery")
    print("  • Educational institutions requiring stable connectivity")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
