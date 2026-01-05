# starlink_connectivity_tools.py

A robust framework for maintaining satellite connectivity in challenging crisis scenarios, with special attention to the specific needs of emergency response teams.

## Acknowledgments

This project was inspired by connectivity challenges in Venezuela and other crisis scenarios where reliable communications are critical for emergency response and humanitarian aid.

### Key Features Implemented

#### 1. Crisis-Optimized Connection Management
- Automatic satellite switching based on quality metrics
- Crisis mode with relaxed requirements for emergency situations
- Continuous health monitoring

#### 2. Intelligent Bandwidth Allocation
- Priority-based bandwidth allocation
- Critical communications (medical, SOS) receive guaranteed bandwidth
- Dynamic adjustment based on available bandwidth

#### 3. Robust Failover System
- Multiple backup connection types (cellular, WiFi, secondary satellite)
- Cost-aware backup selection
- Automatic failover and failback

#### 4. Power Management
- Multiple power modes (Normal, Conservation, Crisis, Survival)
- Battery runtime optimization
- Scheduled sleep cycles for extreme power saving

#### 5. Comprehensive Diagnostics
- Full system health checks
- Historical tracking and reporting
- Automated issue detection and recommendations

#### 6. Emergency Scenarios
- Special modes for humanitarian and medical operations
- Guaranteed minimum connectivity for emergency communications
- Optimized for crisis response teams and aid organizations
A Python library for working with Starlink connectivity.

## Installation

```bash
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
A comprehensive Python toolkit for managing satellite connectivity in emergency and crisis scenarios, with focus on power management and battery optimization for remote operations.

## Features

- **Power Management**: Battery optimization with multiple power modes for extended runtime
- **Component Control**: Manage individual components to optimize power consumption
- **Automatic Optimization**: Intelligent power mode selection based on target battery runtime
- **Sleep Scheduling**: Schedule periodic sleep/wake cycles for extreme power conservation

## Installation

A Python library for managing Starlink satellite connectivity with support for bandwidth optimization, connection management, and prioritized data transmission.

## Features

- **Bandwidth Optimization**: Efficiently allocate and manage bandwidth across multiple connections
- **Priority Management**: Prioritize critical connections (e.g., medical emergencies)
- **Connection Management**: Track and control multiple simultaneous connections
- **Use Cases**: Pre-built examples for common scenarios including medical emergency communications
# starlink_connectivity_tools.py

A Python library for managing and monitoring Starlink connectivity, with built-in emergency mode support for critical situations.

## Features

- **Emergency Mode**: Automated monitoring and recovery for critical connectivity scenarios
- **Status Monitoring**: Real-time dish status and connectivity checks
- **Alert Management**: Detect and respond to dish alerts
- **Automatic Recovery**: Attempt automated recovery procedures when issues are detected

## Installation

Clone the repository:
```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
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
### Low Power Operation Example

Optimize satellite terminal for 24-hour battery life:

```bash
python3 examples/low_power_operation.py
```

This example demonstrates:
- Automatic power optimization for target battery runtime
- Different power modes (Normal, Conservation, Crisis, Survival)
- Component-level power management
- Scheduled sleep cycles for extreme power savings
- Real-time power consumption monitoring

## Usage

### Power Management

The PowerManager module provides intelligent battery optimization:

```python
from src.power_manager import PowerManager

# Initialize with battery capacity (Watt-hours)
power_manager = PowerManager(total_battery_capacity=500.0)

# Optimize for 24-hour battery life
power_manager.optimize_for_battery_life(target_runtime_hours=24)

# Get power status report
report = power_manager.get_power_report()
print(f"Estimated runtime: {report['estimated_runtime_hours']:.1f} hours")
print(f"Total power: {report['total_power_consumption_w']:.1f} W")
```

### Manual Power Mode Control

```python
from src.power_manager import PowerMode

# Set specific power mode
power_manager.set_power_mode(PowerMode.CONSERVATION)

# Available modes:
# - PowerMode.NORMAL: Full performance
# - PowerMode.CONSERVATION: Reduced power (30-40% savings)
# - PowerMode.CRISIS: Minimal power (60-70% savings)
# - PowerMode.SURVIVAL: Maximum savings (85-90% savings)
```

### Component Management

```python
# Disable non-essential components
power_manager.disable_component('cellular_modem')
power_manager.disable_component('compute_unit')

# Re-enable when needed
power_manager.enable_component('cellular_modem')
```

### Scheduled Sleep Cycles

```python
# Active for 5 minutes, sleep for 30 minutes
power_manager.schedule_sleep_cycle(
    active_duration=300,   # 5 minutes
    sleep_duration=1800    # 30 minutes
)
No external dependencies are required for the basic examples.

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
pip install starlink_connectivity_tools
```

Or install from source:
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
pip install -r requirements.txt
```

## Usage

```python
from starlink_connectivity_tools import StarlinkConnectivity, check_connection, format_speed

# Create a connectivity instance
conn = StarlinkConnectivity(dish_id="DISH-12345")

# Connect to the dish
conn.connect()

# Check connection status
print(conn.is_connected())  # True

# Get status
status = conn.get_status()
print(status)  # {'dish_id': 'DISH-12345', 'connected': True}

# Use utility functions
print(check_connection("DISH-12345"))  # True
print(format_speed(250.5))  # "250.50 Mbps"
print(format_speed(1500))  # "1.50 Gbps"
```

## Testing

Run the test suite using pytest:

```bash
python -m pytest tests/
```

Run tests with verbose output:

```bash
python -m pytest tests/ -v
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```
### Emergency Mode Example

The emergency mode example demonstrates how to monitor and recover from connectivity issues:
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

## Quick Start

```python
from starlink_connectivity import BandwidthOptimizer

# Initialize optimizer with available bandwidth
optimizer = BandwidthOptimizer(total_bandwidth=100.0)  # 100 Mbps

# Allocate bandwidth for a connection
allocation = optimizer.allocate_bandwidth(
    connection_id="my_connection",
    destination="data.endpoint",
    requested_bandwidth=10.0
)

print(f"Allocated: {allocation.allocated_bandwidth} Mbps")
print(f"Status: {allocation.status}")
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
### 1. Remote Off-Grid Operation

Operating satellite terminals in remote locations with limited solar or battery power:

```python
# Optimize for 24-hour battery life
power_manager.optimize_for_battery_life(target_runtime_hours=24)
```

### 2. Emergency Backup Power

Extend battery life during power outages:

```python
# Switch to crisis mode immediately
power_manager.set_power_mode(PowerMode.CRISIS)

# Disable non-critical components
power_manager.disable_component('compute_unit')
```

### 3. Scheduled Operations

Maintain connectivity with periodic check-ins to conserve battery:

```python
# Active 10 minutes every hour
power_manager.schedule_sleep_cycle(
    active_duration=600,    # 10 minutes active
    sleep_duration=3000     # 50 minutes sleep
)
```

## Power Consumption Reference

Typical power consumption by component and mode:

| Component | Normal | Conservation | Crisis | Sleep |
|-----------|--------|--------------|--------|-------|
| Satellite Modem | 60W | 40W | 20W | 5W |
| Router | 10W | 7W | 5W | 2W |
| Cellular Modem | 8W | 6W | 4W | 1W |
| Compute Unit | 25W | 15W | 10W | 3W |
| **Total** | **103W** | **68W** | **39W** | **11W** |

**Example Runtimes** (500 Wh battery):
- Normal mode: ~5 hours
- Conservation mode: ~7.5 hours
- Crisis mode: ~13 hours
- Survival mode: ~45 hours
- Sleep cycles (5m/30m): ~26 hours
### Medical Emergency Communications

Prioritize medical data transmission during emergency situations:

```python
from starlink_connectivity import BandwidthOptimizer

optimizer = BandwidthOptimizer(total_bandwidth=100.0)

# Prioritize medical data transmission
optimizer.allocate_bandwidth(
    connection_id="medical_evac",
    destination="medical.data",
    requested_bandwidth=10.0
)
```

See the [examples/medical_emergency.py](examples/medical_emergency.py) for a complete medical emergency communications scenario.

## API Reference

### BandwidthOptimizer

Main class for managing bandwidth allocation.

#### Methods

- `allocate_bandwidth(connection_id, destination, requested_bandwidth, priority=0)`: Allocate bandwidth for a connection
- `release_bandwidth(connection_id)`: Release bandwidth from a connection
- `get_allocation(connection_id)`: Get allocation details for a connection
- `get_all_allocations()`: Get all current allocations
- `get_available_bandwidth()`: Get currently available bandwidth

## Running Examples

```bash
# Medical emergency communications example
python examples/medical_emergency.py
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

# Install in development mode
pip install -e .
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### Running Tests

```bash
python -m unittest discover tests
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

This example will:
1. Connect to a Starlink dish
2. Perform an initial connectivity assessment
3. Activate emergency mode if issues are detected
4. Attempt automatic recovery procedures
5. Monitor connectivity for a period
6. Provide a detailed summary of operations

### Using the Library

```python
from starlink_connectivity_tools import StarlinkDish, EmergencyMode

# Connect to dish using context manager
with StarlinkDish(host="192.168.100.1") as dish:
    # Create emergency mode handler
    emergency = EmergencyMode(dish)
    
    # Check connectivity
    assessment = emergency.check_connectivity()
    
    # Activate emergency mode if needed
    if assessment and not assessment['operational']:
        emergency.activate()
        emergency.attempt_recovery()
    
    # Monitor for a period
    emergency.monitor(duration=60, interval=10)
```

## API Overview

### StarlinkDish

- `connect()`: Establish connection to the dish
- `disconnect()`: Disconnect from the dish
- `get_status()`: Get current dish status
- `get_alerts()`: Get active alerts
- `reboot()`: Reboot the dish

### EmergencyMode

- `activate()`: Activate emergency mode
- `deactivate()`: Deactivate emergency mode
- `check_connectivity()`: Assess current connectivity
- `attempt_recovery()`: Attempt automatic recovery
- `monitor(duration, interval)`: Monitor connectivity over time
- `print_summary()`: Print operation summary

## Note

This is a simplified implementation for demonstration purposes. In a production environment, you would integrate with the actual Starlink gRPC API using libraries like `starlink-grpc-core`.

## License

See LICENSE file for details.
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
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_optimizer
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

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=starlink_connectivity tests/
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

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.
## Acknowledgments

Designed for reliable satellite connectivity in remote, off-grid, and emergency scenarios where power management is critical.
This library is designed to work with Starlink satellite internet connections, providing tools for optimized bandwidth management in various scenarios including critical communications during emergencies.
Inspired by real-world connectivity challenges and the need for reliable emergency communication systems in crisis scenarios.
## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/danielnovais-tech/starlink_connectivity_tools.py).
