# Starlink Connectivity Tools

A Python library for managing Starlink satellite connectivity with support for bandwidth optimization, connection management, and prioritized data transmission.

## Features

- **Bandwidth Optimization**: Efficiently allocate and manage bandwidth across multiple connections
- **Priority Management**: Prioritize critical connections (e.g., medical emergencies)
- **Connection Management**: Track and control multiple simultaneous connections
- **Use Cases**: Pre-built examples for common scenarios including medical emergency communications

## Installation

```bash
pip install starlink_connectivity_tools
```

Or install from source:

```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
pip install -e .
```

## Quick Start

```python
from starlink_connectivity import BandwidthOptimizer

# Initialize optimizer with available bandwidth
optimizer = BandwidthOptimizer(total_bandwidth=100.0)  # 100 Mbps

# Allocate bandwidth for a connection
allocation = optimizer.allocate_bandwidth(
    connection_id="my_connection",
    destination="data.endpoint",
    requested_bandwidth=10.0
)

print(f"Allocated: {allocation.allocated_bandwidth} Mbps")
print(f"Status: {allocation.status}")
```

## Use Cases

### Medical Emergency Communications

Prioritize medical data transmission during emergency situations:

```python
from starlink_connectivity import BandwidthOptimizer

optimizer = BandwidthOptimizer(total_bandwidth=100.0)

# Prioritize medical data transmission
optimizer.allocate_bandwidth(
    connection_id="medical_evac",
    destination="medical.data",
    requested_bandwidth=10.0
)
```

See the [examples/medical_emergency.py](examples/medical_emergency.py) for a complete medical emergency communications scenario.

## API Reference

### BandwidthOptimizer

Main class for managing bandwidth allocation.

#### Methods

- `allocate_bandwidth(connection_id, destination, requested_bandwidth, priority=0)`: Allocate bandwidth for a connection
- `release_bandwidth(connection_id)`: Release bandwidth from a connection
- `get_allocation(connection_id)`: Get allocation details for a connection
- `get_all_allocations()`: Get all current allocations
- `get_available_bandwidth()`: Get currently available bandwidth

## Running Examples

```bash
# Medical emergency communications example
python examples/medical_emergency.py
```

## Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_optimizer
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=starlink_connectivity tests/
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

This library is designed to work with Starlink satellite internet connections, providing tools for optimized bandwidth management in various scenarios including critical communications during emergencies.