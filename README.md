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

No external dependencies are required for the basic examples.

## Usage

### Emergency Mode Example

The emergency mode example demonstrates how to monitor and recover from connectivity issues:

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