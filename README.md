# Starlink Connectivity Tools

Tools for monitoring and managing Starlink satellite connectivity.

## Features

- **Real-time Monitoring**: Track Starlink connection metrics including download/upload speeds, latency, signal strength, and more
- **Performance Reports**: Generate detailed performance reports over customizable time periods
- **Connection Management**: Manage satellite connections with automatic failover capabilities
- **CLI Interface**: Powerful command-line interface for all monitoring and management tasks
- **Customizable Thresholds**: Set custom alert thresholds for various metrics

## Installation

```bash
pip install -e .
```

## Usage

### CLI Commands

Check current Starlink status:
```bash
starlink-cli status
```

Start continuous monitoring:
```bash
starlink-cli monitor --interval 30
```

Generate a performance report:
```bash
starlink-cli report --hours 48
```

Export data to JSON:
```bash
starlink-cli export --output data.json --hours 24
```

Manage connection:
```bash
starlink-cli connection
```

Set monitoring thresholds:
```bash
starlink-cli thresholds
```

Reboot Starlink dish (use with caution):
```bash
starlink-cli reboot
```

### Python API

```python
from src.starlink_monitor import StarlinkMonitor
from src.connection_manager import SatelliteConnectionManager

# Initialize monitor
monitor = StarlinkMonitor(host="192.168.100.1")

# Get current metrics
metrics = monitor.get_metrics()
print(f"Download: {metrics.download_speed} Mbps")
print(f"Latency: {metrics.latency} ms")

# Get performance report
report = monitor.get_performance_report(hours=24)
print(f"Availability: {report['availability_percent']}%")

# Connection management
manager = SatelliteConnectionManager(enable_starlink=True)
manager.scan_available_connections()
manager.connect("starlink_satellite")
```

## Requirements

- Python 3.7+
- Access to Starlink router (default: 192.168.100.1)

## License

MIT License - see LICENSE file for details

## Author

Daniel Azevedo Novais