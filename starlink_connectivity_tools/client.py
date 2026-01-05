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
