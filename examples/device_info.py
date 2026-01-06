#!/usr/bin/env python3
"""
Device information example

This example demonstrates how to retrieve detailed
information about Starlink devices.
"""
import sys
import os
import json

# Add parent directory to path to import starlink_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlink_client import StarlinkClient

def display_device_info(info, device_name):
    """Display device information in a readable format"""
    print(f"\n{device_name.upper()} INFORMATION:")
    print("-" * 60)
    
    if "error" in info:
        print(f"❌ Error: {info['error']}")
    else:
        print(json.dumps(info, indent=2))

def main():
    # Initialize the client
    client = StarlinkClient()
    
    print("Starlink Device Information")
    print("=" * 60)
    
    # Get device info from both devices
    device_info = client.get_device_info(target="both")
    
    # Display router info
    if "router" in device_info:
        display_device_info(device_info["router"], "router")
    
    # Display dish info
    if "dish" in device_info:
        display_device_info(device_info["dish"], "dish")
    
    return device_info

if __name__ == "__main__":
    result = main()
