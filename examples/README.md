# Examples

This directory contains example scripts demonstrating how to use the Starlink Connectivity Tools package.

## Available Examples

### 1. basic_usage.py
Basic introduction to the Space Safety API covering:
- Initializing the API client
- Submitting ephemeris data
- Screening for conjunctions
- Retrieving constellation data

**Run:**
```bash
python examples/basic_usage.py
```

### 2. file_upload.py
Demonstrates file-based ephemeris submission:
- Uploading OEM/TLE files
- Monitoring processing status
- Handling asynchronous operations

**Run:**
```bash
python examples/file_upload.py
```

### 3. advanced_screening.py
Advanced conjunction analysis including:
- Custom time window screening
- Risk categorization (HIGH/MEDIUM/LOW)
- Detailed event analysis
- Automated risk assessment

**Run:**
```bash
python examples/advanced_screening.py
```

## Configuration

### API Key

Set your API key as an environment variable:

```bash
export STARLINK_API_KEY="your_api_key_here"
```

Or in Python:
```python
import os
os.environ['STARLINK_API_KEY'] = 'your_api_key_here'
```

### Without API Key

The examples can run without an API key, but functionality may be limited depending on the API's authentication requirements.

## Notes

- These examples demonstrate the API interface and expected usage patterns
- Actual API responses will depend on the Space Safety API implementation
- Error handling is included to gracefully handle API unavailability
- The examples use realistic orbital parameters for demonstration purposes

## Requirements

Install the package and its dependencies:

```bash
pip install -e .
```

Or just the requirements:
```bash
pip install requests
```
