"""
Failover handling for maintaining connectivity
"""
import time
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class FailoverStrategy(Enum):
    """Failover strategy types"""
    ACTIVE_PASSIVE = "active_passive"
    ACTIVE_ACTIVE = "active_active"
    LOAD_BALANCED = "load_balanced"
    GEO_REDUNDANT = "geo_redundant"


@dataclass
class BackupConnection:
    """Backup connection configuration"""
    connection_id: str
    priority: int
    type: str  # 'satellite', 'cellular', 'wifi', 'wired'
    cost_per_mb: float
    max_bandwidth: float
    enabled: bool = True


class FailoverHandler:
    """Handles failover between different connection types"""
    
    def __init__(self):
        self.backup_connections: List[BackupConnection] = []
        self.active_backup: Optional[BackupConnection] = None
        self.failover_threshold = 3  # Number of failures before failover
        self.failure_count = 0
        self.strategy = FailoverStrategy.ACTIVE_PASSIVE
        
        # Load backup configurations
        self._load_default_backups()
    
    def _load_default_backups(self):
        """Load default backup connection configurations"""
        default_backups = [
            BackupConnection(
                connection_id="cellular_primary",
                priority=1,
                type="cellular",
                cost_per_mb=0.05,
                max_bandwidth=50.0
            ),
            BackupConnection(
                connection_id="cellular_secondary",
                priority=2,
                type="cellular",
                cost_per_mb=0.10,
                max_bandwidth=20.0
            ),
            BackupConnection(
                connection_id="wifi_mesh",
                priority=3,
                type="wifi",
                cost_per_mb=0.0,
                max_bandwidth=100.0
            ),
            BackupConnection(
                connection_id="satellite_backup",
                priority=4,
                type="satellite",
                cost_per_mb=0.50,
                max_bandwidth=10.0
            )
        ]
        
        self.backup_connections.extend(default_backups)
        logger.info(f"Loaded {len(default_backups)} backup connections")
    
    def check_connection_health(self, 
                               latency: float, 
                               packet_loss: float) -> bool:
        """
        Check if primary connection is healthy
        Returns True if healthy, False if failing
        """
        # Define health thresholds
        max_latency = 500  # ms
        max_packet_loss = 20  # percent
        
        healthy = (latency <= max_latency and packet_loss <= max_packet_loss)
        
        if not healthy:
            self.failure_count += 1
            logger.warning(
                f"Connection health check failed. "
                f"Latency: {latency}ms, Packet loss: {packet_loss}%. "
                f"Failure count: {self.failure_count}/{self.failover_threshold}"
            )
        else:
            self.failure_count = max(0, self.failure_count - 1)
        
        return healthy
    
    def should_failover(self) -> bool:
        """Determine if failover should be triggered"""
        return self.failure_count >= self.failover_threshold
    
    def select_backup_connection(self, 
                                required_bandwidth: float = 1.0,
                                max_cost: float = 1.0) -> Optional[BackupConnection]:
        """
        Select appropriate backup connection based on requirements
        """
        available_backups = [
            b for b in self.backup_connections 
            if b.enabled and b.max_bandwidth >= required_bandwidth
        ]
        
        if not available_backups:
            logger.error("No suitable backup connections available")
            return None
        
        # Sort by priority, then cost
        sorted_backups = sorted(
            available_backups,
            key=lambda x: (x.priority, x.cost_per_mb)
        )
        
        selected = sorted_backups[0]
        
        # Check cost constraint
        if selected.cost_per_mb > max_cost:
            logger.warning(f"Selected backup {selected.connection_id} "
                          f"exceeds cost limit")
            # Try to find cheaper alternative
            cheaper = [b for b in sorted_backups if b.cost_per_mb <= max_cost]
            if cheaper:
                selected = cheaper[0]
            else:
                logger.error("No backup within cost limit")
                return None
        
        logger.info(f"Selected backup: {selected.connection_id}")
        return selected
    
    def initiate_failover(self, 
                         reason: str = "primary connection failed") -> bool:
        """Initiate failover to backup connection"""
        if not self.should_failover():
            logger.info("Failover threshold not reached")
            return False
        
        logger.warning(f"Initiating failover: {reason}")
        
        # Select backup connection
        backup = self.select_backup_connection()
        
        if not backup:
            logger.error("Failed to select backup connection")
            return False
        
        # Simulate failover process
        try:
            logger.info(f"Switching to backup: {backup.connection_id}")
            
            # In real implementation, this would:
            # 1. Disconnect primary
            # 2. Configure and connect backup
            # 3. Update routing tables
            # 4. Verify connectivity
            
            time.sleep(2)  # Simulate failover time
            
            self.active_backup = backup
            self.failure_count = 0
            
            logger.info(f"Failover complete to {backup.connection_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failover failed: {e}")
            return False
    
    def failback_to_primary(self) -> bool:
        """Fail back to primary connection when available"""
        if not self.active_backup:
            logger.info("No active backup to fail back from")
            return True
        
        logger.info(f"Attempting to fail back from {self.active_backup.connection_id}")
        
        try:
            # Simulate failback process
            time.sleep(1)
            
            # Reset failure count
            self.failure_count = 0
            previous_backup = self.active_backup
            self.active_backup = None
            
            logger.info(f"Successfully failed back from {previous_backup.connection_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failback failed: {e}")
            return False
    
    def get_failover_status(self) -> Dict[str, Any]:
        """Get current failover status"""
        return {
            'strategy': self.strategy.value,
            'failure_count': self.failure_count,
            'failover_threshold': self.failover_threshold,
            'active_backup': self.active_backup.connection_id 
                           if self.active_backup else None,
            'available_backups': len([b for b in self.backup_connections 
                                     if b.enabled]),
            'timestamp': time.time()
        }
    
    def enable_backup(self, connection_id: str) -> None:
        """Enable a specific backup connection"""
        for backup in self.backup_connections:
            if backup.connection_id == connection_id:
                backup.enabled = True
                logger.info(f"Enabled backup: {connection_id}")
                return
        
        logger.warning(f"Backup not found: {connection_id}")
    
    def disable_backup(self, connection_id: str) -> None:
        """Disable a specific backup connection"""
        for backup in self.backup_connections:
            if backup.connection_id == connection_id:
                backup.enabled = False
                logger.info(f"Disabled backup: {connection_id}")
                return
        
        logger.warning(f"Backup not found: {connection_id}")
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
