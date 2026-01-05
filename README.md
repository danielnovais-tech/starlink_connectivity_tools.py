# Starlink Connectivity Tools

Comprehensive tools for monitoring and managing Starlink satellite connectivity with CLI, configuration management, logging, and alerting capabilities.

## Features

- **Real-time Monitoring**: Track Starlink connection metrics including download/upload speeds, latency, signal strength, and more
- **Performance Reports**: Generate detailed performance reports over customizable time periods
- **Connection Management**: Manage satellite connections with automatic failover capabilities
- **CLI Interface**: Powerful command-line interface for all monitoring and management tasks
- **Customizable Thresholds**: Set custom alert thresholds for various metrics via config file
- **Logging**: Configurable logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Multiple Export Formats**: Export data to JSON or CSV
- **Unit Tests**: Comprehensive unit tests for all CLI commands
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **CLI Autocompletion**: Bash completion script for enhanced usability
- **Type Hints**: Full type annotations throughout the codebase
- **Config Validation**: Automatic validation of configuration files

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

Export data to CSV:
```bash
starlink-cli export --output data.csv --format csv --hours 48
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

## Docker Support

### Build Docker Image

```bash
docker build -t starlink-monitor .
```

### Run with Docker

```bash
# Check status
docker run -it --rm --network host starlink-monitor status

# Start monitoring
docker run -it --rm --network host starlink-monitor monitor --interval 30

# Export data
docker run -it --rm --network host -v $(pwd)/output:/app/output starlink-monitor export --output /app/output/data.csv --format csv
```

### Using Docker Compose

```bash
# Start continuous monitoring
docker-compose up -d

# Check status
docker-compose run --rm status-check

# View logs
docker-compose logs -f

# Stop monitoring
docker-compose down
```

## CLI Autocompletion

Enable Bash completion for enhanced CLI usability:

```bash
# Install completion script
sudo cp starlink-cli-completion.sh /etc/bash_completion.d/

# Or source it in your current session
source starlink-cli-completion.sh

# Now you can use tab completion:
starlink-cli <TAB>
starlink-cli export --format <TAB>
```

## Configuration Validation

The configuration file is automatically validated on load. To manually validate:

```python
from src.config import Config

config = Config()
is_valid, errors = config.validate()

if not is_valid:
    for error in errors:
        print(f"Error: {error}")
```

## Requirements

- Python 3.7+
- Access to Starlink router (default: 192.168.100.1)

## License

MIT License - see LICENSE file for details

## Author

Daniel Azevedo Novais