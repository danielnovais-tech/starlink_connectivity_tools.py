# Starlink Connectivity Tools

Python library for monitoring and managing Starlink dish connectivity with emergency mode support.

## Features

- Monitor Starlink dish status in real-time
- Detect emergency conditions (motor issues, obstructions, thermal problems)
- Emergency actions (stow/unstow dish, reboot)
- Simulated dish interface for testing and development

## Installation

```bash
# Clone the repository
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py

# Install in development mode
pip install -e .
```

## Quick Start

```python
from starlink_connectivity_tools import StarlinkDish

# Connect to the dish
with StarlinkDish() as dish:
    # Get status
    status = dish.get_status()
    print(f"Connected satellites: {status['connected_satellites']}")
    
    # Check for emergencies
    emergency = dish.check_emergency_conditions()
    if emergency:
        print(f"Emergency detected: {emergency}")
        dish.stow()  # Protective action
```

## Usage Examples

### Emergency Mode Example

Run the comprehensive emergency mode example:

```bash
python examples/emergency_mode.py
```

This example demonstrates:
- Real-time status monitoring
- Emergency condition detection
- Interactive emergency handling
- Continuous monitoring mode

See [examples/README.md](examples/README.md) for more details.

## API Overview

### StarlinkDish Class

Main interface for interacting with Starlink dish.

**Methods:**
- `connect()` - Establish connection to dish
- `disconnect()` - Disconnect from dish
- `get_status()` - Get current dish status
- `check_emergency_conditions()` - Check for emergency conditions
- `stow()` - Stow dish to emergency position
- `unstow()` - Return dish to normal operation
- `reboot()` - Reboot the dish

**Context Manager Support:**
```python
with StarlinkDish() as dish:
    # Automatic connection and cleanup
    status = dish.get_status()
```

## Emergency Conditions

The library monitors for various emergency conditions:

- **MOTOR_STUCK**: Dish motor malfunction
- **HIGH_OBSTRUCTION**: Objects blocking dish view (>10%)
- **THERMAL_THROTTLE**: Overheating causing performance degradation
- **HIGH_LATENCY**: Network latency exceeding thresholds (>100ms)

## Development

This is a simulated implementation for demonstration and testing. In production, it would connect to an actual Starlink dish via gRPC at `192.168.100.1:9200`.

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.