# Starlink Connectivity Tools

Python library for interacting with the Starlink API. This library provides a simple and intuitive interface to access Starlink's various API endpoints.

## Installation

```bash
pip install starlink-connectivity-tools
```

Or install from source:

```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
pip install -e .
```

## Requirements

- Python 3.7+
- requests >= 2.25.0

## Quick Start

```python
from starlink_connectivity_tools import StarlinkClient, AccountsAPI, AddressesAPI

# Initialize the client
client = StarlinkClient(base_url="https://api.starlink.com", api_key="your_api_key")

# Get account information
accounts_api = AccountsAPI(client)
account = accounts_api.get_account()
print(f"Email: {account['email']}")

# Create a new address
addresses_api = AddressesAPI(client)
address = addresses_api.create_address({
    'street': '123 Main St',
    'city': 'Seattle',
    'state': 'WA',
    'zip': '98101'
})
print(f"Address ID: {address['id']}")
```

## API Endpoints

This library provides access to the following Starlink API endpoints:

### Accounts
- `GET /account` - Retrieve account details (email, customer info)

```python
from starlink_connectivity_tools import StarlinkClient, AccountsAPI

client = StarlinkClient(api_key="your_api_key")
accounts = AccountsAPI(client)
account = accounts.get_account()
```

### Addresses
- `POST /addresses` - Create a new address for service activation
- `GET /addresses/{id}` - Get details of a specific address

```python
from starlink_connectivity_tools import StarlinkClient, AddressesAPI

client = StarlinkClient(api_key="your_api_key")
addresses = AddressesAPI(client)

# Create address
new_address = addresses.create_address({
    'street': '123 Main St',
    'city': 'Seattle',
    'state': 'WA',
    'zip': '98101'
})

# Get address
address = addresses.get_address('addr_12345')
```

### Data Usage
- `GET /data-usage` - Fetch data usage statistics for the account or devices

```python
from starlink_connectivity_tools import StarlinkClient, DataUsageAPI

client = StarlinkClient(api_key="your_api_key")
data_usage = DataUsageAPI(client)
usage = data_usage.get_data_usage()
```

### Routers
- `GET /routers/{id}/config` - Get router configuration

```python
from starlink_connectivity_tools import StarlinkClient, RoutersAPI

client = StarlinkClient(api_key="your_api_key")
routers = RoutersAPI(client)
config = routers.get_router_config('router_12345')
```

### Service Lines
- `POST /service-lines` - Create a new service line (for activation)
- `GET /service-lines/{id}` - Retrieve service line details

```python
from starlink_connectivity_tools import StarlinkClient, ServiceLinesAPI

client = StarlinkClient(api_key="your_api_key")
service_lines = ServiceLinesAPI(client)

# Create service line
new_line = service_lines.create_service_line({
    'address_id': 'addr_12345',
    'product_id': 'prod_12345'
})

# Get service line
line = service_lines.get_service_line('line_12345')
```

### Subscriptions
- `GET /subscriptions` - List available or active subscription products

```python
from starlink_connectivity_tools import StarlinkClient, SubscriptionsAPI

client = StarlinkClient(api_key="your_api_key")
subscriptions = SubscriptionsAPI(client)
subs = subscriptions.get_subscriptions()
```

### User Terminals
- `GET /user-terminals/{id}` - Get user terminal (dish) details, including ID
- `POST /user-terminals` - Activate or manage a user terminal

```python
from starlink_connectivity_tools import StarlinkClient, UserTerminalsAPI

client = StarlinkClient(api_key="your_api_key")
terminals = UserTerminalsAPI(client)

# Get terminal
terminal = terminals.get_user_terminal('term_12345')

# Create/activate terminal
new_terminal = terminals.create_user_terminal({
    'service_line_id': 'line_12345',
    'serial_number': 'SN12345'
})
```

### TLS
- `GET /tls` - Retrieve TLS configuration for secure communications

```python
from starlink_connectivity_tools import StarlinkClient, TLSAPI

client = StarlinkClient(api_key="your_api_key")
tls = TLSAPI(client)
config = tls.get_tls_config()
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=starlink_connectivity_tools tests/
```

### Running Tests with unittest

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This library is not officially affiliated with or endorsed by Starlink or SpaceX. Use at your own risk. Always refer to the official Starlink API documentation for the most up-to-date information.