"""
TLS API endpoints
"""

from typing import Dict, Any
from .client import StarlinkClient


class TLSAPI:
    """
    API client for TLS-related endpoints.
    
    Endpoints:
        - GET /tls: Retrieve TLS configuration for secure communications
    """
    
    def __init__(self, client: StarlinkClient):
        """
        Initialize the TLS API.
        
        Args:
            client: StarlinkClient instance
        """
        self.client = client
    
    def get_tls_config(self) -> Dict[str, Any]:
        """
        Retrieve TLS configuration for secure communications.
        
        Returns:
            Dictionary containing TLS configuration
            
        Example:
            >>> tls = TLSAPI(client)
            >>> config = tls.get_tls_config()
            >>> print(config['certificate'])
        """
        return self.client.get('/tls')
