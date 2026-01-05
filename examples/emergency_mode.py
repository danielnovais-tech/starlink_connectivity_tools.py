"""
Emergency Mode Example

Demonstrates how to configure Starlink tools for emergency scenarios
with automatic failover and optimized connectivity.
"""

import sys
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.connection_manager import ConnectionManager
from src.failover_handler import FailoverHandler
from src.diagnostics import Diagnostics
from src.config.settings import Settings


def main():
    """Run emergency mode configuration."""
    print("=== Starlink Emergency Mode ===\n")

    # Initialize settings for emergency mode
    emergency_config = {
        "connection": {
            "timeout": 60,
            "retry_attempts": 5,
            "retry_delay": 3,
        },
        "failover": {
            "enabled": True,
            "auto_failover": True,
            "health_check_interval": 30,
        },
    }
    settings = Settings(custom_config=emergency_config)
    print("Emergency configuration loaded")
    print(f"Timeout: {settings.get('connection.timeout')}s")
    print(f"Retry attempts: {settings.get('connection.retry_attempts')}")
    print(f"Auto-failover: {settings.get('failover.auto_failover')}\n")

    # Set up connection manager
    connection_manager = ConnectionManager(config=settings.get_all())
    print("Connecting to Starlink...")
    if connection_manager.connect():
        print("✓ Connected successfully\n")
    else:
        print("✗ Connection failed\n")

    # Configure failover with backup connections
    failover = FailoverHandler()
    failover.enable_failover()
    failover.add_backup_connection({"type": "cellular", "priority": 1})
    failover.add_backup_connection({"type": "satellite_backup", "priority": 2})
    print("Failover configured:")
    status = failover.get_status()
    print(f"  Failover enabled: {status['failover_enabled']}")
    print(f"  Backup connections: {status['backup_count']}")
    print(f"  Current connection: {status['current_connection']}\n")

    # Run diagnostics
    diagnostics = Diagnostics()
    print("Running health check...")
    health = diagnostics.run_health_check()
    print(f"Health status: {health['status']}\n")

    print("Emergency mode is now active!")
    print("The system will automatically failover if the primary connection fails.")


if __name__ == "__main__":
    main()
