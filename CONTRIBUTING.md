# Contributing to Starlink Connectivity Tools

Thank you for your interest in contributing to this project!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/danielnovais-tech/starlink_connectivity_tools.py.git
cd starlink_connectivity_tools.py
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/
```

With coverage:
```bash
pytest --cov=starlink_connectivity_tools tests/
```

## Code Style

This project uses:
- **black** for code formatting
- **ruff** for linting

Format code:
```bash
black starlink_connectivity_tools/ tests/ examples/
```

Lint code:
```bash
ruff check starlink_connectivity_tools/ tests/ examples/
```

## Adding Features

1. Create a new branch for your feature
2. Write tests for your changes
3. Implement your changes
4. Ensure all tests pass
5. Format and lint your code
6. Submit a pull request

## Reporting Issues

When reporting issues, please include:
- Python version
- Library version
- Steps to reproduce
- Expected vs actual behavior
- Error messages and stack traces

## Community Proto Files

If you have reverse-engineered proto files for the Starlink API, please consider:
1. Creating a separate repository for them
2. Documenting the firmware version they correspond to
3. Sharing extraction methodology

## Code of Conduct

Be respectful and constructive in all interactions.
