"""
Setup configuration for starlink_connectivity_tools package.
"""
from setuptools import setup, find_packages

setup(
    name="starlink_connectivity_tools",
    version="0.1.0",
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
)
