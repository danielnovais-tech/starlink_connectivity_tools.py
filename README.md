# Starlink Connectivity Tools

A comprehensive Python library for interacting with Starlink user terminals. This library provides wrappers for various Starlink gRPC methods, enabling device management, network monitoring, and configuration.

## Features

### Available Methods

✅ **Get Status/History** - Retrieve current status (connectivity, alerts) and historical data  
✅ **Get Network Stats** - Download/upload speeds, latency, packet loss  
✅ **Get Telemetry** - Device alerts, errors, warnings (streaming supported)  
✅ **Reboot Dish** - Restart the user terminal  
✅ **Set Dish Config** - Enable/disable features like snow melt mode, power saving  
✅ **Get Device Location** - Precise location (local) or H3 cell (remote)  
✅ **Get WiFi Status** - SSID, connected clients  
✅ **Change WiFi Config** - Modify SSID, passwords, enable bypass mode  
✅ **Get Account Data** - Basic account info (remote only)

### Key Features

- 🔌 Support for both local (gRPC) and remote (API) connections
- 📊 Type-safe data models with validation
- 🔄 Async support for telemetry streaming
- 🛡️ Comprehensive error handling
- 📖 Extensive documentation and examples
- 🧪 Easy to test and integrate

## Installation

```bash
pip install starlink-connectivity-tools
```

Or install from source:

```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
pip install -e .
```

## Quick Start

### Basic Usage

```python
from starlink_connectivity_tools import StarlinkClient

# Connect to local Starlink device
with StarlinkClient() as client:
    # Get device status
    status = client.get_status()
    print(f"Device is {status.state.value}")
    print(f"Uptime: {status.uptime_seconds // 3600} hours")
    
    # Get network statistics
    stats = client.get_network_stats()
    print(f"Download: {stats.download_mbps} Mbps")
    print(f"Latency: {stats.latency_ms} ms")
```

### Network Monitoring

```python
from starlink_connectivity_tools import StarlinkClient

with StarlinkClient() as client:
    stats = client.get_network_stats()
    
    if stats.is_healthy():
        print("✓ Network performance is good")
    else:
        print(f"⚠ High latency: {stats.latency_ms}ms")
        print(f"⚠ Packet loss: {stats.packet_loss_percent}%")
```

### WiFi Management

```python
from starlink_connectivity_tools import StarlinkClient, WiFiConfig

with StarlinkClient() as client:
    # Get current WiFi status
    wifi = client.get_wifi_status()
    print(f"SSID: {wifi.ssid}")
    print(f"Connected clients: {wifi.client_count()}")
    
    # Update WiFi configuration
    config = WiFiConfig(
        ssid="MyStarlink",
        password="SecurePassword123"
    )
    client.set_wifi_config(config)
```

### Dish Configuration

```python
from starlink_connectivity_tools import StarlinkClient, DishConfig

with StarlinkClient() as client:
    # Enable snow melt mode
    config = DishConfig(snow_melt_mode_enabled=True)
    client.set_dish_config(config)
    
    # Enable power saving
    config = DishConfig(power_save_mode_enabled=True)
    client.set_dish_config(config)
```

### Device Telemetry

```python
from starlink_connectivity_tools import StarlinkClient, AlertLevel

with StarlinkClient() as client:
    telemetry = client.get_telemetry()
    
    print(f"Temperature: {telemetry.temperature_celsius}°C")
    print(f"Power: {telemetry.power_input_watts}W")
    
    # Check for critical alerts
    if telemetry.has_critical_alerts():
        for alert in telemetry.get_alerts_by_level(AlertLevel.CRITICAL):
            print(f"CRITICAL: {alert.message}")
```

### Async Telemetry Streaming

```python
import asyncio
from starlink_connectivity_tools import StarlinkClient

async def monitor_telemetry():
    client = StarlinkClient()
    client.connect()
    
    try:
        async for telemetry in client.stream_telemetry():
            print(f"Temp: {telemetry.temperature_celsius}°C")
            
            if telemetry.has_critical_alerts():
                break
    finally:
        client.disconnect()

asyncio.run(monitor_telemetry())
```

### Remote API (Account Data)

```python
from starlink_connectivity_tools import StarlinkClient

# Remote API requires API key
with StarlinkClient(use_remote=True, api_key="your-api-key") as client:
    account = client.get_account_data()
    
    print(f"Service Line: {account.service_line_number}")
    print(f"Data Used: {account.data_used_gb} GB")
    
    if account.is_near_limit():
        print("⚠ Warning: Approaching data limit")
```

### Historical Data

```python
from starlink_connectivity_tools import StarlinkClient

with StarlinkClient() as client:
    # Get last 24 hours at 15-minute intervals
    history = client.get_history(duration_hours=24, interval_minutes=15)
    
    for entry in history:
        if entry.network_stats:
            print(f"{entry.timestamp}: {entry.network_stats.latency_ms}ms")
```

## API Reference

### StarlinkClient

Main client class for interacting with Starlink devices.

**Constructor:**
```python
StarlinkClient(
    host: str = "192.168.100.1",
    port: int = 9200,
    use_remote: bool = False,
    api_key: Optional[str] = None,
    timeout: int = 10
)
```

**Methods:**

- `connect()` - Establish connection to device
- `disconnect()` - Close connection
- `get_status()` - Get current device status
- `get_history(duration_hours, interval_minutes)` - Get historical data
- `get_network_stats()` - Get network performance stats
- `get_telemetry()` - Get device telemetry
- `stream_telemetry()` - Stream telemetry (async)
- `reboot_dish()` - Reboot the user terminal
- `set_dish_config(config)` - Configure dish settings
- `get_dish_config()` - Get current dish configuration
- `get_device_location()` - Get device location
- `get_wifi_status()` - Get WiFi status
- `set_wifi_config(config)` - Update WiFi settings
- `get_account_data()` - Get account info (remote only)

### Data Models

#### DeviceStatus
- `state` - Device operational state
- `uptime_seconds` - Device uptime
- `connected` - Connection status
- `alerts` - List of alerts
- `hardware_version` - Hardware version
- `software_version` - Software version

#### NetworkStats
- `download_mbps` - Download speed
- `upload_mbps` - Upload speed
- `latency_ms` - Latency in milliseconds
- `packet_loss_percent` - Packet loss percentage
- `is_healthy(max_latency_ms, max_packet_loss)` - Check if performance is good

#### TelemetryData
- `alerts` - List of alerts
- `temperature_celsius` - Device temperature
- `power_input_watts` - Power consumption
- `errors` - List of errors
- `warnings` - List of warnings
- `has_critical_alerts()` - Check for critical alerts
- `get_alerts_by_level(level)` - Filter alerts by severity

#### WiFiStatus
- `ssid` - Network name
- `enabled` - WiFi enabled status
- `connected_clients` - List of connected devices
- `client_count()` - Number of connected clients

#### WiFiConfig
- `ssid` - Network name to set
- `password` - Network password
- `bypass_mode_enabled` - Bypass mode setting
- `validate_ssid()` - Validate SSID
- `validate_password()` - Validate password

#### DishConfig
- `snow_melt_mode_enabled` - Snow melt mode
- `power_save_mode_enabled` - Power save mode
- `is_power_saving()` - Check if power saving is active

## Examples

See [examples.py](examples.py) for comprehensive usage examples including:
- Basic status monitoring
- Network performance tracking
- WiFi management
- Dish configuration
- Telemetry streaming
- Remote API usage
- Historical data retrieval

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black starlink_connectivity_tools/
ruff check starlink_connectivity_tools/
```

## Requirements

- Python 3.8+
- grpcio >= 1.50.0

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Inspired by:
- [starlink-client](https://github.com/sparky8512/starlink-grpc-tools) - Multi-language Starlink client libraries
- [starlink-grpc-tools](https://github.com/sparky8512/starlink-grpc-tools) - Scripts and tools for Starlink gRPC

## Support

For issues and questions, please use the [GitHub Issues](https://github.com/danielnovais-tech/starlink_connectivity_tools.py/issues) page.