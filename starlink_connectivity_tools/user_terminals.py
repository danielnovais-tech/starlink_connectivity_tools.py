"""
User Terminals API endpoints
"""

from typing import Dict, Any
from .client import StarlinkClient


class UserTerminalsAPI:
    """
    API client for User Terminal-related endpoints.
    
    Endpoints:
        - GET /user-terminals/{id}: Get user terminal (dish) details, including ID
        - POST /user-terminals: Activate or manage a user terminal
    """
    
    def __init__(self, client: StarlinkClient):
        """
        Initialize the User Terminals API.
        
        Args:
            client: StarlinkClient instance
        """
        self.client = client
    
    def get_user_terminal(self, terminal_id: str) -> Dict[str, Any]:
        """
        Get user terminal (dish) details, including ID.
        
        Args:
            terminal_id: The ID of the user terminal
            
        Returns:
            Dictionary containing user terminal details
            
        Example:
            >>> terminals = UserTerminalsAPI(client)
            >>> terminal = terminals.get_user_terminal('term_12345')
            >>> print(terminal['status'])
        """
        return self.client.get(f'/user-terminals/{terminal_id}')
    
    def create_user_terminal(self, terminal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Activate or manage a user terminal.
        
        Args:
            terminal_data: Dictionary containing user terminal information
            
        Returns:
            Dictionary containing created/updated user terminal details
            
        Example:
            >>> terminals = UserTerminalsAPI(client)
            >>> terminal = terminals.create_user_terminal({
            ...     'service_line_id': 'line_12345',
            ...     'serial_number': 'SN12345'
            ... })
        """
        return self.client.post('/user-terminals', json_data=terminal_data)
