# Example Scenarios

This directory contains realistic crisis scenarios demonstrating the capabilities of the Starlink Connectivity Tools.

## Available Scenarios

### 1. Venezuela Crisis Scenario (`venezuela_crisis_scenario.py`)

Simulates humanitarian aid coordination in a challenging environment with:
- Intermittent power outages
- Government network restrictions
- Limited backup connectivity options
- Environmental obstructions
- Automatic failover between Starlink and backup satellites

**Run:**
```bash
python examples/venezuela_crisis_scenario.py
```

**Features Demonstrated:**
- Multi-satellite failover
- Crisis-optimized monitoring (CONFLICT scenario)
- Automatic issue detection and recovery
- Performance tracking and reporting

---

### 2. Medical Mission Scenario (`medical_mission_scenario.py`)

Simulates a remote medical clinic with critical connectivity requirements:
- Telemedicine consultations requiring low latency (<150ms)
- Medical imaging transfers requiring stable bandwidth
- Emergency communication with automatic failover
- Activity-specific connection requirements

**Run:**
```bash
python examples/medical_mission_scenario.py
```

**Features Demonstrated:**
- Medical scenario thresholds (MEDICAL scenario)
- Custom threshold configuration
- Activity-based monitoring
- Redundant connection management

---

### 3. Power & Network Challenges (`power_network_scenario.py`)

Simulates disaster response coordination with:
- Power outages requiring rapid reconnection
- Network congestion during peak usage
- Equipment failures
- Multiple simultaneous issues

**Run:**
```bash
python examples/power_network_scenario.py
```

**Features Demonstrated:**
- Disaster scenario thresholds
- Rapid recovery mechanisms
- Multiple Starlink dishes for redundancy
- Event-based stress testing

---

## Output Files

Each scenario generates data files:
- `*_simulation.json` - Performance data and metrics
- `*_diagnostics.json` - Diagnostic reports and alerts

## Customization

You can modify scenarios by:
1. Adjusting simulation duration
2. Changing scenario thresholds
3. Adding/removing backup connections
4. Customizing challenge events

## Requirements

All examples use simulation mode by default, so they don't require actual Starlink hardware. To use with real hardware, modify the `simulation_mode` parameter.
