"""
Subscriptions API endpoints
"""

from typing import Dict, Any
from .client import StarlinkClient


class SubscriptionsAPI:
    """
    API client for Subscription-related endpoints.
    
    Endpoints:
        - GET /subscriptions: List available or active subscription products
    """
    
    def __init__(self, client: StarlinkClient):
        """
        Initialize the Subscriptions API.
        
        Args:
            client: StarlinkClient instance
        """
        self.client = client
    
    def get_subscriptions(self) -> Dict[str, Any]:
        """
        List available or active subscription products.
        
        Returns:
            Dictionary containing subscription products
            
        Example:
            >>> subscriptions = SubscriptionsAPI(client)
            >>> subs = subscriptions.get_subscriptions()
            >>> for sub in subs['items']:
            ...     print(sub['name'])
        """
        return self.client.get('/subscriptions')
