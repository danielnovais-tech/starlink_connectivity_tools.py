"""
Failover Handler
Manages failover between different connection types
"""

import logging
import time
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class FailoverHandler:
    """Handles failover between primary and backup connections"""
    
    def __init__(self):
        self.backup_connections: List[Dict[str, Any]] = []
        self.failover_active = False
        self.active_backup = None
        self.failover_history: List[Dict[str, Any]] = []
        
        logger.info("FailoverHandler initialized")
    
    def initiate_failover(self, reason: str):
        """Initiate failover to backup connection"""
        logger.warning(f"Initiating failover: {reason}")
        
        if not self.backup_connections:
            logger.error("No backup connections available for failover")
            return False
        
        # Sort by priority (lower is better)
        sorted_backups = sorted(self.backup_connections, key=lambda x: x.get('priority', 999))
        
        if sorted_backups:
            self.active_backup = sorted_backups[0]
            self.failover_active = True
            
            self.failover_history.append({
                'reason': reason,
                'backup_used': self.active_backup['connection_id'],
                'timestamp': time.time()
            })
            
            logger.info(f"Failover to {self.active_backup['connection_id']} successful")
            return True
        
        return False
    
    def get_failover_status(self) -> Dict[str, Any]:
        """Get failover status report"""
        return {
            'failover_active': self.failover_active,
            'active_backup': self.active_backup,
            'available_backups': len(self.backup_connections),
            'failover_count': len(self.failover_history),
            'backup_connections': self.backup_connections
        }
