# Starlink Connectivity Tools Examples

This directory contains example scripts demonstrating the usage of the Starlink Connectivity Tools library.

## Emergency Mode Example

The emergency mode example (`emergency_mode.py`) demonstrates how to monitor a Starlink dish for emergency conditions and take protective actions.

### Features

- Real-time dish status monitoring
- Emergency condition detection (motor issues, obstructions, thermal problems)
- Automatic protective actions (stowing the dish)
- Continuous monitoring mode
- Interactive user prompts for emergency decisions

### Usage

```bash
python examples/emergency_mode.py
```

### What it demonstrates

1. **Connection Management**: Establishing and maintaining connection to the Starlink dish
2. **Status Monitoring**: Reading and displaying dish status information
3. **Emergency Detection**: Checking for various emergency conditions:
   - Motor stuck
   - High obstruction percentage
   - Thermal throttling
   - High latency
4. **Emergency Actions**: 
   - Stowing the dish for protection
   - Rebooting the dish
   - Unstowing after emergency
5. **Continuous Monitoring**: Running periodic checks to detect issues early

### Emergency Conditions

The example monitors for:

- **MOTOR_STUCK**: Dish motor is not functioning properly
- **HIGH_OBSTRUCTION**: Objects blocking the dish's view (>10%)
- **THERMAL_THROTTLE**: Dish is overheating and limiting performance
- **HIGH_LATENCY**: Network latency exceeds acceptable thresholds (>100ms)

### Example Output

```
╔══════════════════════════════════════════════════════════════╗
║   STARLINK CONNECTIVITY TOOLS - EMERGENCY MODE EXAMPLE       ║
╚══════════════════════════════════════════════════════════════╝

Attempting to connect to Starlink dish at 192.168.100.1:9200...
✓ Connected successfully

📊 Fetching current dish status...

============================================================
STARLINK DISH STATUS
============================================================
Uptime:                  45821 seconds
Connected Satellites:    6
Downlink Throughput:     125.34 Mbps
Uplink Throughput:       25.67 Mbps
Ping Latency:            35.20 ms
Obstructed:              NO ✓
Obstruction Percentage:  2.45%
Stowed:                  NO
Heating:                 NO
Motor Stuck:             NO ✓
Thermal Throttle:        NO ✓
Unexpected Outages:      1
============================================================
```

## Note

This is a simulated implementation for demonstration purposes. In a production environment, it would connect to an actual Starlink dish using the gRPC API at 192.168.100.1:9200.
