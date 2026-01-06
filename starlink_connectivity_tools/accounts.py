"""
Accounts API endpoints
"""

from typing import Dict, Any
from .client import StarlinkClient


class AccountsAPI:
    """
    API client for Account-related endpoints.
    
    Endpoints:
        - GET /account: Retrieve account details (email, customer info)
    """
    
    def __init__(self, client: StarlinkClient):
        """
        Initialize the Accounts API.
        
        Args:
            client: StarlinkClient instance
        """
        self.client = client
    
    def get_account(self) -> Dict[str, Any]:
        """
        Retrieve account details (email, customer info).
        
        Returns:
            Dictionary containing account details
            
        Example:
            >>> accounts = AccountsAPI(client)
            >>> account = accounts.get_account()
            >>> print(account['email'])
        """
        return self.client.get('/account')
