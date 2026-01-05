# Starlink Connectivity Tools

A Python library for managing Starlink connections with automatic failover capabilities.

## Features

- **Automatic Connection Failover**: Seamlessly switch between primary and backup connections when failures are detected
- **Configurable Health Checks**: Customize connection health monitoring with your own callback functions
- **Failure Threshold Management**: Set custom thresholds before triggering failover
- **Comprehensive Logging**: Track connection status and failover events
- **Failover History**: Review past failover events for analysis and debugging

## Installation

```bash
# Install from local source
pip install -e .

# Or install directly
pip install starlink-connectivity-tools
```

## Quick Start

### Basic Usage

```python
from starlink_connectivity_tools import FailoverHandler

# Create a failover handler
failover_handler = FailoverHandler(
    failure_threshold=3,    # Trigger failover after 3 consecutive failures
    check_interval=5.0      # Check connection every 5 seconds
)

# Automatic failover when primary fails
if failover_handler.should_failover():
    failover_handler.initiate_failover("Primary connection lost")
```

### Custom Health Check

```python
import requests
from starlink_connectivity_tools import FailoverHandler

def check_connection_health():
    """Custom health check function."""
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return response.status_code == 200
    except:
        return False

failover_handler = FailoverHandler(
    failure_threshold=3,
    check_interval=10.0,
    health_check_callback=check_connection_health
)
```

## Use Cases

### 1. Automatic Connection Monitoring

Monitor your Starlink connection and automatically switch to a backup connection when the primary fails:

```python
import time
from starlink_connectivity_tools import FailoverHandler

failover_handler = FailoverHandler(failure_threshold=3, check_interval=5.0)

while True:
    if failover_handler.should_failover():
        failover_handler.initiate_failover("Primary connection lost")
        print(f"Switched to: {failover_handler.get_current_state().value}")
    
    time.sleep(1)
```

### 2. Integration with Network Management

```python
from starlink_connectivity_tools import FailoverHandler
import subprocess

def switch_to_backup():
    """Execute network switch commands."""
    subprocess.run(["ip", "route", "add", "default", "via", "backup.gateway"])

failover_handler = FailoverHandler(failure_threshold=2, check_interval=3.0)

if failover_handler.should_failover():
    failover_handler.initiate_failover("Primary connection timeout")
    switch_to_backup()
```

## Examples

See the `examples/` directory for complete working examples:

- `automatic_failover.py`: Demonstrates automatic failover with simulated connection failures

Run an example:

```bash
cd examples
python automatic_failover.py
```

## API Reference

### FailoverHandler

Main class for managing connection failover.

**Constructor Parameters:**
- `failure_threshold` (int): Number of consecutive failures before triggering failover (default: 3)
- `check_interval` (float): Time in seconds between health checks (default: 5.0)
- `health_check_callback` (Callable): Optional callback function for custom health checks

**Methods:**
- `should_failover() -> bool`: Check if failover should be initiated
- `initiate_failover(reason: str) -> bool`: Initiate failover to backup connection
- `get_current_state() -> ConnectionState`: Get current connection state
- `get_failure_count() -> int`: Get current consecutive failure count
- `get_failover_history() -> list`: Get history of failover events
- `reset() -> None`: Reset handler to initial state

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=starlink_connectivity_tools

# Run specific test file
python -m unittest tests/test_failover.py
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Running Tests

```bash
python -m unittest discover tests
```

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.