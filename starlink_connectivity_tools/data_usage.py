"""
Data Usage API endpoints
"""

from typing import Dict, Any
from .client import StarlinkClient


class DataUsageAPI:
    """
    API client for Data Usage-related endpoints.
    
    Endpoints:
        - GET /data-usage: Fetch data usage statistics for the account or devices
    """
    
    def __init__(self, client: StarlinkClient):
        """
        Initialize the Data Usage API.
        
        Args:
            client: StarlinkClient instance
        """
        self.client = client
    
    def get_data_usage(self) -> Dict[str, Any]:
        """
        Fetch data usage statistics for the account or devices.
        
        Returns:
            Dictionary containing data usage statistics
            
        Example:
            >>> data_usage = DataUsageAPI(client)
            >>> usage = data_usage.get_data_usage()
            >>> print(usage['total_bytes'])
        """
        return self.client.get('/data-usage')
