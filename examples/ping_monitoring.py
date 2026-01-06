#!/usr/bin/env python3
"""
Network monitoring example

This example demonstrates how to monitor network metrics
including ping latency and other connectivity statistics.
"""
import sys
import os
import json
import time

# Add parent directory to path to import starlink_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlink_client import StarlinkClient

def display_ping_metrics(metrics):
    """Display ping metrics in a readable format"""
    if "error" in metrics:
        print(f"❌ Error retrieving ping metrics: {metrics['error']}")
        return
    
    print("✅ Ping Metrics Retrieved Successfully")
    print(json.dumps(metrics, indent=2))

def main():
    # Initialize the client
    client = StarlinkClient()
    
    print("Monitoring Network Metrics")
    print("=" * 60)
    
    # Get ping metrics
    print("\n📊 Retrieving ping metrics...")
    metrics = client.get_ping_metrics()
    display_ping_metrics(metrics)
    
    return metrics

def continuous_monitoring(interval=60):
    """Continuously monitor ping metrics at specified interval"""
    client = StarlinkClient()
    
    print(f"Starting continuous monitoring (interval: {interval}s)")
    print("Press Ctrl+C to stop...")
    print("=" * 60)
    
    try:
        while True:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{timestamp}]")
            metrics = client.get_ping_metrics()
            display_ping_metrics(metrics)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")

if __name__ == "__main__":
    # Run once
    main()
    
    # Uncomment to enable continuous monitoring
    # continuous_monitoring(interval=60)
