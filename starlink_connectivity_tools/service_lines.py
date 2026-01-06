"""
Service Lines API endpoints
"""

from typing import Dict, Any
from .client import StarlinkClient


class ServiceLinesAPI:
    """
    API client for Service Line-related endpoints.
    
    Endpoints:
        - POST /service-lines: Create a new service line (for activation)
        - GET /service-lines/{id}: Retrieve service line details
    """
    
    def __init__(self, client: StarlinkClient):
        """
        Initialize the Service Lines API.
        
        Args:
            client: StarlinkClient instance
        """
        self.client = client
    
    def create_service_line(self, service_line_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new service line (for activation).
        
        Args:
            service_line_data: Dictionary containing service line information
            
        Returns:
            Dictionary containing created service line details
            
        Example:
            >>> service_lines = ServiceLinesAPI(client)
            >>> line = service_lines.create_service_line({
            ...     'address_id': 'addr_12345',
            ...     'product_id': 'prod_12345'
            ... })
        """
        return self.client.post('/service-lines', json_data=service_line_data)
    
    def get_service_line(self, service_line_id: str) -> Dict[str, Any]:
        """
        Retrieve service line details.
        
        Args:
            service_line_id: The ID of the service line to retrieve
            
        Returns:
            Dictionary containing service line details
            
        Example:
            >>> service_lines = ServiceLinesAPI(client)
            >>> line = service_lines.get_service_line('line_12345')
        """
        return self.client.get(f'/service-lines/{service_line_id}')
