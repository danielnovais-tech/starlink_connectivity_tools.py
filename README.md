# Starlink Connectivity Tools

A Python library for interacting with Starlink user terminals via gRPC. This library provides convenient wrappers for common Starlink methods to manage and monitor your Starlink dish.

## Features

This library provides methods for:

- **Get Status/History**: Retrieve current status (connectivity, alerts) and historical data
- **Get Network Stats**: Download/upload speeds, latency, packet loss
- **Get Telemetry**: Device alerts, errors, warnings (streaming supported)
- **Reboot Dish**: Restart the user terminal
- **Set Dish Config**: Enable/disable features like snow melt mode, power saving
- **Get Device Location**: Precise location (local) or H3 cell (remote)
- **Get WiFi Status**: SSID, connected clients
- **Change WiFi Config**: Modify SSID, passwords, enable bypass mode
- **Get Account Data**: Basic account info (remote only)

## Installation

### From source

```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
pip install -e .
```

### Using pip (when published to PyPI)

```bash
pip install starlink_connectivity_tools
```

## Requirements

- Python 3.7 or higher
- grpcio >= 1.50.0
- grpcio-tools >= 1.50.0

## Quick Start

### Basic Usage

```python
from starlink_connectivity_tools import StarlinkClient

# Connect to local Starlink dish (default: 192.168.100.1:9200)
client = StarlinkClient()

# Get current status
status = client.get_status()
print(f"Connected: {status['is_connected']}")
print(f"State: {status['state']}")
print(f"Uptime: {status['uptime']} seconds")

# Get network statistics
stats = client.get_network_stats()
print(f"Download: {stats['download_speed_mbps']} Mbps")
print(f"Upload: {stats['upload_speed_mbps']} Mbps")
print(f"Latency: {stats['latency_ms']} ms")
print(f"Packet Loss: {stats['packet_loss_percent']}%")

# Get WiFi status
wifi = client.get_wifi_status()
print(f"SSID: {wifi['ssid']}")
print(f"Connected Clients: {len(wifi['connected_clients'])}")
```

### Using Context Manager

```python
from starlink_connectivity_tools import StarlinkClient

# Automatically handle connection and disconnection
with StarlinkClient() as client:
    status = client.get_status()
    print(status)
```

### Remote Connection (with authentication)

```python
from starlink_connectivity_tools import StarlinkClient

# Connect remotely with authentication token
client = StarlinkClient(
    target="remote.starlink.com:9200",
    auth_token="your-auth-token"
)

# Get account data (requires authentication)
account = client.get_account_data()
print(f"Email: {account['email']}")
print(f"Service Plan: {account['service_plan']}")
```

### Explicit Secure/Insecure Connection

```python
from starlink_connectivity_tools import StarlinkClient

# Force secure channel for local connection (optional)
secure_client = StarlinkClient(
    target="192.168.100.1:9200",
    secure=True
)

# Force insecure channel for testing (not recommended for production)
insecure_client = StarlinkClient(
    target="remote.starlink.com:9200",
    secure=False  # Only for testing/development
)
```

**Note:** The library automatically detects private IP addresses (RFC 1918: 10.x.x.x, 172.16.x.x-172.31.x.x, 192.168.x.x) and uses insecure channels for them. For all other addresses or when an auth_token is provided, it uses secure SSL/TLS channels.

## Available Methods

### get_status()

Retrieve current status of the Starlink dish.

```python
status = client.get_status()
# Returns:
# {
#     "uptime": 123456,
#     "state": "CONNECTED",
#     "alerts": [],
#     "is_connected": true,
#     "software_version": "1.2.3"
# }
```

### get_history(samples=300)

Retrieve historical data from the Starlink dish.

```python
history = client.get_history(samples=100)
# Returns:
# {
#     "timestamps": [...],
#     "download_throughput": [...],
#     "upload_throughput": [...],
#     "latency": [...],
#     "packet_loss": [...],
#     "obstructed": [...]
# }
```

### get_network_stats()

Get current network statistics.

```python
stats = client.get_network_stats()
# Returns:
# {
#     "download_speed_mbps": 150.5,
#     "upload_speed_mbps": 25.3,
#     "latency_ms": 35.2,
#     "packet_loss_percent": 0.1,
#     "uptime_seconds": 123456
# }
```

### get_telemetry(streaming=False)

Retrieve device telemetry including alerts, errors, and warnings.

```python
telemetry = client.get_telemetry()
# Returns:
# {
#     "alerts": [...],
#     "errors": [...],
#     "warnings": [...],
#     "temperature_celsius": 45.2,
#     "power_usage_watts": 65.5
# }
```

### reboot_dish()

Restart the Starlink user terminal.

```python
result = client.reboot_dish()
# Returns:
# {
#     "success": true,
#     "message": "Reboot command sent"
# }
```

### set_dish_config(snow_melt_mode=None, power_save_mode=None, **kwargs)

Configure Starlink dish settings.

```python
result = client.set_dish_config(
    snow_melt_mode=True,
    power_save_mode=False
)
# Returns:
# {
#     "success": true,
#     "message": "Configuration updated",
#     "updated_config": {...}
# }
```

### get_device_location(remote=False)

Get the device location.

```python
# Get precise GPS location (local)
location = client.get_device_location(remote=False)
# Returns:
# {
#     "latitude": 47.6062,
#     "longitude": -122.3321,
#     "altitude": 50.0
# }

# Get H3 cell location (remote)
location = client.get_device_location(remote=True)
# Returns:
# {
#     "h3_cell": "8a2a1072b59ffff"
# }
```

### get_wifi_status()

Get WiFi status and connected clients.

```python
wifi = client.get_wifi_status()
# Returns:
# {
#     "ssid": "STARLINKXXX",
#     "enabled": true,
#     "channel": 36,
#     "connected_clients": [...],
#     "signal_strength": -45
# }
```

### change_wifi_config(ssid=None, password=None, bypass_mode=None, **kwargs)

Modify WiFi configuration.

```python
result = client.change_wifi_config(
    ssid="MyNewSSID",
    password="newsecurepassword123",
    bypass_mode=False
)
# Returns:
# {
#     "success": true,
#     "message": "WiFi configuration updated",
#     "updated_config": {...}
# }
```

### get_account_data()

Get basic account information (remote only, requires authentication).

```python
account = client.get_account_data()
# Returns:
# {
#     "email": "user@example.com",
#     "name": "John Doe",
#     "service_plan": "Residential",
#     "account_number": "ABC123456"
# }
```

## Connection Types

### Local Connection

The default connection is to the local Starlink dish at `192.168.100.1:9200`. This requires you to be on the same network as your Starlink router. Local connections automatically use insecure gRPC channels.

```python
client = StarlinkClient()  # Uses default local address with insecure channel
```

The library automatically detects RFC 1918 private IP addresses and uses insecure channels for them:
- 10.0.0.0/8 (10.x.x.x)
- 172.16.0.0/12 (172.16.x.x - 172.31.x.x)
- 192.168.0.0/16 (192.168.x.x)

### Remote Connection

For remote connections, you need an authentication token. Remote connections automatically use secure SSL/TLS channels:

```python
client = StarlinkClient(
    target="remote.starlink.com:9200",
    auth_token="your-auth-token"
)
```

### Manual Channel Control

You can override automatic detection with the `secure` parameter:

```python
# Force secure channel even for local IP
client = StarlinkClient(target="192.168.100.1:9200", secure=True)

# Force insecure channel (not recommended except for testing)
client = StarlinkClient(target="test.local:9200", secure=False)
```

## Error Handling

The library raises `grpc.RpcError` exceptions when gRPC calls fail:

```python
from starlink_connectivity_tools import StarlinkClient
import grpc

client = StarlinkClient()

try:
    status = client.get_status()
except grpc.RpcError as e:
    print(f"gRPC error: {e.code()} - {e.details()}")
except PermissionError as e:
    print(f"Permission error: {e}")
```

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running tests

```bash
pytest tests/
```

### Code formatting

```bash
black starlink_connectivity_tools/
```

### Type checking

```bash
mypy starlink_connectivity_tools/
```

## Related Projects

This library is inspired by and compatible with:

- [starlink-client](https://github.com/Eitol/starlink-client) - Multi-language support (Python, Go, JS)
- [starlink-grpc-tools](https://github.com/sparky8512/starlink-grpc-tools) - Scripts and tools for Starlink gRPC interaction

## Notes

- The Starlink gRPC API is **unofficial and undocumented**
- This library uses reverse-engineered proto files
- API may change without notice as SpaceX updates the firmware
- Local connections do not require authentication
- Remote connections require valid authentication tokens

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This is an unofficial library and is not affiliated with, endorsed by, or connected to SpaceX or Starlink. Use at your own risk.