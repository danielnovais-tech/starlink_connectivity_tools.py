"""
Starlink Dish Interface Module

This module provides a simulated interface to Starlink dish for monitoring
and control operations. In a production environment, this would connect to
the actual dish via gRPC at 192.168.100.1:9200.
"""

import time
import random
from typing import Dict, Any, Optional
from .exceptions import StarlinkConnectionError, StarlinkEmergencyError


class StarlinkDish:
    """
    Interface to Starlink dish for monitoring and control.
    
    This is a simulated implementation for demonstration purposes.
    In production, this would use the Starlink gRPC API.
    """
    
    DEFAULT_IP = "192.168.100.1"
    DEFAULT_PORT = 9200
    
    def __init__(self, ip: str = DEFAULT_IP, port: int = DEFAULT_PORT):
        """
        Initialize connection to Starlink dish.
        
        Args:
            ip: IP address of the Starlink dish (default: 192.168.100.1)
            port: gRPC port of the Starlink dish (default: 9200)
        """
        self.ip = ip
        self.port = port
        self._connected = False
        self._stowed = False
        
    def connect(self) -> bool:
        """
        Establish connection to the Starlink dish.
        
        Returns:
            True if connection successful, False otherwise
        """
        # Simulated connection
        print(f"Attempting to connect to Starlink dish at {self.ip}:{self.port}...")
        time.sleep(0.5)
        self._connected = True
        print("✓ Connected successfully")
        return True
    
    def disconnect(self):
        """Disconnect from the Starlink dish."""
        self._connected = False
        print("Disconnected from Starlink dish")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the Starlink dish.
        
        Returns:
            Dictionary containing dish status information
            
        Raises:
            StarlinkConnectionError: If not connected to dish
        """
        if not self._connected:
            raise StarlinkConnectionError("Not connected to dish. Call connect() first.")
        
        # Simulated status data
        status = {
            "uptime": random.randint(1000, 100000),
            "obstructed": random.choice([True, False]),
            "obstruction_percentage": random.uniform(0, 15),
            "connected_satellites": random.randint(3, 8),
            "downlink_throughput_bps": random.uniform(50e6, 200e6),
            "uplink_throughput_bps": random.uniform(10e6, 40e6),
            "pop_ping_latency_ms": random.uniform(20, 60),
            "stowed": self._stowed,
            "heating": random.choice([True, False]),
            "motor_stuck": random.random() < 0.25,  # 25% chance
            "thermal_throttle": random.random() < 0.33,  # 33% chance
            "unexpected_outages": random.randint(0, 5),
        }
        
        return status
    
    def stow(self) -> bool:
        """
        Stow the dish (emergency protection position).
        
        This puts the dish in a safe, flat position to protect it during
        high winds, storms, or other emergency conditions.
        
        Returns:
            True if stow successful
            
        Raises:
            StarlinkConnectionError: If not connected to dish
        """
        if not self._connected:
            raise StarlinkConnectionError("Not connected to dish. Call connect() first.")
        
        print("Stowing dish to emergency position...")
        time.sleep(1.0)
        self._stowed = True
        print("✓ Dish stowed successfully")
        return True
    
    def unstow(self) -> bool:
        """
        Unstow the dish (return to normal operation).
        
        Returns:
            True if unstow successful
            
        Raises:
            StarlinkConnectionError: If not connected to dish
        """
        if not self._connected:
            raise StarlinkConnectionError("Not connected to dish. Call connect() first.")
        
        print("Unstowing dish to normal operation...")
        time.sleep(1.0)
        self._stowed = False
        print("✓ Dish unstowed successfully")
        return True
    
    def reboot(self) -> bool:
        """
        Reboot the Starlink dish.
        
        Returns:
            True if reboot initiated successfully
            
        Raises:
            StarlinkConnectionError: If not connected to dish
        """
        if not self._connected:
            raise StarlinkConnectionError("Not connected to dish. Call connect() first.")
        
        print("Initiating dish reboot...")
        time.sleep(0.5)
        print("✓ Reboot command sent successfully")
        return True
    
    def check_emergency_conditions(self) -> Optional[str]:
        """
        Check for emergency conditions that require intervention.
        
        Returns:
            String describing the emergency condition, or None if all is well
        """
        if not self._connected:
            raise StarlinkConnectionError("Not connected to dish. Call connect() first.")
        
        status = self.get_status()
        
        # Check for various emergency conditions
        if status["motor_stuck"]:
            return "MOTOR_STUCK"
        
        if status["obstruction_percentage"] > 10:
            return "HIGH_OBSTRUCTION"
        
        if status["thermal_throttle"]:
            return "THERMAL_THROTTLE"
        
        if status["pop_ping_latency_ms"] > 100:
            return "HIGH_LATENCY"
        
        return None
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
        return False
