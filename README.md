# starlink_connectivity_tools.py

A Python library for managing Starlink satellite connectivity with support for crisis mode and bandwidth optimization.

## Features

- **Connection Management**: Scan and connect to available Starlink satellites
- **Crisis Mode**: Prioritize connections during emergency scenarios with custom bandwidth and latency requirements
- **Bandwidth Optimization**: Optimize bandwidth usage for satellite connections
- **Status Reporting**: Get detailed connection metrics and performance data

## Quick Start

```python
import json
from src.connection_manager import SatelliteConnectionManager
from src.bandwidth_optimizer import BandwidthOptimizer

# Initialize connection manager
manager = SatelliteConnectionManager()

# Enable crisis mode for emergency scenarios
manager.enable_crisis_mode({
    'crisis_min_bandwidth': 1.0,  # Mbps
    'crisis_max_latency': 1000    # ms
})

# Scan and connect
connections = manager.scan_available_connections()
if connections:
    manager.connect(connections[0])

# Get status report
report = manager.get_connection_report()
print(json.dumps(report, indent=2))
```

## Installation

```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
```

## Usage

### Connection Management

The `SatelliteConnectionManager` class provides methods to manage satellite connections:

- `enable_crisis_mode(config)`: Enable crisis mode with custom configuration
- `scan_available_connections()`: Scan for available satellite connections
- `connect(connection)`: Connect to a specific satellite
- `get_connection_report()`: Get detailed status report of the current connection

### Bandwidth Optimization

The `BandwidthOptimizer` class helps optimize bandwidth usage:

- `enable_optimization(profile)`: Enable bandwidth optimization with a specific profile
- `disable_optimization()`: Disable bandwidth optimization
- `get_optimization_status()`: Get current optimization status

## License

See [LICENSE](LICENSE) for details.