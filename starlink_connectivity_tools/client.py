"""
Main client module for Starlink connectivity tools.

Provides the StarlinkClient class for interacting with Starlink user terminals
via gRPC protocol.
"""

import grpc
import ipaddress
from typing import Dict, Any, Optional, List
from datetime import datetime
Starlink client for interacting with user terminals.
"""

import grpc
from typing import Optional, List, AsyncIterator
from datetime import datetime, timedelta
import asyncio

from .models import (
    DeviceStatus,
    NetworkStats,
    TelemetryData,
    DeviceLocation,
    WiFiStatus,
    WiFiConfig,
    DishConfig,
    AccountData,
    Alert,
    AlertLevel,
    DeviceState,
    WiFiClient,
    HistoricalData,
)


class StarlinkConnectionError(Exception):
    """Raised when connection to Starlink device fails."""
    pass


class StarlinkAuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


class StarlinkOperationError(Exception):
    """Raised when an operation fails."""
    pass


class StarlinkClient:
    """
    Client for interacting with Starlink user terminals.
    
    This class provides methods to retrieve status, configure settings,
    and manage Starlink dishes either locally or remotely.
    
    Args:
        target: Connection target (default: "192.168.100.1:9200" for local connection)
        auth_token: Optional authentication token for remote connections
        secure: Force secure/insecure channel (overrides auto-detection)
    """
    
    def __init__(self, target: str = "192.168.100.1:9200", auth_token: Optional[str] = None, 
                 secure: Optional[bool] = None):
        """Initialize the Starlink client."""
        self.target = target
        self.auth_token = auth_token
        self._secure = secure
        self._channel = None
        self._stub = None
    
    def _is_private_ip(self, hostname: str) -> bool:
        """Check if hostname is a private IP address."""
        try:
            # Extract IP from hostname:port
            ip_str = hostname.split(':')[0]
            ip = ipaddress.ip_address(ip_str)
            return ip.is_private
        except (ValueError, IndexError):
            # Not a valid IP address, assume it's a hostname (remote)
            return False
    
    def connect(self) -> None:
        """Establish connection to the Starlink dish."""
        if self._channel is None:
            # Determine if we should use secure channel
            if self._secure is not None:
                # Explicit secure parameter takes precedence
                use_secure = self._secure
            elif self.auth_token:
                # If auth token provided, use secure channel
                use_secure = True
            else:
                # Auto-detect: use secure for non-private IPs
                use_secure = not self._is_private_ip(self.target)
            
            if use_secure:
                # Remote/secure connection
                credentials = grpc.ssl_channel_credentials()
                self._channel = grpc.secure_channel(self.target, credentials)
            else:
                # Local/insecure connection
                self._channel = grpc.insecure_channel(self.target)
            # Note: In a real implementation, this would use the generated gRPC stub
            # from the Starlink proto files
    
    def disconnect(self) -> None:
        """Close the connection to the Starlink dish."""
    Provides methods for device management, network monitoring, and configuration.
    Supports both local (direct) and remote (via Starlink API) connections.
    
    Args:
        host: Hostname or IP address of the Starlink device (default: 192.168.100.1)
        port: gRPC port (default: 9200)
        use_remote: Whether to use remote API instead of local connection
        api_key: API key for remote authentication (required if use_remote=True)
        timeout: Default timeout for operations in seconds
    
    Example:
        >>> client = StarlinkClient()
        >>> status = client.get_status()
        >>> print(f"Device is {status.state.value}")
    """
    
    DEFAULT_HOST = "192.168.100.1"
    DEFAULT_PORT = 9200
    DEFAULT_TIMEOUT = 10
    
    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        use_remote: bool = False,
        api_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """Initialize the Starlink client."""
        self.host = host
        self.port = port
        self.use_remote = use_remote
        self.api_key = api_key
        self.timeout = timeout
        self._channel: Optional[grpc.Channel] = None
        self._stub = None
        
        if use_remote and not api_key:
            raise ValueError("api_key is required when use_remote=True")
    
    def connect(self) -> None:
        """
        Establish connection to the Starlink device.
        
        Raises:
            StarlinkConnectionError: If connection fails
            StarlinkAuthenticationError: If authentication fails
        """
        try:
            if self.use_remote:
                # For remote API, connection is established per-request
                # This is a placeholder for authentication validation
                if not self._validate_api_key():
                    raise StarlinkAuthenticationError("Invalid API key")
            else:
                # Establish gRPC channel for local connection
                self._channel = grpc.insecure_channel(
                    f"{self.host}:{self.port}",
                    options=[
                        ('grpc.max_receive_message_length', 50 * 1024 * 1024),
                    ]
                )
                # In a real implementation, this would initialize the gRPC stub
                # self._stub = SpaceXAPIStub(self._channel)
        except Exception as e:
            raise StarlinkConnectionError(f"Failed to connect: {str(e)}")
    
    def disconnect(self) -> None:
        """Close the connection to the Starlink device."""
        if self._channel:
            self._channel.close()
            self._channel = None
            self._stub = None
"""Starlink Dish gRPC Client.

This module provides a client for interacting with the Starlink dish's
unauthenticated gRPC API exposed at 192.168.100.1:9200.
"""

import grpc
from typing import Optional, Dict, Any, List
from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc


class StarlinkDishClient:
    """Client for interacting with Starlink dish gRPC API.
    
    The Starlink user terminal (dish) exposes an unauthenticated gRPC API
    for monitoring and control. This client provides methods to query device
    status, network statistics, telemetry, and perform actions.
    
    Access Methods:
    - Local: Direct connection to 192.168.100.1:9200 (no authentication)
    - Remote: Via Starlink's remote API with session cookies (valid 15 days)
    
    Attributes:
        address: The gRPC server address (host:port)
        channel: The gRPC channel
        use_reflection: Whether to use server reflection for service discovery
    """
    
    DEFAULT_LOCAL_ADDRESS = "192.168.100.1:9200"
    
    def __init__(
        self,
        address: Optional[str] = None,
        session_cookie: Optional[str] = None,
        use_reflection: bool = True,
        insecure: bool = True,
        timeout: int = 10,
    ):
        """Initialize the Starlink dish client.
        
        Args:
            address: The gRPC server address. Defaults to local dish address.
            session_cookie: Optional session cookie for remote access.
            use_reflection: Whether to use server reflection. Defaults to True.
            insecure: Whether to use insecure channel. Defaults to True for local access.
            timeout: Default timeout for RPC calls in seconds.
        """
        self.address = address or self.DEFAULT_LOCAL_ADDRESS
        self.session_cookie = session_cookie
        self.use_reflection = use_reflection
        self.timeout = timeout
        self._channel: Optional[grpc.Channel] = None
        self._stubs: Dict[str, Any] = {}
        
    def connect(self) -> None:
        """Establish connection to the Starlink dish gRPC server.
        
        Raises:
            grpc.RpcError: If connection fails.
        """
        if self._channel:
            return
            
        # Create channel options
        options = [
            ('grpc.max_receive_message_length', 1024 * 1024 * 100),  # 100 MB
            ('grpc.max_send_message_length', 1024 * 1024 * 100),
        ]
        
        # Add authentication metadata if session cookie provided
        if self.session_cookie:
            options.append(('grpc.default_authority', self.address))
            
        # Create insecure or secure channel
        self._channel = grpc.insecure_channel(self.address, options=options)
        
        # Test connection
        try:
            grpc.channel_ready_future(self._channel).result(timeout=self.timeout)
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to Starlink dish at {self.address} within {self.timeout}s"
            ) from e
    
    def close(self) -> None:
        """Close the gRPC channel."""
        if self._channel:
            self._channel.close()
            self._channel = None
            self._stubs.clear()
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retrieve current status of the Starlink dish.
        
        Returns information about connectivity, alerts, uptime, and current state.
        
        Returns:
            Dict containing:
                - uptime: Device uptime in seconds
                - state: Current device state (e.g., "CONNECTED", "SEARCHING")
                - alerts: List of active alerts
                - is_connected: Boolean indicating connection status
                - software_version: Current firmware version
                
        Raises:
            grpc.RpcError: If the connection fails
        """
        # Placeholder implementation
        # In real implementation, this would call the gRPC method
        return {
            "uptime": 0,
            "state": "UNKNOWN",
            "alerts": [],
            "is_connected": False,
            "software_version": "unknown"
        }
    
    def get_history(self, samples: int = 300) -> Dict[str, Any]:
        """
        Retrieve historical data from the Starlink dish.
        
        Args:
            samples: Number of historical samples to retrieve (default: 300)
            
        Returns:
            Dict containing:
                - timestamps: List of timestamp values
                - download_throughput: Historical download speeds
                - upload_throughput: Historical upload speeds
                - latency: Historical latency values
                - packet_loss: Historical packet loss percentages
                - obstructed: Historical obstruction data
                
        Raises:
            grpc.RpcError: If the connection fails
        """
        # Placeholder implementation
        return {
            "timestamps": [],
            "download_throughput": [],
            "upload_throughput": [],
            "latency": [],
            "packet_loss": [],
            "obstructed": []
        }
    
    def get_network_stats(self) -> Dict[str, Any]:
        """
        Get current network statistics.
        
        Returns network performance metrics including speeds, latency, and packet loss.
        
        Returns:
            Dict containing:
                - download_speed_mbps: Current download speed in Mbps
                - upload_speed_mbps: Current upload speed in Mbps
                - latency_ms: Current latency in milliseconds
                - packet_loss_percent: Current packet loss percentage
                - uptime_seconds: Network uptime in seconds
                
        Raises:
            grpc.RpcError: If the connection fails
        """
        # Placeholder implementation
        return {
            "download_speed_mbps": 0.0,
            "upload_speed_mbps": 0.0,
            "latency_ms": 0.0,
            "packet_loss_percent": 0.0,
            "uptime_seconds": 0
        }
    
    def get_telemetry(self, streaming: bool = False) -> Dict[str, Any]:
        """
        Retrieve device telemetry including alerts, errors, and warnings.
        
        Args:
            streaming: If True, would return a streaming iterator. Currently not implemented
                      in this placeholder version (default: False)
            
        Returns:
            Dict containing:
                - alerts: List of current alerts
                - errors: List of errors
                - warnings: List of warnings
                - temperature_celsius: Device temperature
                - power_usage_watts: Current power consumption
                
        Raises:
            grpc.RpcError: If the connection fails
            NotImplementedError: If streaming=True (not yet implemented)
        """
        # Placeholder implementation
        if streaming:
            raise NotImplementedError(
                "Streaming telemetry is not yet implemented in this version. "
                "Set streaming=False to get snapshot telemetry data."
            )
        
        return {
            "alerts": [],
            "errors": [],
            "warnings": [],
            "temperature_celsius": 0.0,
            "power_usage_watts": 0.0
        }
    
    def reboot_dish(self) -> Dict[str, Any]:
        """
        Restart the Starlink user terminal.
        
        Sends a reboot command to the dish. The device will disconnect
        and restart, which may take several minutes.
        
        Returns:
            Dict containing:
                - success: Boolean indicating if reboot command was accepted
                - message: Status message
                
        Raises:
            grpc.RpcError: If the connection fails
        """
        # Placeholder implementation
        return {
            "success": False,
            "message": "Reboot command not implemented"
        }
    
    def set_dish_config(self, 
                       snow_melt_mode: Optional[bool] = None,
                       power_save_mode: Optional[bool] = None,
                       **kwargs) -> Dict[str, Any]:
        """
        Configure Starlink dish settings.
        
        Args:
            snow_melt_mode: Enable/disable snow melt mode
            power_save_mode: Enable/disable power saving mode
            **kwargs: Additional configuration options
            
        Returns:
            Dict containing:
                - success: Boolean indicating if configuration was applied
                - message: Status message
                - updated_config: The new configuration settings
                
        Raises:
            grpc.RpcError: If the connection fails
        """
        # Placeholder implementation
        config = {}
        if snow_melt_mode is not None:
            config["snow_melt_mode"] = snow_melt_mode
        if power_save_mode is not None:
            config["power_save_mode"] = power_save_mode
        config.update(kwargs)
        
        return {
            "success": False,
            "message": "Configuration update not implemented",
            "updated_config": config
        }
    
    def get_device_location(self, remote: bool = False) -> Dict[str, Any]:
        """
        Get the device location.
        
        Args:
            remote: If True, returns H3 cell location; if False, returns precise GPS location
            
        Returns:
            Dict containing:
                - latitude: Device latitude (if local/precise)
                - longitude: Device longitude (if local/precise)
                - altitude: Device altitude in meters (if local/precise)
                - h3_cell: H3 cell identifier (if remote)
                
        Raises:
            grpc.RpcError: If the connection fails
        """
        # Placeholder implementation
        if remote:
            return {"h3_cell": "unknown"}
        else:
            return {
                "latitude": 0.0,
                "longitude": 0.0,
                "altitude": 0.0
            }
    
    def get_wifi_status(self) -> Dict[str, Any]:
        """
        Get WiFi status and connected clients.
        
        Returns:
            Dict containing:
                - ssid: Current WiFi SSID
                - enabled: Whether WiFi is enabled
                - channel: Current WiFi channel
                - connected_clients: List of connected client devices
                - signal_strength: WiFi signal strength
                
        Raises:
            grpc.RpcError: If the connection fails
        """
        # Placeholder implementation
        return {
            "ssid": "",
            "enabled": False,
            "channel": 0,
            "connected_clients": [],
            "signal_strength": 0
        }
    
    def change_wifi_config(self,
                          ssid: Optional[str] = None,
                          password: Optional[str] = None,
                          bypass_mode: Optional[bool] = None,
                          **kwargs) -> Dict[str, Any]:
        """
        Modify WiFi configuration.
        
        Args:
            ssid: New WiFi SSID
            password: New WiFi password
            bypass_mode: Enable/disable bypass mode
            **kwargs: Additional WiFi configuration options
            
        Returns:
            Dict containing:
                - success: Boolean indicating if configuration was applied
                - message: Status message
                - updated_config: The new WiFi configuration
                
        Raises:
            grpc.RpcError: If the connection fails
        """
        # Placeholder implementation
        config = {}
        if ssid is not None:
            config["ssid"] = ssid
        if password is not None:
            config["password_updated"] = True  # Indicate password was updated without exposing it
        if bypass_mode is not None:
            config["bypass_mode"] = bypass_mode
        config.update(kwargs)
        
        return {
            "success": False,
            "message": "WiFi configuration update not implemented",
            "updated_config": config
        }
    
    def get_account_data(self) -> Dict[str, Any]:
        """
        Get basic account information (remote only).
        
        This method requires authentication and works only with remote connections.
        
        Returns:
            Dict containing:
                - email: Account email address
                - name: Account holder name
                - service_plan: Current service plan
                - account_number: Account identifier
                
        Raises:
            grpc.RpcError: If the connection fails
            PermissionError: If not authenticated for remote access
        """
        # Placeholder implementation
        if not self.auth_token:
            raise PermissionError("Account data requires remote authentication")
        
        return {
            "email": "",
            "name": "",
            "service_plan": "",
            "account_number": ""
        }
    def _validate_api_key(self) -> bool:
        """Validate API key (placeholder)."""
        # In a real implementation, this would validate against Starlink API
        return bool(self.api_key)
    
    def get_status(self) -> DeviceStatus:
        """
        Get the current status of the Starlink device.
        
        Returns:
            DeviceStatus: Current device status including connectivity and alerts
            
        Raises:
            StarlinkConnectionError: If not connected or connection fails
            StarlinkOperationError: If the operation fails
            
        Example:
            >>> status = client.get_status()
            >>> if status.is_online():
            ...     print("Device is online")
        """
        if not self.use_remote and not self._channel:
            raise StarlinkConnectionError("Not connected. Call connect() first.")
        
        try:
            # In a real implementation, this would make a gRPC call
            # response = self._stub.GetStatus(...)
            
            # Placeholder implementation
            return DeviceStatus(
                state=DeviceState.ONLINE,
                uptime_seconds=86400,
                connected=True,
                alerts=[],
                hardware_version="rev2_proto3",
                software_version="2024.01.15.mr12345",
                id="ut01000000-00000000-00000000",
                timestamp=datetime.now(),
            )
        except Exception as e:
            raise StarlinkOperationError(f"Failed to get status: {str(e)}")
    
    def get_history(
        self,
        duration_hours: int = 12,
        interval_minutes: int = 5,
    ) -> List[HistoricalData]:
        """
        Retrieve historical status and network data.
        
        Args:
            duration_hours: Number of hours of historical data to retrieve
            interval_minutes: Interval between data points in minutes
            
        Returns:
            List of historical data points
            
        Raises:
            StarlinkOperationError: If the operation fails
            
        Example:
            >>> history = client.get_history(duration_hours=24)
            >>> for entry in history:
            ...     if entry.network_stats:
            ...         print(f"{entry.timestamp}: {entry.network_stats.latency_ms}ms")
        """
        if not self.use_remote and not self._channel:
            raise StarlinkConnectionError("Not connected. Call connect() first.")
        
        try:
            # Placeholder implementation
            history = []
            now = datetime.now()
            num_points = (duration_hours * 60) // interval_minutes
            
            for i in range(num_points):
                timestamp = now - timedelta(minutes=i * interval_minutes)
                history.append(
                    HistoricalData(
                        timestamp=timestamp,
                        status=None,  # Would be populated from real API
                        network_stats=None,  # Would be populated from real API
                    )
                )
            
            return history
        except Exception as e:
            raise StarlinkOperationError(f"Failed to get history: {str(e)}")
    
    def get_network_stats(self) -> NetworkStats:
        """
        Get current network performance statistics.
        
        Returns:
            NetworkStats: Download/upload speeds, latency, packet loss
            
        Raises:
            StarlinkOperationError: If the operation fails
            
        Example:
            >>> stats = client.get_network_stats()
            >>> print(f"Download: {stats.download_mbps} Mbps")
            >>> print(f"Latency: {stats.latency_ms} ms")
            >>> if stats.is_healthy():
            ...     print("Network performance is good")
        """
        if not self.use_remote and not self._channel:
            raise StarlinkConnectionError("Not connected. Call connect() first.")
        
        try:
            # Placeholder implementation
            return NetworkStats(
                download_mbps=150.5,
                upload_mbps=25.3,
                latency_ms=35.2,
                packet_loss_percent=0.1,
                timestamp=datetime.now(),
                ping_drop_rate=0.05,
                obstructions_percent=0.0,
                downlink_throughput_bps=150500000,
                uplink_throughput_bps=25300000,
            )
        except Exception as e:
            raise StarlinkOperationError(f"Failed to get network stats: {str(e)}")
    
    def get_telemetry(self) -> TelemetryData:
        """
        Get device telemetry including alerts, errors, and warnings.
        
        Returns:
            TelemetryData: Device alerts, temperature, power usage, etc.
            
        Raises:
            StarlinkOperationError: If the operation fails
            
        Example:
            >>> telemetry = client.get_telemetry()
            >>> if telemetry.has_critical_alerts():
            ...     for alert in telemetry.get_alerts_by_level(AlertLevel.CRITICAL):
            ...         print(f"Critical: {alert.message}")
        """
        if not self.use_remote and not self._channel:
            raise StarlinkConnectionError("Not connected. Call connect() first.")
        
        try:
            # Placeholder implementation
            return TelemetryData(
                alerts=[],
                temperature_celsius=45.5,
                power_input_watts=85.2,
                uptime_seconds=86400,
                timestamp=datetime.now(),
                errors=[],
                warnings=[],
            )
        except Exception as e:
            raise StarlinkOperationError(f"Failed to get telemetry: {str(e)}")
    
    async def stream_telemetry(self) -> AsyncIterator[TelemetryData]:
        """
        Stream telemetry data continuously.
        
        Yields:
            TelemetryData: Real-time telemetry updates
            
        Raises:
            StarlinkOperationError: If streaming fails
            
        Example:
            >>> async for telemetry in client.stream_telemetry():
            ...     print(f"Temperature: {telemetry.temperature_celsius}°C")
            ...     if telemetry.has_critical_alerts():
            ...         break
        """
        if not self.use_remote and not self._channel:
            raise StarlinkConnectionError("Not connected. Call connect() first.")
        
        try:
            # Placeholder implementation - would use gRPC streaming
            while True:
                yield self.get_telemetry()
                await asyncio.sleep(1)  # Update interval
        except Exception as e:
            raise StarlinkOperationError(f"Failed to stream telemetry: {str(e)}")
    
    def reboot_dish(self) -> bool:
        """
        Reboot the Starlink user terminal.
        
        Returns:
            True if reboot command was sent successfully
            
        Raises:
            StarlinkOperationError: If the operation fails
            
        Example:
            >>> if client.reboot_dish():
            ...     print("Dish is rebooting...")
        """
        if not self.use_remote and not self._channel:
            raise StarlinkConnectionError("Not connected. Call connect() first.")
        
        try:
            # In a real implementation, this would send a reboot command
            # response = self._stub.Reboot(...)
            return True
        except Exception as e:
            raise StarlinkOperationError(f"Failed to reboot dish: {str(e)}")
    
    def set_dish_config(self, config: DishConfig) -> bool:
        """
        Configure dish settings.
        
        Args:
            config: Dish configuration with desired settings
            
        Returns:
            True if configuration was applied successfully
            
        Raises:
            StarlinkOperationError: If the operation fails
            
        Example:
            >>> config = DishConfig(snow_melt_mode_enabled=True)
            >>> client.set_dish_config(config)
        """
        if not self.use_remote and not self._channel:
            raise StarlinkConnectionError("Not connected. Call connect() first.")
        
        try:
            # In a real implementation, this would apply the configuration
            # response = self._stub.SetConfig(...)
            return True
        except Exception as e:
            raise StarlinkOperationError(f"Failed to set dish config: {str(e)}")
    
    def get_dish_config(self) -> DishConfig:
        """
        Get current dish configuration.
        
        Returns:
            DishConfig: Current dish settings
            
        Raises:
            StarlinkOperationError: If the operation fails
        """
        if not self.use_remote and not self._channel:
            raise StarlinkConnectionError("Not connected. Call connect() first.")
        
        try:
            # Placeholder implementation
            return DishConfig(
                snow_melt_mode_enabled=False,
                power_save_mode_enabled=False,
                stow_requested=False,
                location_request_mode="none",
            )
        except Exception as e:
            raise StarlinkOperationError(f"Failed to get dish config: {str(e)}")
    
    def get_device_location(self) -> DeviceLocation:
        """
        Get device geographical location.
        
        Returns precise location when connected locally, or H3 cell when remote.
        
        Returns:
            DeviceLocation: Location information
            
        Raises:
            StarlinkOperationError: If the operation fails
            
        Example:
            >>> location = client.get_device_location()
            >>> if location.has_coordinates():
            ...     print(f"Lat: {location.latitude}, Lon: {location.longitude}")
            >>> else:
            ...     print(f"H3 Cell: {location.h3_cell}")
        """
        if not self.use_remote and not self._channel:
            raise StarlinkConnectionError("Not connected. Call connect() first.")
        
        try:
            # Placeholder implementation
            if self.use_remote:
                # Remote returns H3 cell for privacy
                return DeviceLocation(
                    h3_cell="8c2a1072b181bff",
                    is_precise=False,
                )
            else:
                # Local returns precise coordinates
                return DeviceLocation(
                    latitude=37.7749,
                    longitude=-122.4194,
                    altitude_meters=150.5,
                    is_precise=True,
                )
        except Exception as e:
            raise StarlinkOperationError(f"Failed to get device location: {str(e)}")
    
    def get_wifi_status(self) -> WiFiStatus:
        """
        Get WiFi status and connected clients.
        
        Returns:
            WiFiStatus: SSID, connected clients, signal strength
            
        Raises:
            StarlinkOperationError: If the operation fails
            
        Example:
            >>> wifi = client.get_wifi_status()
            >>> print(f"SSID: {wifi.ssid}")
            >>> print(f"Connected clients: {wifi.client_count()}")
            >>> for client in wifi.connected_clients:
            ...     print(f"  - {client.hostname or client.mac_address}")
        """
        if not self.use_remote and not self._channel:
            raise StarlinkConnectionError("Not connected. Call connect() first.")
        
        try:
            # Placeholder implementation
            return WiFiStatus(
                ssid="STARLINK",
                enabled=True,
                channel=36,
                connected_clients=[
                    WiFiClient(
                        mac_address="AA:BB:CC:DD:EE:FF",
                        ip_address="192.168.1.100",
                        hostname="laptop",
                        signal_strength=-45,
                        connected_seconds=3600,
                    )
                ],
                signal_strength=-35,
                is_5ghz=True,
                is_2_4ghz=False,
            )
        except Exception as e:
            raise StarlinkOperationError(f"Failed to get WiFi status: {str(e)}")
    
    def set_wifi_config(self, config: WiFiConfig) -> bool:
        """
        Modify WiFi configuration.
        
        Args:
            config: WiFi configuration with desired settings
            
        Returns:
            True if configuration was applied successfully
            
        Raises:
            ValueError: If configuration validation fails
            StarlinkOperationError: If the operation fails
            
        Example:
            >>> config = WiFiConfig(ssid="MyStarlink", password="NewPassword123")
            >>> client.set_wifi_config(config)
        """
        if not self.use_remote and not self._channel:
            raise StarlinkConnectionError("Not connected. Call connect() first.")
        
        # Validate configuration
        if not config.validate_ssid():
            raise ValueError("SSID must be between 1 and 32 characters")
        if not config.validate_password():
            raise ValueError("Password must be between 8 and 63 characters")
        
        try:
            # In a real implementation, this would apply the WiFi configuration
            # response = self._stub.SetWifiConfig(...)
            return True
        except Exception as e:
            raise StarlinkOperationError(f"Failed to set WiFi config: {str(e)}")
    
    def get_account_data(self) -> AccountData:
        """
        Get account information (remote only).
        
        Returns:
            AccountData: Service line, subscription status, data usage
            
        Raises:
            StarlinkOperationError: If the operation fails or not using remote connection
            
        Example:
            >>> account = client.get_account_data()
            >>> if account.is_near_limit():
            ...     print("Warning: Approaching data limit")
        """
        if not self.use_remote:
            raise StarlinkOperationError("Account data is only available via remote API")
        
        try:
            # Placeholder implementation
            return AccountData(
                service_line_number="SL-12345-67890",
                account_number="ACC-98765",
                active_subscription=True,
                data_limit_gb=1000.0,
                data_used_gb=450.5,
            )
        except Exception as e:
            raise StarlinkOperationError(f"Failed to get account data: {str(e)}")
        self.close()
        return False
    
    def discover_services(self) -> List[str]:
        """Discover available gRPC services using server reflection.
        
        Returns:
            List of service names available on the server.
            
        Raises:
            RuntimeError: If reflection is not available or fails.
        """
        if not self._channel:
            self.connect()
            
        try:
            reflection_stub = reflection_pb2_grpc.ServerReflectionStub(self._channel)
            
            # List services
            request = reflection_pb2.ServerReflectionRequest(
                list_services=""
            )
            
            responses = reflection_stub.ServerReflectionInfo(iter([request]))
            
            services = []
            for response in responses:
                if response.HasField('list_services_response'):
                    for service in response.list_services_response.service:
                        services.append(service.name)
                    break
                    
            return services
            
        except grpc.RpcError as e:
            raise RuntimeError(f"Failed to discover services: {e.details()}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the Starlink dish.
        
        This method queries the device for its current operational status,
        including connection state, uptime, and basic health metrics.
        
        Returns:
            Dictionary containing device status information.
            
        Raises:
            grpc.RpcError: If the RPC call fails.
            NotImplementedError: If proto files are not loaded.
        """
        # This is a placeholder - actual implementation requires proto files
        # or dynamic message creation from reflection
        raise NotImplementedError(
            "Status query requires Starlink proto files. "
            "Use discover_services() to find available services, "
            "then load the appropriate proto files or use grpcurl."
        )
    
    def get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics from the Starlink dish.
        
        Returns network performance metrics including throughput, latency,
        packet loss, and connection quality.
        
        Returns:
            Dictionary containing network statistics.
            
        Raises:
            grpc.RpcError: If the RPC call fails.
            NotImplementedError: If proto files are not loaded.
        """
        raise NotImplementedError(
            "Network stats query requires Starlink proto files. "
            "Use discover_services() to find available services."
        )
    
    def get_telemetry(self) -> Dict[str, Any]:
        """Get telemetry data from the Starlink dish.
        
        Returns detailed telemetry including temperature, power consumption,
        signal strength, and other operational metrics.
        
        Returns:
            Dictionary containing telemetry data.
            
        Raises:
            grpc.RpcError: If the RPC call fails.
            NotImplementedError: If proto files are not loaded.
        """
        raise NotImplementedError(
            "Telemetry query requires Starlink proto files. "
            "Use discover_services() to find available services."
        )
    
    def reboot(self) -> bool:
        """Reboot the Starlink dish.
        
        Sends a reboot command to the device. The dish will go offline
        and restart, which may take several minutes.
        
        Returns:
            True if reboot command was accepted.
            
        Raises:
            grpc.RpcError: If the RPC call fails.
            NotImplementedError: If proto files are not loaded.
        """
        raise NotImplementedError(
            "Reboot command requires Starlink proto files. "
            "Use discover_services() to find available services."
        )
    
    def set_configuration(self, config: Dict[str, Any]) -> bool:
        """Configure the Starlink dish.
        
        Args:
            config: Configuration parameters to set.
            
        Returns:
            True if configuration was applied successfully.
            
        Raises:
            grpc.RpcError: If the RPC call fails.
            NotImplementedError: If proto files are not loaded.
        """
        raise NotImplementedError(
            "Configuration requires Starlink proto files. "
            "Use discover_services() to find available services."
        )
    
    def call_method(
        self,
        service_name: str,
        method_name: str,
        request_data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make a generic RPC call to any service method.
        
        This is a low-level method for calling arbitrary gRPC methods
        when proto files are available.
        
        Args:
            service_name: Full service name (e.g., 'SpaceX.API.Device.Device')
            method_name: Method name to call
            request_data: Request data as dictionary
            
        Returns:
            Response from the RPC call.
            
        Raises:
            grpc.RpcError: If the RPC call fails.
            NotImplementedError: If proto files are not loaded.
        """
        raise NotImplementedError(
            "Generic method calls require Starlink proto files. "
            "Proto files must be compiled and imported to use this method."
        )
"""
Base client for Starlink API
"""

import requests
from typing import Dict, Any, Optional


class StarlinkClient:
    """
    Base client for interacting with Starlink API.
    
    This client provides the base functionality for making HTTP requests
    to the Starlink API endpoints.
    """
    
    def __init__(self, base_url: str = "https://api.starlink.com", api_key: Optional[str] = None):
        """
        Initialize the Starlink API client.
        
        Args:
            base_url: Base URL for the Starlink API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}'
            })
    
    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the Starlink API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            params: Query parameters
            json_data: JSON payload for POST/PUT requests
            headers: Additional headers
            
        Returns:
            Response data as dictionary
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = f"{self.base_url}{path}"
        
        request_headers = {}
        if headers:
            request_headers.update(headers)
        
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            headers=request_headers
        )
        
        response.raise_for_status()
        return response.json()
    
    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self._make_request('GET', path, params=params)
    
    def post(self, path: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request."""
        return self._make_request('POST', path, json_data=json_data)
