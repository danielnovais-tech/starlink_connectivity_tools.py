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
