"""
Addresses API endpoints
"""

from typing import Dict, Any
from .client import StarlinkClient


class AddressesAPI:
    """
    API client for Address-related endpoints.
    
    Endpoints:
        - POST /addresses: Create a new address for service activation
        - GET /addresses/{id}: Get details of a specific address
    """
    
    def __init__(self, client: StarlinkClient):
        """
        Initialize the Addresses API.
        
        Args:
            client: StarlinkClient instance
        """
        self.client = client
    
    def create_address(self, address_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new address for service activation.
        
        Args:
            address_data: Dictionary containing address information
            
        Returns:
            Dictionary containing created address details
            
        Example:
            >>> addresses = AddressesAPI(client)
            >>> address = addresses.create_address({
            ...     'street': '123 Main St',
            ...     'city': 'Seattle',
            ...     'state': 'WA',
            ...     'zip': '98101'
            ... })
        """
        return self.client.post('/addresses', json_data=address_data)
    
    def get_address(self, address_id: str) -> Dict[str, Any]:
        """
        Get details of a specific address.
        
        Args:
            address_id: The ID of the address to retrieve
            
        Returns:
            Dictionary containing address details
            
        Example:
            >>> addresses = AddressesAPI(client)
            >>> address = addresses.get_address('addr_12345')
        """
        return self.client.get(f'/addresses/{address_id}')
