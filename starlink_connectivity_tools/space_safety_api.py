"""
Starlink Space Safety API Client

This module provides a Python client for the Starlink Space Safety API
hosted at space-safety.starlink.com. It allows satellite operators to submit
ephemeris files and screen against the Starlink constellation for space
traffic coordination.
"""

import requests
from typing import Optional, Dict, Any, List


class SpaceSafetyAPI:
    """
    Client for interacting with the Starlink Space Safety API.
    
    The Space Safety API is designed for satellite operators to:
    - Submit ephemeris files
    - Screen against the Starlink constellation
    - Coordinate space traffic
    
    Attributes:
        base_url (str): The base URL for the Space Safety API
        api_key (str): Optional API key for authentication
        session (requests.Session): HTTP session for making requests
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://space-safety.starlink.com"):
        """
        Initialize the Space Safety API client.
        
        Args:
            api_key: Optional API key for authentication
            base_url: Base URL for the API (default: https://space-safety.starlink.com)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
        else:
            self.session.headers.update({
                'Content-Type': 'application/json'
            })
    
    def submit_ephemeris(self, ephemeris_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit ephemeris data for a satellite.
        
        Ephemeris data contains the orbital parameters and predicted positions
        of a satellite, which is used for conjunction screening.
        
        Args:
            ephemeris_data: Dictionary containing ephemeris information.
                Expected format:
                {
                    "satellite_id": str,
                    "epoch": str (ISO 8601 format),
                    "state_vector": {
                        "position": [x, y, z],  # km
                        "velocity": [vx, vy, vz]  # km/s
                    },
                    "covariance_matrix": [...],  # Optional
                    "metadata": {...}  # Optional
                }
        
        Returns:
            Response from the API containing submission status and details
            
        Raises:
            Exception: If the API request fails
        """
        endpoint = f"{self.base_url}/api/v1/ephemeris/submit"
        
        try:
            response = self.session.post(endpoint, json=ephemeris_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to submit ephemeris: {str(e)}")
    
    def submit_ephemeris_file(self, file_path: str, file_format: str = "oem") -> Dict[str, Any]:
        """
        Submit an ephemeris file (e.g., OEM, TLE format).
        
        Args:
            file_path: Path to the ephemeris file
            file_format: Format of the file (oem, tle, etc.)
        
        Returns:
            Response from the API containing submission status
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            Exception: If the API request fails
        """
        endpoint = f"{self.base_url}/api/v1/ephemeris/upload"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path, f, 'application/octet-stream')}
                data = {'format': file_format}
                
                # Temporarily remove Content-Type header for multipart upload
                headers = dict(self.session.headers)
                if 'Content-Type' in headers:
                    del headers['Content-Type']
                
                response = self.session.post(endpoint, files=files, data=data, headers=headers)
                response.raise_for_status()
                return response.json()
        except FileNotFoundError:
            raise FileNotFoundError(f"Ephemeris file not found: {file_path}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to upload ephemeris file: {str(e)}")
    
    def screen_conjunction(self, satellite_id: str, time_window: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Screen for potential conjunctions with the Starlink constellation.
        
        Args:
            satellite_id: Identifier for the satellite to screen
            time_window: Optional time window for screening
                {
                    "start": str (ISO 8601 format),
                    "end": str (ISO 8601 format)
                }
        
        Returns:
            Dictionary containing screening results:
            {
                "satellite_id": str,
                "conjunctions": [
                    {
                        "starlink_satellite_id": str,
                        "time_of_closest_approach": str,
                        "miss_distance": float,  # km
                        "probability_of_collision": float,
                        "screening_volume_entered": bool
                    },
                    ...
                ],
                "total_events": int
            }
            
        Raises:
            Exception: If the API request fails
        """
        endpoint = f"{self.base_url}/api/v1/screening/conjunction"
        
        params = {"satellite_id": satellite_id}
        if time_window:
            params.update(time_window)
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to screen for conjunctions: {str(e)}")
    
    def get_starlink_constellation_data(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve current Starlink constellation data.
        
        Args:
            filters: Optional filters for constellation data
                {
                    "shell": str,  # Orbital shell identifier
                    "active_only": bool,
                    "region": str  # Geographic region
                }
        
        Returns:
            List of Starlink satellites with their current orbital parameters
            
        Raises:
            Exception: If the API request fails
        """
        endpoint = f"{self.base_url}/api/v1/constellation/data"
        
        try:
            response = self.session.get(endpoint, params=filters or {})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve constellation data: {str(e)}")
    
    def get_screening_status(self, submission_id: str) -> Dict[str, Any]:
        """
        Get the status of a previous ephemeris submission or screening request.
        
        Args:
            submission_id: ID returned from a previous submission
        
        Returns:
            Status information for the submission
            {
                "submission_id": str,
                "status": str,  # pending, processing, completed, failed
                "results": {...},  # Available when status is completed
                "timestamp": str
            }
            
        Raises:
            Exception: If the API request fails
        """
        endpoint = f"{self.base_url}/api/v1/status/{submission_id}"
        
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get screening status: {str(e)}")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
