# Starlink Client Examples

This directory contains example scripts demonstrating how to use the Starlink Client library.

## Prerequisites

Make sure you have:
1. Installed all dependencies: `pip install -r ../requirements.txt`
2. The protobuf files (`device_pb2.py` and `device_pb2_grpc.py`) in the parent directory
3. Access to Starlink devices on your network

## Running Examples

From this directory, run any example:

```bash
python basic_status.py
python get_diagnostics.py
python ping_monitoring.py
python speed_test.py
python device_info.py
python custom_addresses.py
```

## Example Descriptions

### basic_status.py
**Purpose:** Get basic status information from Starlink devices

Shows how to:
- Initialize the StarlinkClient
- Retrieve status from both router and dish
- Handle errors gracefully

**Output:** Status information in JSON format

---

### get_diagnostics.py
**Purpose:** Retrieve detailed diagnostics information

Shows how to:
- Get comprehensive diagnostics data
- Pretty print JSON output
- Separate router and dish diagnostics

**Output:** Formatted diagnostics for both devices

---

### ping_monitoring.py
**Purpose:** Monitor network metrics and ping latency

Shows how to:
- Retrieve ping metrics
- Display metrics in a readable format
- Implement continuous monitoring (commented out by default)

**Features:**
- Single metrics retrieval
- Continuous monitoring with configurable interval
- Graceful shutdown with Ctrl+C

**Output:** Ping metrics with timestamp

---

### speed_test.py
**Purpose:** Run and retrieve speed test results

Shows how to:
- Get last speed test results
- Run a new speed test
- Handle long-running operations

**Note:** Speed tests can take 20-30 seconds to complete

**Output:** Download/upload speeds and latency

---

### device_info.py
**Purpose:** Get detailed device information

Shows how to:
- Retrieve hardware/software info
- Display information for multiple devices
- Format output for readability

**Output:** Device details including firmware version, serial numbers, etc.

---

### custom_addresses.py
**Purpose:** Connect to devices at non-standard addresses

Shows how to:
- Initialize client with custom addresses
- Useful for special network configurations
- Override default gRPC endpoints

**Use Case:** When your Starlink devices are on different network segments or ports

---

## Modifying Examples

All examples are well-commented and can be easily modified for your needs:

1. Change device addresses in the `StarlinkClient()` initialization
2. Adjust monitoring intervals in `ping_monitoring.py`
3. Change output format (JSON vs pretty print)
4. Add error handling or logging as needed

## Continuous Monitoring

The `ping_monitoring.py` example includes a continuous monitoring function that's commented out by default. To enable it:

```python
# At the end of ping_monitoring.py, uncomment:
continuous_monitoring(interval=60)
```

This will check ping metrics every 60 seconds until stopped with Ctrl+C.

## Error Handling

All examples include basic error handling. Common errors:

- **Connection refused**: Starlink device not accessible
- **Timeout**: Device not responding within timeout period
- **gRPC errors**: Network issues or invalid requests

## Integration

These examples can be integrated into larger applications:

- Network monitoring dashboards
- Automated health checks
- Performance logging systems
- Alert systems for connectivity issues

## Next Steps

After running these examples, you can:
1. Integrate the client into your own applications
2. Build custom monitoring solutions
3. Create scheduled tasks for regular checks
4. Develop alerting systems based on metrics
# Examples

This directory contains example scripts demonstrating how to use the Starlink Connectivity Tools package.

## Available Examples

### 1. basic_usage.py
Basic introduction to the Space Safety API covering:
- Initializing the API client
- Submitting ephemeris data
- Screening for conjunctions
- Retrieving constellation data

**Run:**
```bash
python examples/basic_usage.py
```

### 2. file_upload.py
Demonstrates file-based ephemeris submission:
- Uploading OEM/TLE files
- Monitoring processing status
- Handling asynchronous operations

**Run:**
```bash
python examples/file_upload.py
```

### 3. advanced_screening.py
Advanced conjunction analysis including:
- Custom time window screening
- Risk categorization (HIGH/MEDIUM/LOW)
- Detailed event analysis
- Automated risk assessment

**Run:**
```bash
python examples/advanced_screening.py
```

## Configuration

### API Key

Set your API key as an environment variable:

```bash
export STARLINK_API_KEY="your_api_key_here"
```

Or in Python:
```python
import os
os.environ['STARLINK_API_KEY'] = 'your_api_key_here'
```

### Without API Key

The examples can run without an API key, but functionality may be limited depending on the API's authentication requirements.

## Notes

- These examples demonstrate the API interface and expected usage patterns
- Actual API responses will depend on the Space Safety API implementation
- Error handling is included to gracefully handle API unavailability
- The examples use realistic orbital parameters for demonstration purposes

## Requirements

Install the package and its dependencies:

```bash
pip install -e .
```

Or just the requirements:
```bash
pip install requests
```
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

STARLINK DISH STATUS
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
```

## Note

This is a simulated implementation for demonstration purposes. In a production environment, it would connect to an actual Starlink dish using the gRPC API at 192.168.100.1:9200.
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
