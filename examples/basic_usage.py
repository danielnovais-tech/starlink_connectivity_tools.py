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


if __name__ == "__main__":
    main()
