# Starlink Client Examples

This directory contains example scripts demonstrating how to use the Starlink Client library.

## Prerequisites

Make sure you have:
1. Installed all dependencies: `pip install -r ../requirements.txt`
2. The protobuf files (`device_pb2.py` and `device_pb2_grpc.py`) in the parent directory
3. Access to Starlink devices on your network

## Running Examples

From this directory, run any example:

```bash
python basic_status.py
python get_diagnostics.py
python ping_monitoring.py
python speed_test.py
python device_info.py
python custom_addresses.py
```

## Example Descriptions

### basic_status.py
**Purpose:** Get basic status information from Starlink devices

Shows how to:
- Initialize the StarlinkClient
- Retrieve status from both router and dish
- Handle errors gracefully

**Output:** Status information in JSON format

---

### get_diagnostics.py
**Purpose:** Retrieve detailed diagnostics information

Shows how to:
- Get comprehensive diagnostics data
- Pretty print JSON output
- Separate router and dish diagnostics

**Output:** Formatted diagnostics for both devices

---

### ping_monitoring.py
**Purpose:** Monitor network metrics and ping latency

Shows how to:
- Retrieve ping metrics
- Display metrics in a readable format
- Implement continuous monitoring (commented out by default)

**Features:**
- Single metrics retrieval
- Continuous monitoring with configurable interval
- Graceful shutdown with Ctrl+C

**Output:** Ping metrics with timestamp

---

### speed_test.py
**Purpose:** Run and retrieve speed test results

Shows how to:
- Get last speed test results
- Run a new speed test
- Handle long-running operations

**Note:** Speed tests can take 20-30 seconds to complete

**Output:** Download/upload speeds and latency

---

### device_info.py
**Purpose:** Get detailed device information

Shows how to:
- Retrieve hardware/software info
- Display information for multiple devices
- Format output for readability

**Output:** Device details including firmware version, serial numbers, etc.

---

### custom_addresses.py
**Purpose:** Connect to devices at non-standard addresses

Shows how to:
- Initialize client with custom addresses
- Useful for special network configurations
- Override default gRPC endpoints

**Use Case:** When your Starlink devices are on different network segments or ports

---

## Modifying Examples

All examples are well-commented and can be easily modified for your needs:

1. Change device addresses in the `StarlinkClient()` initialization
2. Adjust monitoring intervals in `ping_monitoring.py`
3. Change output format (JSON vs pretty print)
4. Add error handling or logging as needed

## Continuous Monitoring

The `ping_monitoring.py` example includes a continuous monitoring function that's commented out by default. To enable it:

```python
# At the end of ping_monitoring.py, uncomment:
continuous_monitoring(interval=60)
```

This will check ping metrics every 60 seconds until stopped with Ctrl+C.

## Error Handling

All examples include basic error handling. Common errors:

- **Connection refused**: Starlink device not accessible
- **Timeout**: Device not responding within timeout period
- **gRPC errors**: Network issues or invalid requests

## Integration

These examples can be integrated into larger applications:

- Network monitoring dashboards
- Automated health checks
- Performance logging systems
- Alert systems for connectivity issues

## Next Steps

After running these examples, you can:
1. Integrate the client into your own applications
2. Build custom monitoring solutions
3. Create scheduled tasks for regular checks
4. Develop alerting systems based on metrics
