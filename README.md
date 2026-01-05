# Starlink Connectivity Tools

Python library for interacting with the Starlink dish gRPC API. This library provides a client for querying device status, network statistics, telemetry, and performing actions like rebooting the Starlink user terminal (dish).

## Overview

The Starlink user terminal exposes an **unauthenticated gRPC API** for monitoring and control. This API is not officially documented by SpaceX but has been reverse-engineered by the community.

### API Details

- **Protocol**: gRPC over HTTP/2
- **Local Address**: `192.168.100.1:9200` (local network only)
- **Authentication**: None required for local access
- **Remote Access**: Possible via Starlink's remote API with session cookies (valid for 15 days)
- **Service Discovery**: Supports gRPC server reflection

## Features

- ✅ Connect to local Starlink dish (192.168.100.1:9200)
- ✅ Remote access with session cookie authentication
- ✅ Service discovery using gRPC server reflection
- ✅ Extract proto files from the dish
- ✅ Query device status, network stats, and telemetry (requires proto files)
- ✅ Perform actions like rebooting or configuring the dish (requires proto files)

## Installation

### From PyPI (when published)

```bash
pip install starlink-connectivity-tools
```

### From Source

```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Connection

```python
from starlink_connectivity_tools import StarlinkDishClient

# Connect to local dish
with StarlinkDishClient() as client:
    # Discover available services
    services = client.discover_services()
    print(f"Available services: {services}")
```

### Remote Access

```python
from starlink_connectivity_tools import StarlinkDishClient

# Connect remotely with session cookie
with StarlinkDishClient(
    address="remote.starlink.com:9200",
    session_cookie="your-session-cookie"
) as client:
    services = client.discover_services()
    print(f"Available services: {services}")
```

### Extracting Proto Files

```python
from starlink_connectivity_tools.client import StarlinkDishClient
from starlink_connectivity_tools.reflection import ProtoReflectionClient

# Connect to dish
client = StarlinkDishClient()
client.connect()

# Create reflection client
reflection_client = ProtoReflectionClient(client._channel)

# List services
services = reflection_client.list_services()

# Extract proto file for a service
reflection_client.export_proto_file(
    services[0], 
    "./proto_files/starlink.proto"
)
```

## Examples

Several example scripts are provided in the `examples/` directory:

### Basic Usage
```bash
python examples/basic_usage.py
```

Demonstrates basic connection and service discovery.

### Extract Proto Files
```bash
python examples/extract_proto.py [output_directory]
```

Extracts proto file definitions from the Starlink dish using server reflection.

### Remote Access
```bash
python examples/remote_access.py <session_cookie> [remote_address]
```

Connects to the Starlink dish remotely using session cookies.

## Using Proto Files

The Starlink gRPC API requires proto files to make actual RPC calls. You have two options:

### Option 1: Extract from Dish (Recommended)

Use the `extract_proto.py` example to extract proto files directly from your dish:

```bash
python examples/extract_proto.py ./proto_files
```

### Option 2: Use Community Proto Files

The community has reverse-engineered proto files. Search for "starlink grpc proto" to find them.

### Compiling Proto Files

Once you have the proto files, compile them:

```bash
python -m grpc_tools.protoc \
    -I./proto_files \
    --python_out=. \
    --grpc_python_out=. \
    proto_files/*.proto
```

## API Reference

### StarlinkDishClient

Main client class for interacting with the Starlink dish.

#### Constructor Parameters

- `address` (str, optional): gRPC server address. Defaults to `192.168.100.1:9200`
- `session_cookie` (str, optional): Session cookie for remote access
- `use_reflection` (bool): Whether to use server reflection. Default: `True`
- `insecure` (bool): Whether to use insecure channel. Default: `True`
- `timeout` (int): Default timeout for RPC calls in seconds. Default: `10`

#### Methods

- `connect()`: Establish connection to the gRPC server
- `close()`: Close the gRPC channel
- `discover_services()`: List available gRPC services
- `get_status()`: Get device status (requires proto files)
- `get_network_stats()`: Get network statistics (requires proto files)
- `get_telemetry()`: Get telemetry data (requires proto files)
- `reboot()`: Reboot the dish (requires proto files)
- `set_configuration(config)`: Configure the dish (requires proto files)

### ProtoReflectionClient

Client for extracting proto definitions using gRPC server reflection.

#### Methods

- `list_services()`: List all available services
- `get_file_descriptor(symbol)`: Get file descriptor for a symbol
- `export_proto_file(symbol, output_path)`: Export proto file to disk

## Troubleshooting

### Cannot Connect to Local Dish

1. Ensure you're connected to the Starlink WiFi network
2. Verify the dish is powered on and operational
3. Check the address is `192.168.100.1:9200`
4. Some network configurations may block local gRPC access

### Remote Access Not Working

1. Verify your session cookie is still valid (15-day expiry)
2. Session cookies can be extracted from browser developer tools
3. Check you have internet connectivity
4. Ensure the remote address is correct

### Service Discovery Fails

1. The dish may not support server reflection (older firmware)
2. Try using community proto files instead
3. Check network connectivity

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This library is **not officially supported by SpaceX**. It relies on reverse-engineered API knowledge from the community. The API may change without notice, and usage is at your own risk.

## Acknowledgments

- Community efforts in reverse-engineering the Starlink API
- Tools like `grpcurl` and `grpc-reflection` that enable API discovery

## Related Tools

- [grpcurl](https://github.com/fullstorydev/grpcurl) - Command-line gRPC client
- [starlink-grpc-tools](https://github.com/sparky8512/starlink-grpc-tools) - Community Starlink tools
- [dishykit](https://github.com/Tylerjet/dishykit) - Starlink dish analysis tools

## Support

For issues and questions:
- Open an issue on [GitHub](https://github.com/danielnovais-tech/starlink_connectivity_tools.py/issues)
- Check existing community resources and documentation