# Contributing to Starlink Connectivity Tools

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/danielnovais-tech/starlink_connectivity_tools.py/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/starlink_connectivity_tools.py.git
   cd starlink_connectivity_tools.py
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Follow the coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Run all tests
   pytest tests/
   
   # Run specific test file
   pytest tests/test_starlink_api.py
   
   # Run with coverage
   pytest --cov=starlink_connectivity_tools tests/
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```
   
   Use clear commit messages:
   - `feat: add new crisis scenario`
   - `fix: resolve connection timeout issue`
   - `docs: update installation guide`
   - `test: add tests for diagnostics module`

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   
   Then create a Pull Request on GitHub.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install in editable mode with dependencies
pip install -e .

# Install development tools
pip install pytest pytest-cov black flake8 mypy

# Run tests
pytest tests/
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use type hints where appropriate

### Code Formatting

```bash
# Format code with black
black src/ tests/

# Check style with flake8
flake8 src/ tests/
```

### Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings:
  ```python
  def function_name(param1: str, param2: int) -> bool:
      """
      Brief description.

      Longer description if needed.

      Args:
          param1: Description of param1
          param2: Description of param2

      Returns:
          Description of return value

      Raises:
          ValueError: When invalid input
      """
  ```

- Update README.md for major features
- Add examples for new functionality

### Testing

- Write tests for all new code
- Aim for >80% code coverage
- Test both success and failure cases
- Use simulation mode for tests (no real hardware required)

Example test:
```python
def test_new_feature():
    """Test description."""
    # Arrange
    manager = SatelliteConnectionManager()
    
    # Act
    result = manager.some_method()
    
    # Assert
    assert result is not None
    assert result.status == "expected_value"
```

## Project Structure

```
starlink_connectivity_tools.py/
├── src/starlink_connectivity_tools/
│   ├── __init__.py
│   ├── starlink_api.py           # Starlink gRPC integration
│   ├── satellite_connection_manager.py  # Connection management
│   ├── crisis_monitor.py         # Crisis monitoring
│   ├── diagnostics.py            # Diagnostics engine
│   └── starlink_monitor_cli.py   # CLI interface
├── examples/
│   ├── venezuela_crisis_scenario.py
│   ├── medical_mission_scenario.py
│   └── power_network_scenario.py
├── tests/
│   ├── test_starlink_api.py
│   ├── test_connection_manager.py
│   ├── test_crisis_monitor.py
│   └── test_diagnostics.py
├── README.md
├── INSTALL.md
├── CONTRIBUTING.md
├── requirements.txt
└── setup.py
```

## Adding New Features

### New Crisis Scenario

1. Add scenario to `ScenarioType` enum in `crisis_monitor.py`
2. Add thresholds to `SCENARIO_THRESHOLDS` dictionary
3. Add tests in `test_crisis_monitor.py`
4. Document in README.md

### New Connection Type

1. Add type to `ConnectionType` enum in `satellite_connection_manager.py`
2. Implement connection logic (if needed)
3. Add tests
4. Add example usage

### New CLI Command

1. Add command function to `starlink_monitor_cli.py`
2. Use Click decorators for options
3. Follow existing command structure
4. Add help text
5. Test manually

## Areas for Contribution

We especially welcome contributions in these areas:

- **Performance Optimization**: Improve efficiency of monitoring loops
- **Additional Crisis Scenarios**: More realistic scenario simulations
- **Enhanced Diagnostics**: Better detection algorithms
- **Documentation**: API docs, tutorials, how-to guides
- **Testing**: More comprehensive test coverage
- **UI/UX**: Better CLI output, potential GUI
- **Integration**: Support for additional satellite systems
- **Error Handling**: More robust error recovery

## Questions?

- Open an issue with the "question" label
- Check existing discussions
- Review the documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to Starlink Connectivity Tools! 🛰️
# Contributing to starlink_connectivity_tools.py

Thank you for your interest in contributing to starlink_connectivity_tools.py! We welcome contributions from the community.

## How to Contribute

### 1. Fork the Repository

Start by forking the repository to your GitHub account:

1. Navigate to the [starlink_connectivity_tools.py repository](https://github.com/danielnovais-tech/starlink_connectivity_tools.py)
2. Click the "Fork" button in the upper right corner
3. This creates a copy of the repository in your GitHub account

### 2. Create a Feature Branch

Create a new branch for your contribution:

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py

# Create a new feature branch
git checkout -b feature/your-feature-name
```

Use descriptive branch names that reflect the changes you're making, such as:
- `feature/add-connection-monitor`
- `bugfix/fix-timeout-issue`
- `docs/update-readme`

### 3. Add Tests for New Functionality

All new functionality should include appropriate tests:

- Write unit tests for new functions and classes
- Ensure tests cover edge cases and error handling
- Follow the existing test patterns in the repository
- Run tests locally to verify they pass before submitting

```bash
# Run tests (command may vary based on project setup)
python -m pytest
```

### 4. Submit a Pull Request

Once your changes are ready:

1. **Commit your changes** with clear, descriptive commit messages:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request**:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Provide a clear title and description of your changes
   - Reference any related issues

4. **Address review feedback**:
   - Respond to comments from maintainers
   - Make requested changes
   - Push updates to your branch (the PR will update automatically)

## Code Style Guidelines

- Follow PEP 8 style guidelines for Python code
- Write clear, descriptive variable and function names
- Include docstrings for functions and classes
- Keep commits focused and atomic

## Questions?

If you have questions about contributing, feel free to open an issue for discussion.

Thank you for contributing!
