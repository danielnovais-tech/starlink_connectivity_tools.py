# Starlink Connectivity Tools

Tools for monitoring and managing Starlink satellite connectivity.

## Features

- **Real-time Monitoring**: Track Starlink connection metrics including download/upload speeds, latency, signal strength, and more
- **Performance Reports**: Generate detailed performance reports over customizable time periods
- **Connection Management**: Manage satellite connections with automatic failover capabilities
- **CLI Interface**: Powerful command-line interface for all monitoring and management tasks
- **Customizable Thresholds**: Set custom alert thresholds for various metrics via config file
- **Logging**: Configurable logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Unit Tests**: Comprehensive unit tests for all CLI commands

## Installation

```bash
pip install -e .
```

## Configuration

Configuration is stored in `~/.config/starlink_monitor/config.json`. The default configuration includes:

```json
{
  "thresholds": {
    "min_download_speed": 25.0,
    "max_latency": 100.0,
    "max_packet_loss": 5.0,
    "max_obstruction": 10.0
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": null
  },
  "monitor": {
    "default_host": "192.168.100.1",
    "history_size": 1000,
    "default_interval": 60
  }
}
```

You can edit this file directly or use the CLI to modify thresholds interactively.

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

### Logging Options

Control logging output with command-line flags:

```bash
# Set log level
starlink-cli status --log-level DEBUG

# Log to file
starlink-cli monitor --log-file /var/log/starlink.log

# Combine options
starlink-cli monitor --log-level INFO --log-file /var/log/starlink.log
```

### Python API

```python
from src.starlink_monitor import StarlinkMonitor
from src.connection_manager import SatelliteConnectionManager
from src.config import Config

# Load configuration
config = Config()

# Initialize monitor with config
monitor = StarlinkMonitor(config=config)

# Get current metrics
metrics = monitor.get_metrics()
print(f"Download: {metrics.download_speed} Mbps")
print(f"Latency: {metrics.latency} ms")

# Get performance report
report = monitor.get_performance_report(hours=24)
print(f"Availability: {report['availability_percent']}%")

# Update thresholds
config.set_thresholds(min_download_speed=50.0, max_latency=80.0)

# Connection management
manager = SatelliteConnectionManager(enable_starlink=True)
manager.scan_available_connections()
manager.connect("starlink_satellite")
```

## Testing

Run unit tests:

```bash
python3 -m unittest discover tests
```

Run specific test file:

```bash
python3 -m unittest tests.test_cli -v
```

## Requirements

- Python 3.7+
- Access to Starlink router (default: 192.168.100.1)

## License

MIT License - see LICENSE file for details

## Author

Daniel Azevedo Novais