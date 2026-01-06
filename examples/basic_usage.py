"""
Example usage of the Starlink Connectivity Tools library.

This file demonstrates various ways to use the library to interact
with your Starlink dish.
"""

from starlink_connectivity_tools import StarlinkClient


def main():
    """Main example function."""
    
    print("=" * 60)
    print("Starlink Connectivity Tools - Example Usage")
    print("=" * 60)
    print()
    
    # Example 1: Basic connection and status
    print("Example 1: Getting status")
    print("-" * 60)
    client = StarlinkClient()
    status = client.get_status()
    print(f"Connected: {status['is_connected']}")
    print(f"State: {status['state']}")
    print(f"Uptime: {status['uptime']} seconds")
    print(f"Software Version: {status['software_version']}")
    print(f"Active Alerts: {len(status['alerts'])}")
    print()
    
    # Example 2: Network statistics
    print("Example 2: Network Statistics")
    print("-" * 60)
    stats = client.get_network_stats()
    print(f"Download Speed: {stats['download_speed_mbps']:.2f} Mbps")
    print(f"Upload Speed: {stats['upload_speed_mbps']:.2f} Mbps")
    print(f"Latency: {stats['latency_ms']:.2f} ms")
    print(f"Packet Loss: {stats['packet_loss_percent']:.2f}%")
    print(f"Network Uptime: {stats['uptime_seconds']} seconds")
    print()
    
    # Example 3: Historical data
    print("Example 3: Historical Data")
    print("-" * 60)
    history = client.get_history(samples=100)
    print(f"Retrieved {len(history['timestamps'])} historical samples")
    print(f"Data points: timestamps, download, upload, latency, packet_loss, obstructed")
    print()
    
    # Example 4: WiFi status
    print("Example 4: WiFi Status")
    print("-" * 60)
    wifi = client.get_wifi_status()
    print(f"SSID: {wifi['ssid']}")
    print(f"Enabled: {wifi['enabled']}")
    print(f"Channel: {wifi['channel']}")
    print(f"Connected Clients: {len(wifi['connected_clients'])}")
    print(f"Signal Strength: {wifi['signal_strength']} dBm")
    print()
    
    # Example 5: Device telemetry
    print("Example 5: Device Telemetry")
    print("-" * 60)
    telemetry = client.get_telemetry()
    print(f"Active Alerts: {len(telemetry['alerts'])}")
    print(f"Errors: {len(telemetry['errors'])}")
    print(f"Warnings: {len(telemetry['warnings'])}")
    print(f"Temperature: {telemetry['temperature_celsius']:.1f}°C")
    print(f"Power Usage: {telemetry['power_usage_watts']:.1f}W")
    print()
    
    # Example 6: Device location
    print("Example 6: Device Location")
    print("-" * 60)
    location = client.get_device_location(remote=False)
    print(f"Latitude: {location.get('latitude', 'N/A')}")
    print(f"Longitude: {location.get('longitude', 'N/A')}")
    print(f"Altitude: {location.get('altitude', 'N/A')} meters")
    print()
    
    # Example 7: Using context manager
    print("Example 7: Using Context Manager")
    print("-" * 60)
    with StarlinkClient() as ctx_client:
        status = ctx_client.get_status()
        print(f"Connection state: {status['state']}")
    print("Connection automatically closed")
    print()
    
    # Example 8: Configuration (commented out for safety)
    print("Example 8: Configuration Examples (not executed)")
    print("-" * 60)
    print("# To change dish config:")
    print("# result = client.set_dish_config(snow_melt_mode=True)")
    print()
    print("# To change WiFi config:")
    print("# result = client.change_wifi_config(ssid='MyNewSSID', password='newpass123')")
    print()
    print("# To reboot dish:")
    print("# result = client.reboot_dish()")
    print()
    
    # Example 9: Remote connection (commented out - requires auth)
    print("Example 9: Remote Connection (requires authentication)")
    print("-" * 60)
    print("# For remote connections:")
    print("# remote_client = StarlinkClient(")
    print("#     target='remote.starlink.com:9200',")
    print("#     auth_token='your-auth-token'")
    print("# )")
    print("# account = remote_client.get_account_data()")
    print()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
#!/usr/bin/env python3
"""
Basic example demonstrating how to use the Starlink Space Safety API
to submit ephemeris data and screen for conjunctions.
"""

from starlink_connectivity_tools import SpaceSafetyAPI
import os


def main():
    # Get API key from environment variable or use None for unauthenticated requests
    api_key = os.getenv('STARLINK_API_KEY')
    
    # Initialize the API client
    print("Initializing Starlink Space Safety API client...")
    api = SpaceSafetyAPI(api_key=api_key)
    
    # Example 1: Submit ephemeris data
    print("\n=== Example 1: Submitting Ephemeris Data ===")
    ephemeris_data = {
        "satellite_id": "EXAMPLE-SAT-001",
        "epoch": "2026-01-05T12:00:00Z",
        "state_vector": {
            "position": [7000.0, 0.0, 0.0],  # km - circular orbit at ~620 km altitude
            "velocity": [0.0, 7.546, 0.0]    # km/s
        },
        "metadata": {
            "operator": "Example Space Agency",
            "mass": 500.0,  # kg
            "cross_sectional_area": 10.0  # m^2
        }
    }
    
    try:
        response = api.submit_ephemeris(ephemeris_data)
        print(f"✓ Ephemeris submitted successfully")
        print(f"  Submission ID: {response.get('submission_id', 'N/A')}")
    except Exception as e:
        print(f"✗ Error submitting ephemeris: {e}")
    
    # Example 2: Screen for conjunctions
    print("\n=== Example 2: Screening for Conjunctions ===")
    try:
        results = api.screen_conjunction("EXAMPLE-SAT-001")
        total_events = results.get('total_events', 0)
        print(f"✓ Screening completed")
        print(f"  Total potential conjunctions found: {total_events}")
        
        if total_events > 0:
            conjunctions = results.get('conjunctions', [])
            print(f"\n  Top 5 closest approaches:")
            for i, conj in enumerate(conjunctions[:5], 1):
                print(f"    {i}. Starlink satellite: {conj.get('starlink_satellite_id')}")
                print(f"       TCA: {conj.get('time_of_closest_approach')}")
                print(f"       Miss distance: {conj.get('miss_distance', 'N/A')} km")
                print(f"       PoC: {conj.get('probability_of_collision', 'N/A')}")
    except Exception as e:
        print(f"✗ Error screening for conjunctions: {e}")
    
    # Example 3: Get constellation data
    print("\n=== Example 3: Retrieving Constellation Data ===")
    try:
        constellation = api.get_starlink_constellation_data(
            filters={"active_only": True}
        )
        print(f"✓ Constellation data retrieved")
        print(f"  Total active Starlink satellites: {len(constellation)}")
    except Exception as e:
        print(f"✗ Error retrieving constellation data: {e}")
    
    # Clean up
    api.close()
    print("\n✓ Session closed")
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
