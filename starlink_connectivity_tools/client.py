"""
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
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
    
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
