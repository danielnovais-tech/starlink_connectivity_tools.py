#!/usr/bin/env python3
"""
Diagnostics monitoring example

This example demonstrates how to retrieve and monitor
diagnostics information from Starlink devices.
"""
import sys
import os
import json
import time

# Add parent directory to path to import starlink_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlink_client import StarlinkClient

def print_diagnostics(diagnostics):
    """Pretty print diagnostics information"""
    print(json.dumps(diagnostics, indent=2))

def main():
    # Initialize the client
    client = StarlinkClient()
    
    print("Fetching diagnostics from Starlink devices...")
    print("=" * 60)
    
    # Get diagnostics from both devices
    diagnostics = client.get_diagnostics(target="both")
    
    # Display router diagnostics
    if "router" in diagnostics:
        print("\n📡 ROUTER DIAGNOSTICS:")
        print("-" * 60)
        if "error" in diagnostics["router"]:
            print(f"Error: {diagnostics['router']['error']}")
        else:
            print_diagnostics(diagnostics["router"])
    
    # Display dish diagnostics
    if "dish" in diagnostics:
        print("\n🛰️  DISH DIAGNOSTICS:")
        print("-" * 60)
        if "error" in diagnostics["dish"]:
            print(f"Error: {diagnostics['dish']['error']}")
        else:
            print_diagnostics(diagnostics["dish"])
    
    return diagnostics

if __name__ == "__main__":
    result = main()
