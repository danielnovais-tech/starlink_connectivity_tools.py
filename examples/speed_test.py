#!/usr/bin/env python3
"""
Speed test example

This example demonstrates how to run speed tests and
retrieve speed test results.
"""
import sys
import os
import json

# Add parent directory to path to import starlink_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlink_client import StarlinkClient

def main():
    # Initialize the client
    client = StarlinkClient()
    
    print("Starlink Speed Test")
    print("=" * 60)
    
    # Get the last speed test results
    print("\n📥 Retrieving last speed test results...")
    last_results = client.get_speed_test()
    
    if "error" in last_results:
        print(f"No previous speed test results: {last_results['error']}")
    else:
        print("Last Speed Test Results:")
        print(json.dumps(last_results, indent=2))
    
    # Run a new speed test
    print("\n🚀 Running new speed test...")
    print("This may take 20-30 seconds...")
    
    new_results = client.run_speed_test()
    
    if "error" in new_results:
        print(f"❌ Speed test failed: {new_results['error']}")
    else:
        print("\n✅ Speed Test Complete!")
        print(json.dumps(new_results, indent=2))
    
    return new_results

if __name__ == "__main__":
    result = main()
