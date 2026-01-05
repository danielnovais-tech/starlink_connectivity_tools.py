"""Connection failover handler for managing primary and backup connections."""

import time
import logging
from typing import Optional, Callable
from enum import Enum


class ConnectionState(Enum):
    """Enum representing connection states."""
    PRIMARY = "primary"
    BACKUP = "backup"
    FAILED = "failed"


class FailoverHandler:
    """
    Handles automatic failover between primary and backup connections.
    
    This class monitors the primary connection and automatically switches
    to a backup connection when failures are detected.
    """
    
    def __init__(
        self,
        failure_threshold: int = 3,
        check_interval: float = 5.0,
        health_check_callback: Optional[Callable[[], bool]] = None
    ):
        """
        Initialize the FailoverHandler.
        
        Args:
            failure_threshold: Number of consecutive failures before triggering failover
            check_interval: Time in seconds between health checks
            health_check_callback: Optional callback function to check connection health
        """
        self.failure_threshold = failure_threshold
        self.check_interval = check_interval
        self.health_check_callback = health_check_callback
        
        self._failure_count = 0
        self._current_state = ConnectionState.PRIMARY
        self._last_check_time = 0.0
        self._failover_history = []
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Add console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def should_failover(self) -> bool:
        """
        Check if failover should be initiated.
        
        Returns:
            bool: True if failover should be initiated, False otherwise
        """
        current_time = time.time()
        
        # Check if enough time has passed since last check
        if current_time - self._last_check_time < self.check_interval:
            return False
        
        self._last_check_time = current_time
        
        # Perform health check
        is_healthy = self._check_connection_health()
        
        if not is_healthy:
            self._failure_count += 1
            self.logger.warning(
                f"Connection health check failed. "
                f"Failure count: {self._failure_count}/{self.failure_threshold}"
            )
            
            if self._failure_count >= self.failure_threshold:
                self.logger.error("Failure threshold reached. Failover recommended.")
                return True
        else:
            # Reset failure count on successful check
            if self._failure_count > 0:
                self.logger.info("Connection recovered. Resetting failure count.")
            self._failure_count = 0
        
        return False
    
    def initiate_failover(self, reason: str) -> bool:
        """
        Initiate failover to backup connection.
        
        Args:
            reason: Reason for initiating failover
            
        Returns:
            bool: True if failover was successful, False otherwise
        """
        if self._current_state == ConnectionState.BACKUP:
            self.logger.warning("Already on backup connection. Cannot failover further.")
            return False
        
        self.logger.info(f"Initiating failover. Reason: {reason}")
        
        # Record failover event
        failover_event = {
            "timestamp": time.time(),
            "from_state": self._current_state.value,
            "to_state": ConnectionState.BACKUP.value,
            "reason": reason,
            "failure_count": self._failure_count
        }
        self._failover_history.append(failover_event)
        
        # Switch to backup connection
        previous_state = self._current_state
        self._current_state = ConnectionState.BACKUP
        
        # Reset failure counter after failover
        self._failure_count = 0
        
        self.logger.info(
            f"Failover successful: {previous_state.value} -> {self._current_state.value}"
        )
        
        return True
    
    def _check_connection_health(self) -> bool:
        """
        Check the health of the current connection.
        
        Returns:
            bool: True if connection is healthy, False otherwise
        """
        if self.health_check_callback:
            try:
                return self.health_check_callback()
            except Exception as e:
                self.logger.error(f"Health check callback failed: {e}")
                return False
        
        # Default behavior: assume connection is healthy if no callback provided
        return True
    
    def get_current_state(self) -> ConnectionState:
        """
        Get the current connection state.
        
        Returns:
            ConnectionState: Current connection state
        """
        return self._current_state
    
    def get_failure_count(self) -> int:
        """
        Get the current failure count.
        
        Returns:
            int: Number of consecutive failures
        """
        return self._failure_count
    
    def get_failover_history(self) -> list:
        """
        Get the history of failover events.
        
        Returns:
            list: List of failover event dictionaries
        """
        return self._failover_history.copy()
    
    def reset(self) -> None:
        """Reset the failover handler to initial state."""
        self._failure_count = 0
        self._current_state = ConnectionState.PRIMARY
        self._last_check_time = 0.0
        self.logger.info("Failover handler reset to initial state")
