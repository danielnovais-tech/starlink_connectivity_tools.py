# starlink_connectivity_tools.py

Python tools for monitoring Starlink connectivity.

## Usage Examples

### Basic Monitoring

Check the current status of your Starlink connection:
```bash
python tools/starlink_monitor_cli.py status
```

Monitor your Starlink connection continuously with a 30-second interval:
```bash
python tools/starlink_monitor_cli.py monitor --interval 30
```