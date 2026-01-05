# starlink_connectivity_tools.py

A Python library for working with Starlink connectivity.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from starlink_connectivity_tools import StarlinkConnectivity, check_connection, format_speed

# Create a connectivity instance
conn = StarlinkConnectivity(dish_id="DISH-12345")

# Connect to the dish
conn.connect()

# Check connection status
print(conn.is_connected())  # True

# Get status
status = conn.get_status()
print(status)  # {'dish_id': 'DISH-12345', 'connected': True}

# Use utility functions
print(check_connection("DISH-12345"))  # True
print(format_speed(250.5))  # "250.50 Mbps"
print(format_speed(1500))  # "1.50 Gbps"
```

## Testing

Run the test suite using pytest:

```bash
python -m pytest tests/
```

Run tests with verbose output:

```bash
python -m pytest tests/ -v
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```