#!/usr/bin/env python3
"""
Basic usage example for Starlink Client

This example demonstrates how to get basic status information
from both the Starlink router and dish.
"""
import sys
import os

# Add parent directory to path to import starlink_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlink_client import StarlinkClient

def main():
    # Initialize the client with default addresses
    client = StarlinkClient()
    
    print("Getting device status...")
    status = client.get_status(target="both")
    
    # Check for errors
    if "error" in status.get("router", {}):
        print(f"Router error: {status['router']['error']}")
    else:
        print("Router status retrieved successfully")
    
    if "error" in status.get("dish", {}):
        print(f"Dish error: {status['dish']['error']}")
    else:
        print("Dish status retrieved successfully")
    
    return status

if __name__ == "__main__":
    result = main()
    print("\nStatus:", result)
