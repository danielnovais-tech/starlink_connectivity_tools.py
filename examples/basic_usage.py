#!/usr/bin/env python3
"""
Basic example demonstrating how to use the Starlink Space Safety API
to submit ephemeris data and screen for conjunctions.
"""

from starlink_connectivity_tools import SpaceSafetyAPI
import os


def main():
    # Get API key from environment variable or use None for unauthenticated requests
    api_key = os.getenv('STARLINK_API_KEY')
    
    # Initialize the API client
    print("Initializing Starlink Space Safety API client...")
    api = SpaceSafetyAPI(api_key=api_key)
    
    # Example 1: Submit ephemeris data
    print("\n=== Example 1: Submitting Ephemeris Data ===")
    ephemeris_data = {
        "satellite_id": "EXAMPLE-SAT-001",
        "epoch": "2026-01-05T12:00:00Z",
        "state_vector": {
            "position": [7000.0, 0.0, 0.0],  # km - circular orbit at ~620 km altitude
            "velocity": [0.0, 7.546, 0.0]    # km/s
        },
        "metadata": {
            "operator": "Example Space Agency",
            "mass": 500.0,  # kg
            "cross_sectional_area": 10.0  # m^2
        }
    }
    
    try:
        response = api.submit_ephemeris(ephemeris_data)
        print(f"✓ Ephemeris submitted successfully")
        print(f"  Submission ID: {response.get('submission_id', 'N/A')}")
    except Exception as e:
        print(f"✗ Error submitting ephemeris: {e}")
    
    # Example 2: Screen for conjunctions
    print("\n=== Example 2: Screening for Conjunctions ===")
    try:
        results = api.screen_conjunction("EXAMPLE-SAT-001")
        total_events = results.get('total_events', 0)
        print(f"✓ Screening completed")
        print(f"  Total potential conjunctions found: {total_events}")
        
        if total_events > 0:
            conjunctions = results.get('conjunctions', [])
            print(f"\n  Top 5 closest approaches:")
            for i, conj in enumerate(conjunctions[:5], 1):
                print(f"    {i}. Starlink satellite: {conj.get('starlink_satellite_id')}")
                print(f"       TCA: {conj.get('time_of_closest_approach')}")
                print(f"       Miss distance: {conj.get('miss_distance', 'N/A')} km")
                print(f"       PoC: {conj.get('probability_of_collision', 'N/A')}")
    except Exception as e:
        print(f"✗ Error screening for conjunctions: {e}")
    
    # Example 3: Get constellation data
    print("\n=== Example 3: Retrieving Constellation Data ===")
    try:
        constellation = api.get_starlink_constellation_data(
            filters={"active_only": True}
        )
        print(f"✓ Constellation data retrieved")
        print(f"  Total active Starlink satellites: {len(constellation)}")
    except Exception as e:
        print(f"✗ Error retrieving constellation data: {e}")
    
    # Clean up
    api.close()
    print("\n✓ Session closed")


if __name__ == "__main__":
    main()
