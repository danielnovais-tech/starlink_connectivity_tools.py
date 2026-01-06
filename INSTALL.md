# Installation Guide

This guide will help you install and configure the Starlink Connectivity Tools.

## Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Optional: Starlink dish with network connectivity

## Installation Methods

### Method 1: Install from Source (Recommended)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
   cd starlink_connectivity_tools.py
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the Package**
   ```bash
   pip install -e .
   ```

   This installs the package in "editable" mode, allowing you to modify the code and see changes immediately.

4. **Verify Installation**
   ```bash
   starlink-monitor --help
   ```

### Method 2: Install in a Virtual Environment

For a clean, isolated installation:

```bash
# Create virtual environment
python -m venv starlink-env

# Activate the environment
# On Linux/Mac:
source starlink-env/bin/activate
# On Windows:
starlink-env\Scripts\activate

# Install the package
cd starlink_connectivity_tools.py
pip install -e .
```

## Optional: Installing starlink-grpc

The `starlink-grpc` library is required only if you want to connect to real Starlink hardware. It's not available on PyPI, so you need to install it manually.

### For Real Hardware Connection

1. **Clone the starlink-grpc-tools repository**
   ```bash
   git clone https://github.com/sparky8512/starlink-grpc-tools.git
   cd starlink-grpc-tools
   ```

2. **Install the package**
   ```bash
   pip install .
   ```

3. **Verify Starlink Connection**
   Make sure your computer can reach the Starlink dish at `192.168.100.1:9200` (default).

### For Simulation Mode Only

If you don't have Starlink hardware or just want to test the tools, you don't need to install `starlink-grpc`. The tools will automatically use simulation mode.

## Post-Installation

### 1. Test the Installation

Run a quick test to verify everything works:

```bash
# Test with simulation mode
starlink-monitor status --simulation

# Run tests
python -m pytest tests/
```

### 2. Configure for Your Environment

Create a configuration file (optional):

```bash
# Create .env file for custom settings
cat > .env << EOF
STARLINK_TARGET=192.168.100.1:9200
SIMULATION_MODE=false
LOG_LEVEL=INFO
EOF
```

### 3. Try Example Scenarios

Run one of the example scenarios:

```bash
# Venezuela crisis scenario
python examples/venezuela_crisis_scenario.py

# Medical mission scenario
python examples/medical_mission_scenario.py

# Power outage scenario
python examples/power_network_scenario.py
```

## Troubleshooting

### Issue: "starlink-grpc not available"

**Solution**: This is expected if you haven't installed `starlink-grpc`. The tools will use simulation mode automatically. If you want real hardware support, follow the "Installing starlink-grpc" section above.

### Issue: "Permission denied" when installing

**Solution**: Use `pip install --user -e .` to install in your user directory, or use a virtual environment.

### Issue: "Module not found" errors

**Solution**: Make sure you're in the correct directory and have activated your virtual environment (if using one).

```bash
cd /path/to/starlink_connectivity_tools.py
pip install -e .
```

### Issue: Can't connect to Starlink dish

**Solution**: 
1. Verify the dish is powered on and connected to your network
2. Check that you can ping `192.168.100.1`
3. Ensure no firewall is blocking port 9200
4. Try using `--target` flag to specify a different address:
   ```bash
   starlink-monitor status --target 192.168.100.1:9200
   ```

## Development Installation

For development purposes:

```bash
# Clone and install with dev dependencies
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py

# Install with test dependencies
pip install -e ".[dev]"  # Note: [dev] support needs to be added to setup.py

# Or manually install test tools
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/

# Format code
black src/

# Lint code
flake8 src/
```

## Uninstallation

To remove the package:

```bash
pip uninstall starlink-connectivity-tools
```

If you installed in a virtual environment, simply delete the environment directory.

## Next Steps

- Read the [README.md](../README.md) for usage examples
- Check out the [examples](../examples/README.md) directory for scenario simulations
- Review the API documentation (coming soon)
- Join the community discussions

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review the [GitHub Issues](https://github.com/danielnovais-tech/starlink_connectivity_tools.py/issues)
3. Create a new issue with details about your problem
