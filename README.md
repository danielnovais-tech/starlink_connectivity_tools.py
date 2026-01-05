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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Inspired by real-world connectivity challenges and the need for reliable emergency communication systems in crisis scenarios.
