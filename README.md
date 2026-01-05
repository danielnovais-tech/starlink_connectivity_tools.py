# starlink_connectivity_tools.py

A Python library for interacting with Starlink satellite internet devices.

## Installation

```bash
pip install -e .
```

Or using the package directly:

```bash
python setup.py install
```

## Usage

```python
from starlink_client import StarlinkClient

client = StarlinkClient()  # Local connection
stats = client.get_network_stats()
print(f"Download: {stats.download_speed} Mbps, Latency: {stats.latency} ms")
client.reboot_dish()
```

## Features

- **Network Statistics**: Retrieve download/upload speeds, latency, and connection status
- **Device Control**: Reboot your Starlink dish remotely
- **Easy Integration**: Simple Python API for Starlink device interaction

## API Reference

### StarlinkClient

Main client class for interacting with Starlink devices.

```python
client = StarlinkClient(host="192.168.100.1", port=9200, timeout=10)
```

#### Methods

- `get_network_stats()`: Returns a `NetworkStats` object with current network performance metrics
- `reboot_dish()`: Initiates a reboot of the Starlink dish

### NetworkStats

Data class containing network statistics:

- `download_speed`: Download speed in Mbps
- `upload_speed`: Upload speed in Mbps  
- `latency`: Latency in milliseconds
- `uptime`: Device uptime in seconds
- `obstruction_percentage`: Percentage of time obstructed
- `connected`: Whether the dish is connected to satellites

## Example

See `example.py` for a complete example:

```bash
python example.py
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

## License

MIT License - see LICENSE file for details