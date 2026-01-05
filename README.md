# Starlink Connectivity Tools

A comprehensive Python tool for monitoring and managing Starlink connectivity with advanced features designed for reliability in challenging network conditions.

## Features

### 1. Command-Line Interface
- **Multiple Operation Modes**: monitor, single-check, reboot, report
- **Comprehensive Argument Parsing**: Customizable thresholds and intervals
- **Flexible Configuration**: Command-line overrides for any setting

### 2. Crisis Mode
- **Emergency Operation**: Relaxed thresholds for critical situations
- **Automatic Adjustment**: Sensitivity adapts to scenario requirements
- **Venezuela-Inspired**: Designed for resilience in challenging environments

### 3. Enhanced Logging
- **Dual Output**: Logs to both file and console simultaneously
- **Structured Alerts**: Organized notification system with severity levels
- **Performance History**: Automatic tracking of connectivity metrics over time

### 4. Reporting
- **Comprehensive Reports**: Detailed performance statistics and analysis
- **JSON Export**: Export logs for external analysis tools
- **Statistics**: Success rate, latency metrics, packet loss tracking

### 5. Robust Error Handling
- **Graceful Failures**: Clean handling of connection failures
- **Auto-Reconnection**: Automatic retry attempts with backoff
- **Detailed Errors**: Clear, actionable error messages

### 6. Thread-Safe Monitoring
- **Background Operation**: Monitoring runs without blocking main thread
- **Clean Shutdown**: Graceful handling of interrupts (Ctrl+C)
- **Thread Safety**: Safe concurrent access to monitoring data

### 7. Configuration Management
- **JSON Config Files**: Store settings in easy-to-edit JSON format
- **Command-Line Override**: Override any config setting from CLI
- **Sensible Defaults**: Works out-of-the-box with reasonable settings

### 8. Venezuela-Inspired Features
- **Crisis Mode**: Tailored for emergency and low-connectivity scenarios
- **Intermittent Resilience**: Handles unstable connections gracefully
- **Essential Communications**: Prioritizes critical connectivity checks

## Installation

```bash
# Clone the repository
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py

# Make the script executable (Linux/Mac)
chmod +x starlink_connectivity.py

# No external dependencies required - uses Python standard library only!
```

## Quick Start

### Single Connectivity Check
```bash
python starlink_connectivity.py single-check
```

### Continuous Monitoring
```bash
# Monitor with default settings (60-second interval)
python starlink_connectivity.py monitor

# Monitor with custom interval
python starlink_connectivity.py monitor --interval 30

# Monitor for specific duration (1 hour)
python starlink_connectivity.py monitor --duration 3600
```

### Crisis Mode
```bash
# Enable crisis mode for emergency situations
python starlink_connectivity.py --crisis-mode monitor
```

### Generate Reports
```bash
# Print report to console
python starlink_connectivity.py report

# Save report to file
python starlink_connectivity.py report --output connectivity_report.json

# Export raw logs
python starlink_connectivity.py report --export-logs logs_export.json
```

## Configuration

### Create Configuration File
```bash
# Generate example configuration
python starlink_connectivity.py create-config --output my_config.json
```

### Configuration Options

```json
{
  "thresholds": {
    "ping_timeout": 5,
    "max_failures": 3,
    "min_success_rate": 0.8,
    "alert_latency_ms": 100
  },
  "crisis_thresholds": {
    "ping_timeout": 10,
    "max_failures": 5,
    "min_success_rate": 0.5,
    "alert_latency_ms": 300
  },
  "monitoring": {
    "check_interval": 60,
    "history_size": 1000
  },
  "logging": {
    "log_file": "starlink_monitor.log",
    "log_level": "INFO",
    "console_output": true
  },
  "starlink": {
    "dish_ip": "192.168.100.1",
    "router_ip": "192.168.1.1"
  },
  "notifications": {
    "enabled": false,
    "email": null,
    "webhook_url": null
  }
}
```

### Use Custom Configuration
```bash
python starlink_connectivity.py --config my_config.json monitor
```

## Usage Examples

### Monitor with verbose logging
```bash
python starlink_connectivity.py --verbose monitor --interval 15
```

### Crisis mode monitoring with custom duration
```bash
python starlink_connectivity.py --crisis-mode monitor --duration 7200
```

### Combined operations
```bash
# Monitor for 30 minutes, then generate report
python starlink_connectivity.py monitor --duration 1800
python starlink_connectivity.py report --output session_report.json
```

## Operation Modes

### Monitor Mode
Continuously monitors Starlink connectivity at specified intervals.
- Tracks latency, packet loss, and connection status
- Alerts on consecutive failures
- Maintains performance history
- Supports graceful shutdown (Ctrl+C)

### Single-Check Mode
Performs one connectivity check and exits.
- Quick status verification
- Outputs JSON result
- Useful for scripting and automation

### Report Mode
Generates comprehensive performance reports.
- Success rate analysis
- Latency statistics (min, max, avg, median)
- Packet loss metrics
- Status breakdown
- Export capabilities

### Reboot Mode (Placeholder)
Provides interface for dish reboot operations.
- Currently requires manual intervention
- Ready for Starlink API integration

## Crisis Mode Details

Crisis mode automatically adjusts monitoring parameters for emergency scenarios:

**Normal Mode:**
- Ping timeout: 5 seconds
- Max failures before alert: 3
- Minimum success rate: 80%
- Alert latency threshold: 100ms

**Crisis Mode:**
- Ping timeout: 10 seconds
- Max failures before alert: 5
- Minimum success rate: 50%
- Alert latency threshold: 300ms

Use crisis mode during:
- Emergency situations
- Severe weather events
- Known infrastructure issues
- Temporary network degradation

## Logging

Logs are written to both console and file simultaneously:

**Log File:** `starlink_monitor.log` (configurable)
**Log Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
**Format:** Timestamp, level, and message

Example log output:
```
2026-01-05 14:30:00 - INFO - Starting continuous monitoring (interval: 60s)...
2026-01-05 14:30:05 - INFO - ✓ Connectivity: EXCELLENT - Latency: 42.3ms
2026-01-05 14:31:05 - WARNING - ⚠ Connectivity: DEGRADED - Latency: 156.8ms, Packet Loss: 5.2%
2026-01-05 14:32:05 - ERROR - Connection failure 1/3: Failed to reach Starlink dish
```

## Reporting Output

Sample report structure:
```json
{
  "generated_at": "2026-01-05T14:35:00",
  "crisis_mode": false,
  "period": {
    "start": "2026-01-05T14:00:00",
    "end": "2026-01-05T14:35:00",
    "total_checks": 35
  },
  "connectivity": {
    "success_rate": 0.943,
    "status_breakdown": {
      "excellent": 28,
      "good": 5,
      "degraded": 2
    }
  },
  "performance": {
    "latency": {
      "min": 38.2,
      "max": 187.4,
      "avg": 52.6,
      "median": 45.3
    },
    "packet_loss": {
      "avg": 0.014,
      "max": 0.125
    }
  },
  "alerts": {
    "success_rate_threshold_met": true
  }
}
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses standard library only)
- Network connectivity to Starlink dish (default: 192.168.100.1)
- Ping utility (available on all platforms)

## Platform Support

- ✅ Linux
- ✅ macOS
- ✅ Windows
- ✅ Cross-platform ping implementation

## Troubleshooting

### Cannot reach Starlink dish
- Verify you're connected to Starlink network
- Check dish IP address in configuration (default: 192.168.100.1)
- Ensure ping is available on your system

### Permission errors with log file
- Check write permissions in current directory
- Specify alternative log path in configuration

### High latency alerts
- Adjust `alert_latency_ms` threshold in configuration
- Consider using crisis mode for known degraded conditions

## Contributing

Contributions welcome! Please feel free to submit pull requests or open issues.

## License

See LICENSE file for details.

## Acknowledgments

Inspired by the resilience and resourcefulness of communities maintaining connectivity in challenging conditions, particularly Venezuela's approach to crisis communication.