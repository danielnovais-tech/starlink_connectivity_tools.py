# Venezuela Crisis Scenario Example

This example demonstrates Starlink connectivity optimization for crisis scenarios based on real challenges faced in Venezuela.

## Overview

The Venezuela Crisis Scenario simulates humanitarian operations using Starlink connectivity in challenging conditions including:
- Frequent power outages
- Limited battery capacity
- Network congestion
- Government restrictions
- Weather disruptions

## Features

- **Crisis Mode Configuration**: Optimizes all systems for low-resource environments
- **Event Simulation**: Simulates various crisis events (power outages, network congestion, etc.)
- **Medical Mission Simulation**: Demonstrates real-world humanitarian operations
- **Comprehensive Reporting**: Generates detailed JSON reports of operations
- **Failover Support**: Includes backup connections (mesh networks, satellite phones)

## Requirements

- Python 3.7+
- No external dependencies required (uses only standard library)

## Usage

### Run the Full Demonstration

```bash
cd /path/to/project
python3 examples/venezuela_scenario.py
```

The demonstration will:
1. Configure all systems for crisis mode
2. Establish Starlink connectivity
3. Simulate crisis events (power outage, network congestion)
4. Run a medical aid mission (1 hour in demo mode)
5. Generate a final report

### Use as a Library

```python
from examples.venezuela_scenario import VenezuelaCrisisScenario

# Initialize scenario
scenario = VenezuelaCrisisScenario()

# Setup crisis mode
scenario.setup_crisis_mode()

# Connect to Starlink
scenario.connection_manager.connect("starlink_satellite")

# Simulate specific events
scenario.simulate_crisis_event('power_outage')
scenario.simulate_crisis_event('network_congestion')
scenario.simulate_crisis_event('government_restriction')
scenario.simulate_crisis_event('weather_disruption')

# Run a medical mission
mission_data = scenario.run_medical_mission(duration_hours=6)
```

## Crisis Events

The scenario simulates four types of crisis events:

1. **Power Outage**
   - Switches to battery power
   - Enables power-saving sleep cycles
   - Prioritizes critical communications only

2. **Network Congestion**
   - Reduces bandwidth expectations
   - Enables data compression
   - Prioritizes text-based communications

3. **Government Restrictions**
   - Enables encrypted communications
   - Switches to alternative DNS
   - Sets up VPN/Proxy bypass mechanisms

4. **Weather Disruption**
   - Increases obstruction tolerance
   - Prepares for dish stow
   - Enables weather monitoring

## Output Files

The scenario generates several output files:

- `venezuela_scenario.log` - Detailed logging of all operations
- `venezuela_scenario_report.json` - Final scenario report
- `medical_mission_report.json` - Detailed medical mission results

## Critical Services

The scenario prioritizes the following services:

1. **Medical Supplies** (Critical Priority)
   - Required Bandwidth: 2.0 Mbps
   - Destinations: hospital.org, redcross.org

2. **SOS Messages** (Critical Priority)
   - Required Bandwidth: 0.5 Mbps
   - Destinations: sos.venezuela, emergency.comms

3. **Currency Exchange** (High Priority)
   - Required Bandwidth: 1.0 Mbps
   - Destinations: crypto.exchange, remittance.service

4. **News Information** (Medium Priority)
   - Required Bandwidth: 1.0 Mbps
   - Destinations: news.venezuela, independent.media

## Architecture

The scenario uses the following core modules from the `src/` directory:

- `connection_manager.py` - Manages Starlink and satellite connections
- `bandwidth_optimizer.py` - Optimizes bandwidth allocation
- `power_manager.py` - Manages power consumption and battery life
- `failover_handler.py` - Handles failover to backup connections
- `starlink_monitor.py` - Monitors Starlink health and performance

## Configuration

Key configuration parameters can be modified in the `VenezuelaCrisisScenario.__init__()` method:

```python
# Total bandwidth (Mbps)
BandwidthOptimizer(total_bandwidth=50.0)

# Battery capacity (Wh)
PowerManager(total_battery_capacity=300.0)

# Starlink router address
SatelliteConnectionManager(starlink_host="192.168.100.1")
```

## License

See LICENSE file for details.
