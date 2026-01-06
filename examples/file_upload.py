#!/usr/bin/env python3
"""
Example demonstrating how to upload ephemeris files and monitor their
processing status.
"""

from starlink_connectivity_tools import SpaceSafetyAPI
import os
import time


def main():
    api_key = os.getenv('STARLINK_API_KEY')
    
    # Use context manager for automatic cleanup
    with SpaceSafetyAPI(api_key=api_key) as api:
        print("=== Ephemeris File Upload Example ===\n")
        
        # Example file path (you would replace this with your actual file)
        file_path = "/path/to/your/ephemeris.oem"
        
        # Check if the file exists (for demonstration)
        if not os.path.exists(file_path):
            print(f"Note: Example file '{file_path}' does not exist.")
            print("In production, you would provide a valid OEM or TLE file.\n")
            
            # Create a demonstration with the submit_ephemeris method instead
            print("Using direct ephemeris submission as demonstration...")
            ephemeris_data = {
                "satellite_id": "DEMO-SAT-002",
                "epoch": "2026-01-05T18:30:00Z",
                "state_vector": {
                    "position": [6800.0, 1000.0, 500.0],
                    "velocity": [0.5, 7.4, 0.2]
                },
                "covariance_matrix": [
                    [1e-6, 0, 0, 0, 0, 0],
                    [0, 1e-6, 0, 0, 0, 0],
                    [0, 0, 1e-6, 0, 0, 0],
                    [0, 0, 0, 1e-9, 0, 0],
                    [0, 0, 0, 0, 1e-9, 0],
                    [0, 0, 0, 0, 0, 1e-9]
                ]
            }
            
            try:
                response = api.submit_ephemeris(ephemeris_data)
                submission_id = response.get('submission_id')
                print(f"✓ Ephemeris submitted")
                print(f"  Submission ID: {submission_id}\n")
                
                # Monitor the processing status
                print("Monitoring processing status...")
                for attempt in range(5):
                    time.sleep(2)  # Wait 2 seconds between checks
                    
                    try:
                        status = api.get_screening_status(submission_id)
                        current_status = status.get('status', 'unknown')
                        print(f"  Attempt {attempt + 1}: Status = {current_status}")
                        
                        if current_status == 'completed':
                            print("\n✓ Processing completed!")
                            results = status.get('results', {})
                            print(f"  Results: {results}")
                            break
                        elif current_status == 'failed':
                            print("\n✗ Processing failed")
                            print(f"  Error: {status.get('error', 'Unknown error')}")
                            break
                    except Exception as e:
                        print(f"  Error checking status: {e}")
                        break
                else:
                    print("\n⧗ Processing still in progress after monitoring period")
                    
            except Exception as e:
                print(f"✗ Error: {e}")
        else:
            # If the file actually exists, upload it
            print(f"Uploading ephemeris file: {file_path}")
            try:
                result = api.submit_ephemeris_file(
                    file_path=file_path,
                    file_format="oem"
                )
                print(f"✓ File uploaded successfully")
                print(f"  Submission ID: {result.get('submission_id')}")
            except Exception as e:
                print(f"✗ Upload failed: {e}")


if __name__ == "__main__":
    main()
