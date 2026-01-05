#!/usr/bin/env python3
"""Example script for extracting proto files from Starlink dish using server reflection.

This demonstrates how to:
1. Connect to the Starlink dish
2. Use server reflection to discover services
3. Extract proto file definitions
"""

import sys
import os
from starlink_connectivity_tools.client import StarlinkDishClient
from starlink_connectivity_tools.reflection import ProtoReflectionClient


def main():
    """Extract proto files from Starlink dish."""
    print("Starlink Proto File Extractor")
    print("=" * 50)
    print()
    
    # Parse command line arguments
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "./proto_files"
    
    print(f"Output directory: {output_dir}")
    print()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Connect to dish
        print("Connecting to Starlink dish...")
        client = StarlinkDishClient()
        client.connect()
        print("✓ Connected")
        print()
        
        # Create reflection client
        reflection_client = ProtoReflectionClient(client._channel)
        
        # List services
        print("Discovering services...")
        services = reflection_client.list_services()
        print(f"✓ Found {len(services)} service(s):")
        for service in services:
            print(f"  - {service}")
        print()
        
        # Extract proto files
        print("Extracting proto files...")
        for service in services:
            try:
                # Skip reflection service itself
                if 'reflection' in service.lower():
                    continue
                
                # Generate filename from service name
                filename = service.replace('.', '_') + '.proto'
                output_path = os.path.join(output_dir, filename)
                
                # Extract proto file
                reflection_client.export_proto_file(service, output_path)
                print(f"✓ Extracted {filename}")
                
            except Exception as e:
                print(f"✗ Failed to extract {service}: {e}")
        
        print()
        print(f"Proto files saved to: {output_dir}")
        print()
        print("Next steps:")
        print("1. Review the extracted .proto files")
        print("2. Compile them using: python -m grpc_tools.protoc ...")
        print("3. Import the compiled modules in your code")
        
        client.close()
        
    except ConnectionError as e:
        print(f"✗ Connection failed: {e}")
        print()
        print("Make sure you're connected to the Starlink network")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
