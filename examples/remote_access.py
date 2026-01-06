#!/usr/bin/env python3
"""Example script for remote access to Starlink dish using session cookies.

This demonstrates how to:
1. Connect to Starlink dish remotely
2. Authenticate using session cookies
3. Query device information
"""

import sys
from starlink_connectivity_tools import StarlinkDishClient


def main():
    """Example remote access with session cookie."""
    print("Starlink Remote Access Example")
    print("=" * 50)
    print()
    
    # Get session cookie from command line or environment
    if len(sys.argv) < 2:
        print("Usage: python remote_access.py <session_cookie> [remote_address]")
        print()
        print("Session cookies can be extracted from your browser after logging")
        print("into the Starlink web portal. They're valid for 15 days.")
        print()
        print("Example:")
        print("  python remote_access.py 'your-session-cookie-here'")
        sys.exit(1)
    
    session_cookie = sys.argv[1]
    remote_address = sys.argv[2] if len(sys.argv) > 2 else "remote.starlink.com:9200"
    
    print(f"Remote address: {remote_address}")
    print(f"Session cookie: {session_cookie[:20]}..." if len(session_cookie) > 20 else session_cookie)
    print()
    
    try:
        # Connect with session cookie
        print("Connecting to remote Starlink dish...")
        with StarlinkDishClient(
            address=remote_address,
            session_cookie=session_cookie,
        ) as client:
            print("✓ Connected successfully!")
            print()
            
            # Discover services
            print("Discovering services...")
            try:
                services = client.discover_services()
                print(f"✓ Found {len(services)} service(s):")
                for service in services:
                    print(f"  - {service}")
                print()
            except Exception as e:
                print(f"✗ Service discovery failed: {e}")
                print()
            
            print("Remote connection successful!")
            print()
            print("Note: To query status, stats, and telemetry, you need")
            print("to load the Starlink proto files (see extract_proto.py)")
            
    except ConnectionError as e:
        print(f"✗ Connection failed: {e}")
        print()
        print("Troubleshooting:")
        print("1. Verify your session cookie is valid (15-day expiry)")
        print("2. Check the remote address")
        print("3. Ensure you have internet connectivity")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
