# Starlink Connectivity Tools

Python tools for interacting with Starlink Enterprises API via gRPC. This library provides a simple interface to monitor and manage Starlink router and dish devices.

## Features

- 📡 Get device status and diagnostics
- 🛰️ Monitor ping metrics and network performance
- 🚀 Run speed tests
- 🔧 Retrieve device information
- 🔄 Reboot devices remotely
- 📊 Support for both router and dish devices

## Requirements

- Python 3.7+
- gRPC
- Protocol Buffers
- Access to Starlink devices on your network

## Installation

1. Clone this repository:
```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. You'll also need the Starlink protobuf files (`device_pb2.py` and `device_pb2_grpc.py`). These can be generated from the official Starlink protobuf definitions.

## Usage

### Command Line Interface

The main script provides a CLI for interacting with Starlink devices:

```bash
# Get diagnostics from both router and dish
python starlink_client.py --command diagnostics

# Get status from router only
python starlink_client.py --command status --target router

# Run a speed test
python starlink_client.py --command run-speed-test

# Get ping metrics
python starlink_client.py --command ping

# Get device information
python starlink_client.py --command device-info

# Reboot the router
python starlink_client.py --command reboot --target router

# Output to a file in JSON format
python starlink_client.py --command status --format json --output status.json
```

### CLI Options

- `--command, -c`: Command to execute (diagnostics, status, ping, reboot, speed-test, run-speed-test, device-info)
- `--target, -t`: Target device (router, dish, both) - default: both
- `--router-addr`: Router gRPC address - default: 192.168.1.1:9000
- `--dish-addr`: Dish gRPC address - default: 192.168.100.1:9200
- `--format, -f`: Output format (json, pretty) - default: pretty
- `--output, -o`: Output file path (optional)

### Python API

You can also use the `StarlinkClient` class directly in your Python code:

```python
from starlink_client import StarlinkClient

# Initialize the client
client = StarlinkClient()

# Get status
status = client.get_status(target="both")
print(status)

# Get diagnostics
diagnostics = client.get_diagnostics(target="router")
print(diagnostics)

# Get ping metrics
ping_metrics = client.get_ping_metrics()
print(ping_metrics)

# Run speed test
speed_test = client.run_speed_test()
print(speed_test)

# Get device info
device_info = client.get_device_info(target="dish")
print(device_info)

# Reboot device
result = client.reboot(target="router")
print(result)
```

### Custom Addresses

If your Starlink devices are on non-standard addresses:

```python
from starlink_client import StarlinkClient

client = StarlinkClient(
    router_addr="192.168.2.1:9000",
    dish_addr="192.168.100.1:9200"
)

status = client.get_status()
```

## Examples

The `examples/` directory contains various usage examples:

- `basic_status.py` - Get basic status information
- `get_diagnostics.py` - Retrieve detailed diagnostics
- `ping_monitoring.py` - Monitor ping metrics (with continuous monitoring option)
- `speed_test.py` - Run speed tests and retrieve results
- `device_info.py` - Get detailed device information
- `custom_addresses.py` - Use custom gRPC addresses

Run an example:
```bash
cd examples
python basic_status.py
```

## API Methods

### StarlinkClient Methods

- `get_diagnostics(target="both")` - Get diagnostic information
- `get_status(target="both")` - Get current status
- `get_ping_metrics()` - Get ping/latency metrics (dish only)
- `get_speed_test()` - Get last speed test results (router only)
- `run_speed_test()` - Run a new speed test (router only)
- `get_device_info(target="both")` - Get device information
- `reboot(target)` - Reboot a device (router or dish)

### Parameters

- `target`: Specifies which device(s) to query
  - `"router"` - Router only
  - `"dish"` - Dish only
  - `"both"` - Both devices (where applicable)

## Default Addresses

- Router: `192.168.1.1:9000`
- Dish: `192.168.100.1:9200`

These are the standard addresses for Starlink devices on the local network.

## Error Handling

All methods return a dictionary. In case of errors, the response will contain an `"error"` key:

```python
result = client.get_status()
if "error" in result.get("router", {}):
    print(f"Router error: {result['router']['error']}")
```

## Network Requirements

- Your computer must be connected to the Starlink network
- Starlink devices must be accessible at their gRPC endpoints
- No authentication is required for local network access

## Troubleshooting

**Connection Issues:**
- Ensure you're connected to the Starlink network
- Verify device addresses are correct
- Check firewall settings aren't blocking gRPC ports

**Import Errors:**
- Make sure protobuf files (`device_pb2.py`, `device_pb2_grpc.py`) are in the same directory
- Install all requirements: `pip install -r requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This is an unofficial tool and is not affiliated with or endorsed by SpaceX or Starlink. Use at your own risk.

## Acknowledgments

Based on the Starlink gRPC API for enterprises and business customers.