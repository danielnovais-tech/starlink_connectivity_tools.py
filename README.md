# Starlink Connectivity Tools

A comprehensive Python toolkit for managing, monitoring, and optimizing Starlink satellite internet connections. This project provides essential tools for connection management, bandwidth optimization, power management, failover handling, and real-time monitoring.

## 🌟 Features

- **Connection Management**: Intelligent Starlink connection handling with automatic reconnection and health monitoring
- **Bandwidth Optimization**: Traffic shaping, QoS, and bandwidth allocation strategies
- **Power Management**: Multiple power modes for battery operation and emergency scenarios
- **Failover Handling**: Automatic failover between Starlink and backup connections
- **Real-time Monitoring**: Live metrics tracking including signal quality, satellites, latency, and throughput
- **Diagnostics**: Comprehensive diagnostic tools for troubleshooting
- **Web Dashboard**: User-friendly web interface for monitoring and control
- **CLI Tools**: Command-line tools for monitoring and management

## 📋 Project Structure

```
starlink-connectivity-tools/
├── src/
│   ├── __init__.py
│   ├── connection_manager.py      # Starlink connection management
│   ├── bandwidth_optimizer.py     # Bandwidth optimization
│   ├── failover_handler.py        # Failover management
│   ├── power_manager.py           # Power consumption management
│   ├── diagnostics.py             # Diagnostic tools
│   ├── starlink_monitor.py        # Real-time monitoring
│   └── config/
│       └── settings.py            # Configuration settings
├── tools/
│   ├── starlink_monitor_cli.py    # Command-line monitoring tool
│   └── connectivity_dashboard.py  # Web dashboard
├── examples/
│   ├── emergency_mode.py          # Emergency mode example
│   ├── venezuela_scenario.py      # Venezuela scenario example
│   └── low_power_mode.py          # Low power mode example
├── requirements.txt
├── setup.py
└── README.md
```

## 🚀 Installation

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### With Web Dashboard Support

```bash
pip install -e .[web]
```

### Development Installation

```bash
pip install -e .[dev]
```

## 📖 Usage

### Python Library

```python
from src.connection_manager import ConnectionManager
from src.starlink_monitor import StarlinkMonitor
from src.power_manager import PowerManager, PowerMode

# Initialize components
connection = ConnectionManager()
monitor = StarlinkMonitor()
power = PowerManager()

# Connect to Starlink
connection.connect()

# Get current metrics
metrics = monitor.get_current_metrics()
print(f"Signal Quality: {metrics['signal_quality']}%")
print(f"Download Speed: {metrics['download_mbps']} Mbps")

# Set power mode
power.set_power_mode(PowerMode.ECO)
```

### Command-Line Monitoring

```bash
# Live monitoring
python tools/starlink_monitor_cli.py monitor --interval 5

# Get statistics
python tools/starlink_monitor_cli.py stats --duration 60

# Run diagnostics
python tools/starlink_monitor_cli.py diagnostics

# Export metrics
python tools/starlink_monitor_cli.py export --format json --output metrics.json
```

### Web Dashboard

```bash
# Start the web dashboard
python tools/connectivity_dashboard.py --host 0.0.0.0 --port 5000

# Access at http://localhost:5000
```

### Examples

#### Emergency Mode
```bash
python examples/emergency_mode.py --simulate --duration 30
```

#### Venezuela Scenario (Power Outage Optimization)
```bash
python examples/venezuela_scenario.py --simulate-outage --duration 60
```

#### Low Power Mode
```bash
python examples/low_power_mode.py --battery 1000 --target-hours 12 --monitor
```

## 🔧 Configuration

Configuration can be customized via environment variables or by modifying `src/config/settings.py`:

```python
# Starlink Configuration
STARLINK_ENDPOINT = "192.168.100.1"
STARLINK_GRPC_PORT = 9200

# Monitoring Configuration
MONITOR_INTERVAL_SECONDS = 30
METRICS_HISTORY_SIZE = 100

# Alert Thresholds
ALERT_SIGNAL_QUALITY_MIN = 70
ALERT_LATENCY_MAX_MS = 100
```

## 🌍 Use Cases

### Emergency Communications
- Optimized for extended battery operation
- Critical services prioritization
- Minimal power consumption
- Automatic failover to backup connections

### Remote/Off-Grid Scenarios
- Power management for solar/battery systems
- Bandwidth optimization for limited capacity
- Real-time monitoring and alerts
- Diagnostic tools for troubleshooting

### Areas with Unreliable Power
- Automatic power mode adjustment
- Battery runtime estimation
- Failover to backup connections during outages
- Continuous monitoring even during transitions

## 📊 Monitoring Capabilities

- **Signal Quality**: Real-time signal strength monitoring
- **Satellite Tracking**: Number of visible satellites
- **Network Performance**: Latency, jitter, packet loss
- **Throughput**: Download/upload speeds
- **Obstructions**: Detection and analysis
- **Temperature**: Dish temperature monitoring
- **Alerts**: Configurable thresholds with notifications

## 🔋 Power Modes

- **Normal**: Full features, maximum performance
- **ECO**: Balanced power consumption and features
- **Low Power**: Extended battery life, essential features only
- **Emergency**: Maximum battery life, critical communications only

## 🔄 Failover Features

- Automatic detection of primary connection failures
- Seamless switching to backup connections
- Configurable failover thresholds
- Automatic restoration of primary connection
- Support for multiple backup connections

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This is an independent project and is not affiliated with, endorsed by, or connected to SpaceX or Starlink. Use at your own risk.

## 🙏 Acknowledgments

- Built for communities with challenging connectivity scenarios
- Inspired by real-world needs in areas with unreliable power and internet access
- Special consideration for scenarios like Venezuela where reliable communications are critical

## 📞 Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/danielnovais-tech/starlink_connectivity_tools.py).