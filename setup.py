#!/usr/bin/env python3
"""
Setup script for Starlink Connectivity Tools
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
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
    },
    entry_points={
        "console_scripts": [
            "starlink-monitor=tools.starlink_monitor_cli:main",
            "starlink-dashboard=tools.connectivity_dashboard:main",
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
