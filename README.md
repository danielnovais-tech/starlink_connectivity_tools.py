# Starlink Connectivity Tools

A Python package for interacting with Starlink-related APIs, focusing on space traffic coordination and satellite operations.

## Features

### Starlink Space Safety API

The Space Safety API is hosted at `space-safety.starlink.com` and provides tools for satellite operators to:

- **Submit ephemeris files**: Upload orbital data for your satellites
- **Screen against Starlink constellation**: Check for potential conjunctions
- **Coordinate space traffic**: Ensure safe operations in shared orbital space

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

## Usage

### Basic Example

```python
from starlink_connectivity_tools import SpaceSafetyAPI

# Initialize the API client
api = SpaceSafetyAPI(api_key="your_api_key_here")

# Submit ephemeris data
ephemeris_data = {
    "satellite_id": "SAT-001",
    "epoch": "2026-01-05T12:00:00Z",
    "state_vector": {
        "position": [7000.0, 0.0, 0.0],  # km
        "velocity": [0.0, 7.5, 0.0]  # km/s
    }
}

response = api.submit_ephemeris(ephemeris_data)
print(f"Submission ID: {response['submission_id']}")

# Screen for conjunctions
results = api.screen_conjunction("SAT-001")
print(f"Found {results['total_events']} potential conjunctions")

# Close the session
api.close()
```

### Using Context Manager

```python
from starlink_connectivity_tools import SpaceSafetyAPI

with SpaceSafetyAPI(api_key="your_api_key_here") as api:
    # Submit an ephemeris file
    result = api.submit_ephemeris_file(
        file_path="/path/to/ephemeris.oem",
        file_format="oem"
    )
    
    # Get constellation data
    constellation = api.get_starlink_constellation_data(
        filters={"active_only": True}
    )
    print(f"Active satellites: {len(constellation)}")
```

### Screening for Conjunctions

```python
from starlink_connectivity_tools import SpaceSafetyAPI

api = SpaceSafetyAPI(api_key="your_api_key_here")

# Screen with a specific time window
time_window = {
    "start": "2026-01-05T00:00:00Z",
    "end": "2026-01-12T00:00:00Z"
}

results = api.screen_conjunction("SAT-001", time_window=time_window)

for conjunction in results['conjunctions']:
    print(f"Potential conjunction with {conjunction['starlink_satellite_id']}")
    print(f"  Time: {conjunction['time_of_closest_approach']}")
    print(f"  Miss distance: {conjunction['miss_distance']} km")
    print(f"  Collision probability: {conjunction['probability_of_collision']}")
```

### Checking Submission Status

```python
from starlink_connectivity_tools import SpaceSafetyAPI

api = SpaceSafetyAPI(api_key="your_api_key_here")

# After submitting ephemeris data
response = api.submit_ephemeris(ephemeris_data)
submission_id = response['submission_id']

# Check status later
status = api.get_screening_status(submission_id)
print(f"Status: {status['status']}")

if status['status'] == 'completed':
    print("Results:", status['results'])
```

## API Reference

### SpaceSafetyAPI

#### Constructor

```python
SpaceSafetyAPI(api_key=None, base_url="https://space-safety.starlink.com")
```

**Parameters:**
- `api_key` (str, optional): API key for authentication
- `base_url` (str): Base URL for the API

#### Methods

##### submit_ephemeris(ephemeris_data)

Submit ephemeris data for a satellite.

**Parameters:**
- `ephemeris_data` (dict): Dictionary containing orbital parameters

**Returns:** dict with submission confirmation

##### submit_ephemeris_file(file_path, file_format="oem")

Upload an ephemeris file.

**Parameters:**
- `file_path` (str): Path to the ephemeris file
- `file_format` (str): Format of the file (e.g., "oem", "tle")

**Returns:** dict with upload confirmation

##### screen_conjunction(satellite_id, time_window=None)

Screen for potential conjunctions with Starlink satellites.

**Parameters:**
- `satellite_id` (str): Satellite identifier
- `time_window` (dict, optional): Time range for screening

**Returns:** dict with conjunction results

##### get_starlink_constellation_data(filters=None)

Retrieve current Starlink constellation data.

**Parameters:**
- `filters` (dict, optional): Filters for constellation data

**Returns:** list of satellite data

##### get_screening_status(submission_id)

Get the status of a previous submission.

**Parameters:**
- `submission_id` (str): Submission ID from previous request

**Returns:** dict with status information

## Important Notes

### Starlink-UK API Clarification

⚠️ **Important**: The "Starlink-UK API" is NOT related to SpaceX's Starlink satellite constellation. It is an unrelated astronomical software API from the University of Bristol for analyzing stellar populations.

This package focuses exclusively on SpaceX Starlink-related APIs for satellite connectivity and space traffic coordination.

For more information, see [STARLINK_UK_NOTE.md](starlink_connectivity_tools/STARLINK_UK_NOTE.md).

### Official Resources

For official updates and documentation:
- **Starlink Support Portal**: https://support.starlink.com
- **Space Safety API**: https://space-safety.starlink.com
- **Developer Resources**: Check Starlink's official channels for API updates

## Requirements

- Python 3.7+
- requests >= 2.25.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See [LICENSE](LICENSE) file for details.

## Disclaimer

This is an unofficial package. For official Starlink services and support, please visit https://starlink.com.

APIs may evolve over time. Check official Starlink resources for the latest updates.