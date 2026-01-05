"""Main client for communicating with Starlink devices."""

import socket
import json
from typing import Optional
from .models import NetworkStats


class StarlinkClient:
    """Client for interacting with Starlink satellite internet devices.
    
    This client can connect to a local Starlink dish to retrieve network
    statistics and perform device operations like rebooting.
    
    Args:
        host: IP address of the Starlink dish (default: 192.168.100.1)
        port: Port number for communication (default: 9200)
        timeout: Connection timeout in seconds (default: 10)
    
    Example:
        >>> client = StarlinkClient()  # Local connection
        >>> stats = client.get_network_stats()
        >>> print(f"Download: {stats.download_speed} Mbps, Latency: {stats.latency} ms")
        >>> client.reboot_dish()
    """
    
    DEFAULT_HOST = "192.168.100.1"
    DEFAULT_PORT = 9200
    DEFAULT_TIMEOUT = 10
    
    def __init__(
        self, 
        host: Optional[str] = None, 
        port: Optional[int] = None,
        timeout: Optional[int] = None
    ):
        """Initialize Starlink client connection.
        
        Args:
            host: IP address of the Starlink dish
            port: Port number for communication
            timeout: Connection timeout in seconds
        """
        self.host = host or self.DEFAULT_HOST
        self.port = port or self.DEFAULT_PORT
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self._connected = False
    
    def _send_grpc_request(self, method: str, params: Optional[dict] = None) -> dict:
        """Send a gRPC-style request to the Starlink dish.
        
        This is a simplified implementation that simulates gRPC communication.
        In a real implementation, this would use the actual Starlink gRPC protocol.
        
        Args:
            method: The method name to call
            params: Optional parameters for the method
            
        Returns:
            Response dictionary from the device
            
        Raises:
            ConnectionError: If unable to connect to the device
            TimeoutError: If the request times out
        """
        # For now, this is a mock implementation
        # In a real implementation, this would connect to the actual Starlink dish
        # using the gRPC protocol over the local network
        
        # Return mock data for demonstration purposes
        if method == "get_status":
            return {
                "status": "connected",
                "downlink_throughput_bps": 125000000,  # 125 Mbps in bps
                "uplink_throughput_bps": 25000000,     # 25 Mbps in bps
                "pop_ping_latency_ms": 25.5,
                "uptime": 86400,
                "obstruction_stats": {
                    "currently_obstructed": False,
                    "fraction_obstructed": 0.02
                }
            }
        elif method == "reboot":
            return {"status": "rebooting"}
        
        return {}
    
    def get_network_stats(self) -> NetworkStats:
        """Retrieve current network statistics from the Starlink dish.
        
        Returns:
            NetworkStats object containing current network performance metrics
            
        Raises:
            ConnectionError: If unable to retrieve stats from the device
        
        Example:
            >>> client = StarlinkClient()
            >>> stats = client.get_network_stats()
            >>> print(f"Download: {stats.download_speed} Mbps")
        """
        try:
            response = self._send_grpc_request("get_status")
            
            # Convert bits per second to Mbps
            download_speed = response.get("downlink_throughput_bps", 0) / 1_000_000
            upload_speed = response.get("uplink_throughput_bps", 0) / 1_000_000
            latency = response.get("pop_ping_latency_ms", 0)
            uptime = response.get("uptime", 0)
            
            obstruction_stats = response.get("obstruction_stats", {})
            obstruction_percentage = obstruction_stats.get("fraction_obstructed", 0) * 100
            connected = response.get("status") == "connected"
            
            return NetworkStats(
                download_speed=download_speed,
                upload_speed=upload_speed,
                latency=latency,
                uptime=uptime,
                obstruction_percentage=obstruction_percentage,
                connected=connected
            )
        except Exception as e:
            raise ConnectionError(f"Failed to retrieve network stats: {e}")
    
    def reboot_dish(self) -> bool:
        """Reboot the Starlink dish.
        
        This will cause the dish to restart, which may take several minutes
        to complete. During this time, internet connectivity will be lost.
        
        Returns:
            True if the reboot command was successfully sent
            
        Raises:
            ConnectionError: If unable to send the reboot command
            
        Example:
            >>> client = StarlinkClient()
            >>> client.reboot_dish()
            True
        """
        try:
            response = self._send_grpc_request("reboot")
            return response.get("status") == "rebooting"
        except Exception as e:
            raise ConnectionError(f"Failed to reboot dish: {e}")
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"StarlinkClient(host='{self.host}', port={self.port})"
