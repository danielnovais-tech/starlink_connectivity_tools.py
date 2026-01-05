# Starlink Connectivity Tools

**Crisis-optimized satellite connectivity monitoring and management tools**

A comprehensive Python toolkit for managing Starlink connectivity in challenging environments, with real-time monitoring, automatic failover, and crisis-specific optimizations.

## Features

### 🛰️ **Starlink API Integration**
- Uses official `starlink-grpc` library for real device communication
- Real-time monitoring of dish status, obstructions, and performance metrics
- Automated issue detection and recovery (reboot, stow/unstow)
- Support for simulation mode when hardware isn't available

### 🔄 **Unified Connection Management**
- Manage multiple satellite connections (Starlink, Iridium, Inmarsat, Thuraya)
- Real metrics from Starlink API instead of simulated data
- Automatic failover between primary and backup connections
- Priority-based connection selection

### 🚨 **Crisis-Optimized Monitoring**
- Pre-configured scenarios: Normal, Humanitarian, Medical, Disaster, Conflict
- Adjustable thresholds for different crisis situations
- Persistent issue detection with automatic recovery
- Performance history tracking and reporting

### 💻 **Command-Line Tools**
- `starlink-monitor` CLI for easy monitoring and management
- Real-time status display with color-coded alerts
- Performance reporting and data export
- Quick access to reboot, stow/unstow commands

### 🎯 **Scenario-Specific Examples**
- Venezuela crisis scenario with realistic challenges
- Medical mission simulation with connectivity optimization
- Power outage, network congestion, and restriction simulations

### 🔍 **Enhanced Diagnostics**
- Integrated Starlink telemetry with diagnostic tools
- Historical performance tracking
- Automated alerting and issue resolution
- Comprehensive diagnostic reports

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Dependencies

- Python 3.8+
- starlink-grpc >= 1.2.0
- click >= 8.1.0
- rich >= 13.0.0
- numpy >= 1.24.0
- pandas >= 2.0.0
- loguru >= 0.7.0

## Quick Start

### Using the CLI

```bash
# Check Starlink status
starlink-monitor status

# Start real-time monitoring (normal scenario)
starlink-monitor monitor --interval 10

# Monitor with crisis scenario
starlink-monitor monitor --scenario humanitarian

# Generate performance report
starlink-monitor report --hours 24 --output report.json

# Run diagnostics
starlink-monitor diagnostics

# Reboot dish
starlink-monitor reboot

# Use simulation mode (no hardware required)
starlink-monitor status --simulation
starlink-monitor monitor --simulation --scenario disaster
```

### Using as a Library

```python
from starlink_connectivity_tools import (
    StarlinkAPI,
    SatelliteConnectionManager,
    CrisisMonitor,
    DiagnosticsEngine,
)
from starlink_connectivity_tools.satellite_connection_manager import ConnectionType
from starlink_connectivity_tools.crisis_monitor import ScenarioType

# Initialize Starlink API
api = StarlinkAPI(simulation_mode=True)  # Set False for real hardware

# Get status
status = api.get_status()
print(f"Latency: {status['ping_latency_ms']} ms")
print(f"Downlink: {status['downlink_throughput_bps'] / 1_000_000} Mbps")

# Setup connection manager with failover
manager = SatelliteConnectionManager()
manager.add_connection("Starlink Primary", ConnectionType.STARLINK, priority=100)
manager.add_connection("Iridium Backup", ConnectionType.IRIDIUM, priority=50)
manager.connect()

# Setup crisis monitoring
monitor = CrisisMonitor(manager, scenario=ScenarioType.HUMANITARIAN)
health = monitor.check_health()
print(f"Status: {health['status']}")

# Run diagnostics
diagnostics = DiagnosticsEngine(manager)
report = diagnostics.run_full_diagnostic()
print(f"Overall status: {report['status']}")

# Cleanup
manager.close_all()
api.close()
```

## Crisis Scenarios

The toolkit includes pre-configured monitoring scenarios optimized for different crisis situations:

| Scenario | Max Latency | Min Bandwidth | Obstruction Tolerance | Use Case |
|----------|-------------|---------------|----------------------|----------|
| **Normal** | 100ms | 20 Mbps | 5% | Standard operations |
| **Humanitarian** | 200ms | 10 Mbps | 15% | Aid coordination |
| **Medical** | 150ms | 15 Mbps | 10% | Telemedicine |
| **Disaster** | 300ms | 5 Mbps | 25% | Emergency response |
| **Conflict** | 250ms | 8 Mbps | 20% | Restricted areas |

You can also create custom scenarios:

```python
monitor.set_custom_thresholds({
    "max_latency_ms": 180,
    "min_downlink_mbps": 12,
    "min_uplink_mbps": 4,
    "max_obstruction_percent": 0.15,
    "min_snr": 6.0,
})
```

## Example Scenarios

The `examples/` directory contains realistic crisis simulations:

### Venezuela Crisis Scenario
```bash
python examples/venezuela_crisis_scenario.py
```
Demonstrates multi-satellite failover, network restrictions, and automatic recovery.

### Medical Mission Scenario
```bash
python examples/medical_mission_scenario.py
```
Shows activity-based monitoring with medical-specific requirements.

### Power & Network Challenges
```bash
python examples/power_network_scenario.py
```
Simulates power outages, network congestion, and equipment failures.

See [examples/README.md](examples/README.md) for detailed documentation.

## Architecture

```
starlink_connectivity_tools/
├── starlink_api.py              # Starlink gRPC integration
├── satellite_connection_manager.py  # Multi-satellite management
├── crisis_monitor.py            # Crisis-optimized monitoring
├── diagnostics.py               # Enhanced diagnostics
└── starlink_monitor_cli.py      # Command-line interface
```

## Real vs Simulation Mode

### Real Mode
- Requires Starlink dish connected to network
- Default target: `192.168.100.1:9200`
- Provides actual telemetry data
- Can control dish (reboot, stow/unstow)

```python
api = StarlinkAPI()  # Real mode
manager.add_connection("Starlink", ConnectionType.STARLINK, simulation_mode=False)
```

### Simulation Mode
- No hardware required
- Generates realistic synthetic data
- Perfect for testing and development
- All features work without dish

```python
api = StarlinkAPI(simulation_mode=True)  # Simulation mode
manager.add_connection("Starlink", ConnectionType.STARLINK, simulation_mode=True)
```

## Monitoring Features

### Real-time Metrics
- Latency (ping to Starlink PoP)
- Downlink/uplink throughput
- Signal-to-noise ratio (SNR)
- Obstruction percentage
- Dish state and alerts

### Automatic Recovery
- Connection failure detection
- Automatic reboot on persistent issues
- Failover to backup connections
- Issue resolution tracking

### Performance History
- Time-series data collection
- Statistical analysis (avg, min, max, percentiles)
- Long-term trend tracking
- Export to JSON for analysis

### Alerts & Diagnostics
- Hardware alerts (motors stuck, thermal issues)
- Performance degradation detection
- Obstruction analysis with directional info
- Actionable recommendations

## Use Cases

### 🏥 **Medical Missions**
Ensure reliable connectivity for telemedicine with automatic failover and low-latency monitoring.

### 🌍 **Humanitarian Aid**
Coordinate relief efforts in challenging environments with crisis-optimized thresholds.

### ⚠️ **Disaster Response**
Maintain communications during emergencies with automatic recovery and redundant connections.

### 🌐 **Remote Operations**
Monitor and manage satellite connectivity in areas with limited infrastructure.

## Development

### Running Tests
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of the excellent [starlink-grpc](https://github.com/sparky8512/starlink-grpc-tools) library
- Designed for crisis response and humanitarian applications
- Inspired by real-world connectivity challenges in remote areas

## Disclaimer

This is an independent project and is not affiliated with, endorsed by, or supported by SpaceX or Starlink. Use at your own risk. The authors are not responsible for any issues arising from the use of this software.

## Support

For issues, questions, or contributions, please use the [GitHub issue tracker](https://github.com/danielnovais-tech/starlink_connectivity_tools.py/issues).