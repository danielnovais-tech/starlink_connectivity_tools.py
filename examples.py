"""
Example usage of the Starlink Connectivity Tools library.
"""

from starlink_connectivity_tools import (
    StarlinkClient,
    WiFiConfig,
    DishConfig,
    AlertLevel,
)
import asyncio


def basic_status_example():
    """Example: Get basic device status."""
    print("=== Basic Status Example ===")
    
    # Create client and connect to local Starlink device
    with StarlinkClient() as client:
        # Get current status
        status = client.get_status()
        print(f"Device State: {status.state.value}")
        print(f"Connected: {status.connected}")
        print(f"Uptime: {status.uptime_seconds // 3600} hours")
        print(f"Software Version: {status.software_version}")
        
        if status.is_online():
            print("✓ Device is online and connected")
        
        if status.alerts:
            print(f"\n⚠ Alerts ({len(status.alerts)}):")
            for alert in status.alerts:
                print(f"  - [{alert.level.value}] {alert.message}")


def network_stats_example():
    """Example: Monitor network performance."""
    print("\n=== Network Statistics Example ===")
    
    with StarlinkClient() as client:
        stats = client.get_network_stats()
        
        print(f"Download Speed: {stats.download_mbps:.2f} Mbps")
        print(f"Upload Speed: {stats.upload_mbps:.2f} Mbps")
        print(f"Latency: {stats.latency_ms:.2f} ms")
        print(f"Packet Loss: {stats.packet_loss_percent:.2f}%")
        
        if stats.is_healthy():
            print("✓ Network performance is good")
        else:
            print("⚠ Network performance issues detected")


def telemetry_example():
    """Example: Get device telemetry."""
    print("\n=== Telemetry Example ===")
    
    with StarlinkClient() as client:
        telemetry = client.get_telemetry()
        
        print(f"Temperature: {telemetry.temperature_celsius}°C")
        print(f"Power Usage: {telemetry.power_input_watts}W")
        
        if telemetry.has_critical_alerts():
            print("\n⚠ CRITICAL ALERTS:")
            for alert in telemetry.get_alerts_by_level(AlertLevel.CRITICAL):
                print(f"  - {alert.message}")


def wifi_management_example():
    """Example: Manage WiFi settings."""
    print("\n=== WiFi Management Example ===")
    
    with StarlinkClient() as client:
        # Get current WiFi status
        wifi = client.get_wifi_status()
        print(f"Current SSID: {wifi.ssid}")
        print(f"Connected Clients: {wifi.client_count()}")
        
        for client_device in wifi.connected_clients:
            print(f"  - {client_device.hostname or client_device.mac_address}")
            print(f"    IP: {client_device.ip_address}")
            print(f"    Signal: {client_device.signal_strength} dBm")
        
        # Update WiFi configuration
        new_config = WiFiConfig(
            ssid="MyStarlink",
            password="SecurePassword123",
        )
        
        if new_config.validate_ssid() and new_config.validate_password():
            # Uncomment to actually change WiFi settings
            # client.set_wifi_config(new_config)
            print("\n✓ WiFi configuration validated (not applied)")


def dish_config_example():
    """Example: Configure dish settings."""
    print("\n=== Dish Configuration Example ===")
    
    with StarlinkClient() as client:
        # Get current configuration
        current_config = client.get_dish_config()
        print(f"Snow Melt Mode: {current_config.snow_melt_mode_enabled}")
        print(f"Power Save Mode: {current_config.power_save_mode_enabled}")
        
        # Enable snow melt mode
        new_config = DishConfig(snow_melt_mode_enabled=True)
        
        # Uncomment to actually change dish settings
        # client.set_dish_config(new_config)
        print("\n✓ Snow melt mode would be enabled")


def location_example():
    """Example: Get device location."""
    print("\n=== Location Example ===")
    
    # Local connection provides precise coordinates
    with StarlinkClient() as client:
        location = client.get_device_location()
        
        if location.has_coordinates():
            print(f"Latitude: {location.latitude}")
            print(f"Longitude: {location.longitude}")
            print(f"Altitude: {location.altitude_meters}m")
        else:
            print(f"H3 Cell: {location.h3_cell}")


def remote_api_example():
    """Example: Use remote API for account data."""
    print("\n=== Remote API Example ===")
    
    # Remote API requires API key
    api_key = "your-api-key-here"
    
    try:
        with StarlinkClient(use_remote=True, api_key=api_key) as client:
            account = client.get_account_data()
            
            print(f"Service Line: {account.service_line_number}")
            print(f"Active Subscription: {account.active_subscription}")
            print(f"Data Used: {account.data_used_gb:.2f} GB / {account.data_limit_gb} GB")
            
            if account.is_near_limit():
                print("⚠ Warning: Approaching data limit")
    except ValueError as e:
        print(f"⚠ Remote API requires valid API key: {e}")


def history_example():
    """Example: Retrieve historical data."""
    print("\n=== Historical Data Example ===")
    
    with StarlinkClient() as client:
        # Get last 24 hours of data at 15-minute intervals
        history = client.get_history(duration_hours=24, interval_minutes=15)
        
        print(f"Retrieved {len(history)} historical data points")
        print(f"Time range: {history[-1].timestamp} to {history[0].timestamp}")


async def streaming_telemetry_example():
    """Example: Stream telemetry data (async)."""
    print("\n=== Streaming Telemetry Example ===")
    
    client = StarlinkClient()
    client.connect()
    
    try:
        # Stream telemetry for 5 updates
        count = 0
        async for telemetry in client.stream_telemetry():
            print(f"Update {count + 1}: Temp={telemetry.temperature_celsius}°C, "
                  f"Power={telemetry.power_input_watts}W")
            
            count += 1
            if count >= 5:
                break
    finally:
        client.disconnect()


def reboot_example():
    """Example: Reboot the dish."""
    print("\n=== Reboot Example ===")
    
    with StarlinkClient() as client:
        # Get confirmation before rebooting
        print("⚠ This will reboot the dish!")
        # Uncomment to actually reboot
        # if client.reboot_dish():
        #     print("✓ Reboot command sent successfully")
        print("(Reboot disabled in example)")


def main():
    """Run all examples."""
    try:
        basic_status_example()
        network_stats_example()
        telemetry_example()
        wifi_management_example()
        dish_config_example()
        location_example()
        history_example()
        remote_api_example()
        reboot_example()
        
        # Async example
        print("\nRunning async streaming example...")
        asyncio.run(streaming_telemetry_example())
        
        print("\n=== All Examples Completed ===")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Note: Examples use placeholder data. Connect to a real Starlink device for actual data.")


if __name__ == "__main__":
    main()
