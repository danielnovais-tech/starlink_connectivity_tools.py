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
