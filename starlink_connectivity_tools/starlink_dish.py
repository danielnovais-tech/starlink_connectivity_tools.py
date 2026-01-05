"""
StarlinkDish - Core class for interacting with Starlink dish.
"""

import time
import random


class StarlinkDish:
    """
    Represents a Starlink dish and provides methods to interact with it.
    
    This is a simplified implementation that simulates dish connectivity
    and status monitoring for demonstration purposes.
    """
    
    def __init__(self, host="192.168.100.1", port=9200):
        """
        Initialize connection to Starlink dish.
        
        Args:
            host: IP address of the Starlink dish (default: 192.168.100.1)
            port: gRPC port (default: 9200)
        """
        self.host = host
        self.port = port
        self.connected = False
        
    def connect(self):
        """Establish connection to the dish."""
        print(f"Connecting to Starlink dish at {self.host}:{self.port}...")
        time.sleep(0.5)  # Simulate connection delay
        self.connected = True
        print("Connected successfully.")
        
    def disconnect(self):
        """Disconnect from the dish."""
        if self.connected:
            print("Disconnecting from dish...")
            self.connected = False
            print("Disconnected.")
    
    def get_status(self):
        """
        Get current status of the dish.
        
        Returns:
            dict: Dictionary containing dish status information
        """
        if not self.connected:
            raise ConnectionError("Not connected to dish. Call connect() first.")
        
        # Simulate status retrieval
        status = {
            "uptime": random.randint(3600, 86400),
            "state": "CONNECTED",
            "obstructed": random.choice([True, False]),
            "snr": round(random.uniform(5.0, 15.0), 2),
            "downlink_throughput": round(random.uniform(50, 250), 2),
            "uplink_throughput": round(random.uniform(10, 50), 2),
            "ping_latency": round(random.uniform(20, 60), 2),
        }
        return status
    
    def get_alerts(self):
        """
        Get current alerts from the dish.
        
        Returns:
            list: List of alert messages
        """
        if not self.connected:
            raise ConnectionError("Not connected to dish. Call connect() first.")
        
        # Simulate alerts
        possible_alerts = [
            "Motors stuck",
            "Thermal throttle",
            "Unexpected location",
            "Mast not near vertical",
            "Slow ethernet speeds",
        ]
        
        # Randomly return 0-2 alerts
        num_alerts = random.randint(0, 2)
        if num_alerts == 0:
            return []
        
        return random.sample(possible_alerts, num_alerts)
    
    def reboot(self):
        """Reboot the dish."""
        if not self.connected:
            raise ConnectionError("Not connected to dish. Call connect() first.")
        
        print("Initiating dish reboot...")
        time.sleep(1)
        print("Reboot command sent successfully.")
        
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
        return False
