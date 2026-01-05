# starlink_connectivity_tools.py

A Python toolkit for monitoring and analyzing Starlink connectivity performance.

## Features

- Performance reporting over customizable time periods
- Data export to JSON format
- Command-line interface for easy access

## Installation

Clone the repository:

```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
```

## Usage

### Performance Reports

Generate a performance report for a specific time period:

```bash
python tools/starlink_monitor_cli.py report --hours 48
```

This command generates a performance report for the last 48 hours, showing metrics such as:
- Average latency
- Average download speed
- Average upload speed
- Uptime statistics

### Data Export

Export collected data to a JSON file:

```bash
python tools/starlink_monitor_cli.py export --output starlink_data.json
```

This command exports all collected metrics to the specified JSON file for further analysis or archival purposes.

### Help

View all available commands and options:

```bash
python tools/starlink_monitor_cli.py --help
```

View help for a specific command:

```bash
python tools/starlink_monitor_cli.py report --help
python tools/starlink_monitor_cli.py export --help
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.