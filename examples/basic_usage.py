#!/usr/bin/env python3
"""Example script demonstrating basic usage of the Starlink connectivity tools.

This script shows how to:
1. Connect to a local Starlink dish
2. Discover available gRPC services
3. Query device status (requires proto files)
"""

import sys
from starlink_connectivity_tools import StarlinkDishClient


def main():
    """Main example function."""
    # Example 1: Connect to local dish
    print("Example 1: Connecting to local Starlink dish...")
    print(f"Address: {StarlinkDishClient.DEFAULT_LOCAL_ADDRESS}")
    print()
    
    try:
        with StarlinkDishClient() as client:
            print("✓ Connected successfully!")
            print()
            
            # Example 2: Discover services
            print("Example 2: Discovering available services...")
            try:
                services = client.discover_services()
                print(f"Found {len(services)} service(s):")
                for service in services:
                    print(f"  - {service}")
                print()
            except Exception as e:
                print(f"✗ Service discovery failed: {e}")
                print()
            
            # Example 3: Query status (requires proto files)
            print("Example 3: Querying device status...")
            try:
                status = client.get_status()
                print("Status:", status)
            except NotImplementedError as e:
                print(f"Note: {e}")
                print()
                print("To use status query methods, you need to:")
                print("1. Extract proto files using grpcurl or similar tools")
                print("2. Compile them with protoc")
                print("3. Import them in your code")
                print()
                
    except ConnectionError as e:
        print(f"✗ Connection failed: {e}")
        print()
        print("Troubleshooting:")
        print("1. Ensure you're connected to the Starlink network")
        print("2. Check that the dish is powered on")
        print("3. Verify the dish address (default: 192.168.100.1:9200)")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
