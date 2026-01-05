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
# Starlink Connectivity Tools for Crisis Scenarios

A Python-based toolkit for optimizing satellite connectivity in crisis scenarios, inspired by challenges faced in Venezuela and other emergency situations.

## Features

- **Smart Connection Management**: Automatic satellite switching and optimization
- **Bandwidth Prioritization**: Critical communications get priority bandwidth
- **Failover Handling**: Automatic switch to backup connections
- **Power Management**: Optimize for limited power/battery scenarios
- **Comprehensive Diagnostics**: Full system health monitoring
- **Emergency Mode**: Special configurations for crisis situations
# Starlink Connectivity Tools

A comprehensive Python toolkit for managing satellite connectivity in emergency and crisis scenarios, inspired by real-world connectivity challenges in Venezuela and other regions.

## Features

- **Connection Management**: Scan, connect, and manage satellite connections
- **Bandwidth Optimization**: Intelligent bandwidth allocation with traffic prioritization
- **Crisis Mode**: Special emergency mode for critical communications only
- **Failover Handling**: Automatic connection failover with health monitoring
- **Power Management**: Battery optimization with multiple power modes
- **Diagnostics**: Comprehensive connectivity diagnostics and health checks

## Installation

```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
pip install -r requirements.txt
```

## Usage

### Emergency Mode Example

Run the emergency connectivity system demo:

```bash
python3 examples/emergency_mode.py
```

This example demonstrates:
- Enabling emergency/crisis mode
- Establishing satellite connectivity
- Sending emergency SOS messages
- Synchronizing medical data with priority bandwidth
- Continuous monitoring and health checks
- Graceful shutdown with status reporting

Press `Ctrl+C` to gracefully shutdown the system.

## Core Modules

### Connection Manager (`src/connection_manager.py`)
Handles satellite connectivity, scanning, and connection management.

```python
from src.connection_manager import SatelliteConnectionManager

manager = SatelliteConnectionManager()
connections = manager.scan_available_connections()
manager.connect(connections[0])
```

### Bandwidth Optimizer (`src/bandwidth_optimizer.py`)
Manages bandwidth allocation and traffic prioritization.
A Python library for managing Starlink satellite connections, optimizing bandwidth usage, handling failover scenarios, and managing power consumption.

## Features

- **Connection Management**: Establish, monitor, and manage Starlink satellite connections
- **Bandwidth Optimization**: Optimize bandwidth usage and manage network traffic efficiently
- **Failover Handling**: Automatic failover to backup connections when primary connection fails
- **Power Management**: Manage power consumption with low-power modes for battery-powered scenarios
- **Diagnostics**: Comprehensive diagnostic tools and health checks for Starlink connections

## Project Structure

```
starlink-connectivity-tools/
├── src/
│   ├── __init__.py
│   ├── connection_manager.py      # Connection establishment and monitoring
│   ├── bandwidth_optimizer.py     # Bandwidth optimization and traffic management
│   ├── failover_handler.py        # Automatic failover to backup connections
│   ├── power_manager.py           # Power consumption management
│   ├── diagnostics.py             # Diagnostic tools and health checks
│   └── config/
│       └── settings.py            # Configuration management
├── tests/
│   ├── test_connection_manager.py # Tests for connection manager
│   └── test_bandwidth_optimizer.py # Tests for bandwidth optimizer
├── examples/
│   ├── emergency_mode.py          # Emergency mode configuration example
│   └── low_power_mode.py          # Low power mode configuration example
├── requirements.txt               # Project dependencies
├── setup.py                       # Package setup configuration
└── README.md                      # This file
```

## Installation

```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
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

```python
from starlink_connectivity_tools import StarlinkManager

# Initialize the manager
manager = StarlinkManager()

# Enable emergency mode for crisis scenarios
manager.enable_emergency_mode()

# Monitor connection health
status = manager.get_connection_status()
print(f"Connection Status: {status}")
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
### Smart Connection Management

```python
# Automatic satellite switching
manager.enable_auto_switching()

# Manual satellite selection
manager.select_satellite(satellite_id="sat-001")
```

### Bandwidth Prioritization

```python
# Set priority for critical communications
manager.set_priority("emergency_calls", priority=1)
manager.set_priority("data_sync", priority=2)
manager.set_priority("general_web", priority=3)
### Basic Connection Management

```python
from src.connection_manager import ConnectionManager

# Create a connection manager
manager = ConnectionManager()

# Connect to Starlink
manager.connect()

# Check connection status
status = manager.get_status()
print(f"Connected: {status['connected']}")

# Disconnect
manager.disconnect()
```

### Bandwidth Optimization

```python
from src.bandwidth_optimizer import BandwidthOptimizer

optimizer = BandwidthOptimizer(total_bandwidth=100.0)
optimizer.enable_crisis_mode()
allocated = optimizer.allocate_bandwidth(
    connection_id="emergency_msg",
    destination="emergency.comms",
    requested_bandwidth=5.0
)
```

### Failover Handler (`src/failover_handler.py`)
Manages connection failover and health monitoring.
# Create bandwidth optimizer
optimizer = BandwidthOptimizer(max_bandwidth=100)  # 100 Mbps limit

# Enable optimization
optimizer.enable_optimization()

# Set bandwidth limit
optimizer.set_bandwidth_limit(50)

# Get current usage
usage = optimizer.get_current_usage()
print(f"Optimization enabled: {usage['optimization_enabled']}")
```

### Failover Configuration

```python
from src.failover_handler import FailoverHandler

handler = FailoverHandler()
healthy = handler.check_connection_health(latency=50.0, packet_loss=0.5)
if not healthy:
    handler.initiate_failover(reason="High latency detected")
```

### Power Manager (`src/power_manager.py`)
Manages power consumption and battery optimization.

```python
from src.power_manager import PowerManager, PowerMode

power_mgr = PowerManager(total_battery_capacity=500.0)
power_mgr.set_power_mode(PowerMode.CRISIS)
power_mgr.optimize_for_battery_life(target_runtime_hours=48)
```

### Diagnostics (`src/diagnostics.py`)
Performs connectivity diagnostics and health checks.

```python
from src.diagnostics import ConnectivityDiagnostics

diagnostics = ConnectivityDiagnostics()
report = diagnostics.run_full_diagnostic()
```

## Crisis Mode

Crisis mode prioritizes critical traffic only, reducing power consumption and ensuring essential communications remain operational:

- **Emergency communications**: SOS messages, emergency calls
- **Medical data**: Patient records, medical telemetry
- **Coordination**: Central command communications

Non-critical traffic is automatically denied to preserve bandwidth and battery life.

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## License

MIT License - see LICENSE file for details
# Create failover handler
failover = FailoverHandler()

# Enable automatic failover
failover.enable_failover()

# Add backup connections
failover.add_backup_connection({"type": "cellular", "priority": 1})
failover.add_backup_connection({"type": "satellite_backup", "priority": 2})

# Trigger manual failover if needed
result = failover.trigger_failover()
print(f"Failover status: {result['status']}")
```

### Power Management

```python
# Enable power-saving mode
manager.enable_power_saving()

# Set battery threshold for emergency mode
manager.set_battery_threshold(20)  # Switch to emergency mode at 20%
from src.power_manager import PowerManager

# Create power manager
power_mgr = PowerManager()

# Enable low power mode
power_mgr.enable_low_power_mode()

# Get power status
status = power_mgr.get_power_status()
print(f"Power mode: {status['power_mode']}")
print(f"Power consumption: {status['power_consumption']}%")

# Estimate battery runtime
runtime = power_mgr.estimate_runtime(battery_capacity=500)  # 500 Wh battery
print(f"Estimated runtime: {runtime:.1f} hours")
```

### Diagnostics

```python
# Get comprehensive system diagnostics
diagnostics = manager.run_diagnostics()
print(diagnostics.report())

# Monitor specific metrics
signal_strength = manager.get_signal_strength()
latency = manager.get_latency()
bandwidth = manager.get_available_bandwidth()
```

## Configuration

Create a `config.yaml` file in your project directory:

```yaml
starlink:
  emergency_mode:
    enabled: false
    auto_activate: true
    battery_threshold: 15
  
  bandwidth_priorities:
    emergency_calls: 1
    medical_data: 2
    emergency_messages: 3
    general_traffic: 4
  
  power_management:
    power_saving_enabled: false
    low_power_threshold: 30
    critical_battery_level: 10
  
  failover:
    enabled: true
    backup_connections:
      - type: cellular
        priority: 1
      - type: mesh_network
        priority: 2
```

## Crisis Scenario Use Cases

### Venezuela Emergency Response
- Optimize connectivity during power outages
- Prioritize medical and emergency communications
- Efficient bandwidth usage in limited infrastructure

### Natural Disaster Response
- Quick deployment and configuration
- Automatic failover when primary connections fail
- Battery-optimized operation for extended periods

### Remote Area Operations
- Intelligent satellite selection for best coverage
- Adaptive bandwidth management
- Real-time diagnostics and monitoring

## Requirements

- Python 3.8 or higher
- Network connectivity for satellite communication
- Compatible Starlink hardware (for production use)

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=starlink_connectivity_tools

# Run specific test file
pytest tests/test_connection_manager.py
```

## Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code:
- Follows PEP 8 style guidelines
- Includes appropriate tests
- Updates documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by real-world challenges in Venezuela and crisis scenarios
- Built with support from the open-source community
- Thanks to all contributors and supporters

## Support

For issues, questions, or contributions:
- Open an issue on [GitHub](https://github.com/danielnovais-tech/starlink_connectivity_tools.py/issues)
- Contact: daniel.novais@sempreceub.com
- Documentation: [GitHub Repository](https://github.com/danielnovais-tech/starlink_connectivity_tools.py)

## Roadmap

- [ ] Enhanced power optimization algorithms
- [ ] Multi-satellite mesh networking
- [ ] Mobile app for remote monitoring
- [ ] Integration with emergency response systems
- [ ] Advanced predictive failover
- [ ] Support for additional satellite providers

## Disclaimer

This tool is designed to assist in crisis scenarios and optimize satellite connectivity. Always follow local regulations and guidelines when deploying communication equipment. This software is provided "as is" without warranty of any kind.
from src.diagnostics import Diagnostics

# Create diagnostics instance
diag = Diagnostics()

# Run health check
health = diag.run_health_check()
print(f"Health status: {health['status']}")

# Test connectivity
connectivity = diag.test_connectivity()
print(f"Connectivity test: {connectivity['status']}")

# Get signal strength
signal = diag.get_signal_strength()
print(f"Signal strength: {signal['signal_strength']}")
```

## Examples

### Emergency Mode

Run the emergency mode example for automatic failover configuration:

```bash
python examples/emergency_mode.py
```

This example demonstrates:
- Extended connection timeout and retry settings
- Automatic failover with multiple backup connections
- Health check monitoring

### Low Power Mode

Run the low power mode example for battery-powered scenarios:

```bash
python examples/low_power_mode.py
```

This example demonstrates:
- Reduced power consumption settings
- Bandwidth limiting and optimization
- Battery runtime estimation

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/test_connection_manager.py
```

## Configuration

The library uses a centralized configuration system in `src/config/settings.py`:

```python
from src.config.settings import Settings

# Create settings with custom config
config = {
    "connection": {
        "timeout": 60,
        "retry_attempts": 5,
    },
    "power": {
        "default_mode": "low_power",
    },
}
settings = Settings(custom_config=config)

# Get configuration values
timeout = settings.get("connection.timeout")

# Update configuration
settings.set("connection.retry_attempts", 3)
```

## Development

### Code Style

This project follows Python best practices:
- PEP 8 style guide
- Type hints where appropriate
- Comprehensive docstrings

### Running Linters

```bash
# Format code with black
black src/ tests/ examples/

# Check code with flake8
flake8 src/ tests/ examples/

# Type checking with mypy
mypy src/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Inspired by real-world connectivity challenges and the need for reliable emergency communication systems in crisis scenarios.
## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/danielnovais-tech/starlink_connectivity_tools.py).
