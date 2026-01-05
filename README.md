# Starlink Connectivity Tools

A Python tool to monitor and optimize Starlink satellite connectivity in crisis scenarios.

This script uses the `starlink-client` library to periodically check network stats, detect connectivity issues, and take automated actions like rebooting the dish if needed. Inspired by use cases in areas like Venezuela where reliable internet is critical during crises.

## Features

- **Continuous Monitoring**: Periodically checks Starlink network statistics
- **Health Detection**: Monitors multiple connectivity metrics against configurable thresholds
- **Automated Recovery**: Automatically reboots the dish after consecutive failures
- **Comprehensive Logging**: Logs all connectivity data to rotating log files for historical tracking
- **Configurable Thresholds**: Customize what constitutes a connectivity issue
- **Crisis-Ready**: Designed for scenarios where reliable internet is critical

## Installation

1. Clone this repository:
```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install the starlink-client library directly:
```bash
pip install starlink-client
```

## Usage

### Basic Usage

Run the monitor with default settings:
```bash
python starlink_monitor.py
```

### Advanced Usage

Customize monitoring parameters:
```bash
python starlink_monitor.py --interval 30 --max-latency 150 --min-download 25
```

### Command Line Options

- `--interval SECONDS`: Seconds between connectivity checks (default: 60)
- `--log-file PATH`: Path to log file (default: starlink_connectivity.log)
- `--max-latency MS`: Maximum acceptable ping latency in milliseconds (default: 100)
- `--min-download MBPS`: Minimum acceptable download speed in Mbps (default: 50)
- `--failures-before-reboot COUNT`: Number of consecutive failures before triggering reboot (default: 3)

### Example Commands

Monitor with shorter interval for critical scenarios:
```bash
python starlink_monitor.py --interval 30 --failures-before-reboot 5
```

Monitor with relaxed thresholds for challenging conditions:
```bash
python starlink_monitor.py --max-latency 200 --min-download 10
```

Use a custom log file location:
```bash
python starlink_monitor.py --log-file /var/log/starlink/monitor.log
```

## Monitored Metrics

The tool monitors the following connectivity metrics:

1. **Uptime**: Ensures the dish has been stable for a minimum period
2. **Ping Latency**: Checks for acceptable response times (default: < 100ms)
3. **Ping Drop Rate**: Monitors packet loss (default: < 5%)
4. **Download Speed**: Ensures minimum throughput (default: > 50 Mbps)
5. **Upload Speed**: Ensures minimum upload capability (default: > 5 Mbps)
6. **Obstruction Percentage**: Monitors physical obstructions (default: < 5%)

## Configuration

You can customize thresholds by modifying the `DEFAULT_CONFIG` dictionary in `starlink_monitor.py` or by using command-line arguments.

See `config.example.yml` for a reference configuration file with all available options.

### Default Thresholds

```python
check_interval: 60 seconds
max_ping_latency_ms: 100
max_ping_drop_rate: 5%
min_download_mbps: 50
min_upload_mbps: 5
max_obstruction_percentage: 5%
consecutive_failures_before_reboot: 3
```

## Logging

The tool maintains detailed logs in rotating log files:
- **Log file**: `starlink_connectivity.log` (configurable)
- **Max size**: 10 MB per file
- **Backup count**: 5 files
- **Format**: Timestamp, level, and detailed message

Logs include:
- Periodic connectivity statistics
- Health check results
- Issue detection with specific metrics
- Automated action triggers (reboots)
- Error conditions

## Use Cases

### Crisis Scenarios

In areas experiencing political or social crises where internet connectivity is vital:
- Monitor connection stability 24/7
- Automatically recover from connectivity issues
- Maintain historical logs for analysis
- Ensure critical communications remain available

### Remote Locations

For Starlink installations in remote areas:
- Detect and resolve issues without physical access
- Monitor environmental impacts (obstructions)
- Track performance trends over time

### Business Continuity

For organizations relying on Starlink for connectivity:
- Ensure SLA compliance
- Proactive issue detection
- Automated recovery reduces downtime

## Requirements

- Python 3.7+
- `starlink-client` library
- Network access to Starlink dish (typically via local network)

## How It Works

1. **Connection**: Establishes connection to the Starlink dish via the starlink-client library
2. **Monitoring Loop**: Continuously retrieves network statistics at configured intervals
3. **Health Check**: Compares metrics against configured thresholds
4. **Issue Detection**: Logs any metrics that fall outside acceptable ranges
5. **Automated Action**: After consecutive failures, triggers dish reboot
6. **Recovery**: Waits for dish to stabilize after reboot before resuming monitoring

## Troubleshooting

### Cannot connect to Starlink dish
- Ensure you're on the same network as the Starlink dish
- Check that the dish is powered on and operational
- Verify the starlink-client library is correctly installed

### Too many false positives
- Adjust thresholds to match your environment
- Increase `consecutive_failures_before_reboot` to reduce sensitivity
- Consider local factors (weather, obstructions) when setting thresholds

### Logs growing too large
- Adjust `log_max_bytes` and `log_backup_count` in the configuration
- Consider implementing external log rotation or archival

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

See LICENSE file for details.

## Acknowledgments

Inspired by the need for reliable internet connectivity in crisis scenarios, particularly in regions like Venezuela where communication infrastructure is critical for safety and coordination.