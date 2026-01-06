"""
Routers API endpoints
"""

from typing import Dict, Any
from .client import StarlinkClient


class RoutersAPI:
    """
    API client for Router-related endpoints.
    
    Endpoints:
        - GET /routers/{id}/config: Get router configuration
    """
    
    def __init__(self, client: StarlinkClient):
        """
        Initialize the Routers API.
        
        Args:
            client: StarlinkClient instance
        """
        self.client = client
    
    def get_router_config(self, router_id: str) -> Dict[str, Any]:
        """
        Get router configuration.
        
        Args:
            router_id: The ID of the router
            
        Returns:
            Dictionary containing router configuration
            
        Example:
            >>> routers = RoutersAPI(client)
            >>> config = routers.get_router_config('router_12345')
            >>> print(config['ssid'])
        """
        return self.client.get(f'/routers/{router_id}/config')
