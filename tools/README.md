# Starlink Connectivity Tools

## starlink_simple_monitor.py

A standalone Python tool to monitor and optimize Starlink satellite connectivity in crisis scenarios.

### Features

- **Network Monitoring**: Track download/upload speeds, latency, jitter, and packet loss
- **Automatic Recovery**: Auto-reboot dish on persistent connectivity issues
- **Crisis Mode**: Relaxed thresholds for emergency situations (inspired by Venezuela use cases)
- **Performance Reporting**: Generate detailed JSON reports of network performance
- **Flexible Configuration**: Support for JSON config files and command-line arguments
- **Multiple Operation Modes**: Single check, continuous monitoring, report generation, and more

### Installation

```bash
pip install starlink-client
```

### Quick Start

```bash
# Start continuous monitoring with default settings
python starlink_simple_monitor.py

# Run a single connectivity check
python starlink_simple_monitor.py --single-check

# Enable crisis mode for emergency situations
python starlink_simple_monitor.py --crisis-mode

# Generate a performance report
python starlink_simple_monitor.py --report --hours 24

# Use custom configuration file
python starlink_simple_monitor.py --config my_config.json
```

### Configuration

Create a JSON configuration file with custom settings:

```json
{
  "min_download_speed": 5.0,
  "max_latency": 100,
  "max_packet_loss": 10,
  "check_interval": 60,
  "max_issue_count": 3,
  "crisis_mode": false,
  "enable_auto_recovery": true,
  "notify_on_issues": true,
  "auto_reboot_on_persistent_issues": true,
  "webhook_url": null
}
```

### Command-Line Options

```
--host IP              Starlink router IP address (default: 192.168.100.1)
--interval SECONDS     Check interval in seconds (default: 60)
--min-download MBPS    Minimum acceptable download speed (default: 5.0)
--max-latency MS       Maximum acceptable latency (default: 100)
--max-issues COUNT     Consecutive issues before action (default: 3)
--crisis-mode          Enable crisis mode with relaxed thresholds
--single-check         Run a single check and exit
--reboot               Reboot Starlink dish and exit
--report               Generate performance report and exit
--hours HOURS          Hours of data for report (default: 24)
--config FILE          JSON configuration file
--log-file FILE        Log file path (default: starlink_log.txt)
--export-logs          Export logs to JSON file and exit
```

### Crisis Mode

Crisis mode is designed for situations where any connectivity is better than none. It relaxes the monitoring thresholds while maintaining automatic recovery features.

Inspired by connectivity challenges in regions like Venezuela where internet access can be critical for communication and safety.

```bash
python starlink_simple_monitor.py --crisis-mode
```

### Use Cases

1. **Remote Work**: Ensure stable connectivity for critical work
2. **Emergency Communication**: Maintain internet access during crisis situations
3. **Network Monitoring**: Track and log Starlink performance over time
4. **Automated Recovery**: Reduce manual intervention for connectivity issues
5. **Performance Analysis**: Generate reports to understand network patterns

### Output Files

- `starlink_log.txt` - Continuous log of monitoring events
- `starlink_report_*.json` - Performance reports
- `starlink_logs_*.json` - Exported logs with full history
- `starlink_final_*.json` - Final session reports

All generated files are automatically excluded from git via `.gitignore`.

### License

See LICENSE file in the repository root.
