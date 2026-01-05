# Starlink Connectivity Tools

A comprehensive Python toolkit for managing satellite connectivity in emergency and crisis scenarios, with focus on power management and battery optimization for remote operations.

## Features

- **Power Management**: Battery optimization with multiple power modes for extended runtime
- **Component Control**: Manage individual components to optimize power consumption
- **Automatic Optimization**: Intelligent power mode selection based on target battery runtime
- **Sleep Scheduling**: Schedule periodic sleep/wake cycles for extreme power conservation

## Installation

```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
```

## Quick Start

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
```

## Use Cases

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

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Designed for reliable satellite connectivity in remote, off-grid, and emergency scenarios where power management is critical.