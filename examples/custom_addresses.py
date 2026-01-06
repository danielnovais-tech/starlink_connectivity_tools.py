#!/usr/bin/env python3
"""
Custom addresses example

This example demonstrates how to use the StarlinkClient
with custom gRPC addresses (useful for non-standard setups).
"""
import sys
import os
import json

# Add parent directory to path to import starlink_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlink_client import StarlinkClient

def main():
    # Initialize client with custom addresses
    # Replace these with your actual addresses if different
    custom_router_addr = "192.168.1.1:9000"
    custom_dish_addr = "192.168.100.1:9200"
    
    client = StarlinkClient(
        router_addr=custom_router_addr,
        dish_addr=custom_dish_addr
    )
    
    print("Starlink Client with Custom Addresses")
    print("=" * 60)
    print(f"Router: {custom_router_addr}")
    print(f"Dish: {custom_dish_addr}")
    print("=" * 60)
    
    # Get status from both devices
    print("\nRetrieving status...")
    status = client.get_status(target="both")
    
    print("\nStatus Results:")
    print(json.dumps(status, indent=2))
    
    return status

if __name__ == "__main__":
    result = main()
