# starlink_connectivity_tools.py

A Python library for monitoring and analyzing Starlink satellite internet connectivity.

## Features

- Check Starlink service availability by location
- Monitor connection quality in real-time
- Measure latency, download/upload speeds, and packet loss
- Track signal strength and satellite connections
- Generate connectivity statistics and reports

## Usage

### Venezuela Scenario Example

Run the Venezuela scenario example to see how Starlink connectivity can be monitored:

```bash
python examples/venezuela_scenario.py
```

This example demonstrates:
- Checking Starlink availability in Venezuelan cities
- Monitoring connection quality over time
- Analyzing connectivity statistics
- Understanding the impact of Starlink in areas with limited internet infrastructure

### Basic Usage

```python
from starlink_connectivity_tools import StarlinkConnectivity, check_availability

# Check if Starlink is available
check_availability("Your Location")

# Create a connectivity monitor
monitor = StarlinkConnectivity(location="Your Location")

# Monitor connection for 60 seconds
metrics = monitor.monitor_connection(duration_seconds=60, interval_seconds=5)

# Display statistics
monitor.print_statistics()
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## License

Apache License 2.0
