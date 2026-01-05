"""
Failover Handler Module

Manages automatic failover to backup connections when primary Starlink connection fails.
"""


class FailoverHandler:
    """Handles connection failover scenarios."""

    def __init__(self, backup_connections=None):
        """
        Initialize the FailoverHandler.

        Args:
            backup_connections: List of backup connection configurations
        """
        self.backup_connections = backup_connections or []
        self.primary_active = True
        self.current_connection = "primary"
        self.failover_enabled = False

    def enable_failover(self):
        """
        Enable automatic failover.

        Returns:
            bool: True if failover enabled successfully
        """
        self.failover_enabled = True
        return True

    def disable_failover(self):
        """
        Disable automatic failover.

        Returns:
            bool: True if failover disabled successfully
        """
        self.failover_enabled = False
        return True

    def add_backup_connection(self, connection_config):
        """
        Add a backup connection configuration.

        Args:
            connection_config: Backup connection configuration

        Returns:
            bool: True if backup added successfully
        """
        self.backup_connections.append(connection_config)
        return True

    def trigger_failover(self):
        """
        Manually trigger failover to backup connection.

        Returns:
            dict: Failover results
        """
        if not self.backup_connections:
            return {"status": "no_backup_available"}

        self.primary_active = False
        self.current_connection = "backup"
        return {
            "status": "failover_complete",
            "current_connection": self.current_connection,
        }

    def restore_primary(self):
        """
        Restore connection to primary Starlink connection.

        Returns:
            dict: Restoration results
        """
        self.primary_active = True
        self.current_connection = "primary"
        return {
            "status": "primary_restored",
            "current_connection": self.current_connection,
        }

    def get_status(self):
        """
        Get current failover status.

        Returns:
            dict: Failover status information
        """
        return {
            "failover_enabled": self.failover_enabled,
            "primary_active": self.primary_active,
            "current_connection": self.current_connection,
            "backup_count": len(self.backup_connections),
        }
