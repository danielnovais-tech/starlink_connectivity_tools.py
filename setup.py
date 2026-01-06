"""Setup script for Starlink Connectivity Tools."""
"""Setup script for starlink_connectivity_tools package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

#!/usr/bin/env python3
"""
Setup script for Starlink Connectivity Tools
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
"""
Setup configuration for starlink_connectivity_tools package.
"""
from setuptools import setup, find_packages

setup(
    name="starlink_connectivity_tools",
    version="0.1.0",
    author="Daniel Novais",
    description="Python library for monitoring and managing Starlink dish connectivity",
    description="A Python library for working with Starlink connectivity",
    author="Daniel Novais",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
        ],
    },
"""Setup configuration for starlink_connectivity_tools package."""

from setuptools import setup, find_packages

"""
Setup configuration for Starlink Connectivity Tools.
"""

from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="starlink_connectivity_tools",
    version="0.1.0",
    author="Daniel Novais",
    description="Crisis-optimized Starlink connectivity monitoring and management tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielnovais-tech/starlink_connectivity_tools.py",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Internet :: Satellite",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    author_email="",
    description="A Python library for managing Starlink connections with automatic failover",
    author="Daniel Azevedo Novais",
    description="A Python library for managing Starlink satellite connectivity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielnovais-tech/starlink_connectivity_tools.py",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Communications",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    name="starlink-connectivity-tools",
    version="0.1.0",
    author="Daniel Novais",
    author_email="",
    description="Comprehensive suite of tools for managing Starlink satellite internet connections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielnovais-tech/starlink_connectivity_tools.py",
    packages=find_packages(exclude=["tests", "examples", "tools"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Networking",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    description="A Python library for managing Starlink connections, optimizing bandwidth, and handling failover scenarios",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielnovais-tech/starlink_connectivity_tools.py",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Networking",
        "Topic :: Communications :: Internet Phone",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies for simulated implementation
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "starlink-monitor=starlink_connectivity_tools.starlink_monitor_cli:main",
        ],
    },
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
    ],
    extras_require={
        "web": ["flask>=3.0.0"],
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies required for core functionality
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies required for basic functionality
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "starlink-monitor=tools.starlink_monitor_cli:main",
            "starlink-dashboard=tools.connectivity_dashboard:main",
            # Add CLI entry points here if needed
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="starlink satellite internet connectivity monitoring optimization power-management",
    project_urls={
        "Bug Reports": "https://github.com/danielnovais-tech/starlink_connectivity_tools.py/issues",
        "Source": "https://github.com/danielnovais-tech/starlink_connectivity_tools.py",
    },
)
