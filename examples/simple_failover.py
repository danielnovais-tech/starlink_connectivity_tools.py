"""
Simple Use Case: Demonstrating Connection Failover

This example shows the exact use case from the problem statement.
"""

import time
from starlink_connectivity_tools import FailoverHandler


def simulate_connection_failure():
    """
    Simulate a failing connection for demonstration.
    Returns False to indicate connection is down.
    """
    return False


def main():
    """Demonstrate the use case from the problem statement."""
    
    print("=" * 70)
    print("Connection Failover Use Case - Problem Statement Implementation")
    print("=" * 70)
    print()
    
    # Initialize failover handler with a health check that always fails
    failover_handler = FailoverHandler(
        failure_threshold=3,
        check_interval=1.0,
        health_check_callback=simulate_connection_failure
    )
    
    print("Monitoring connection status...")
    print(f"Initial state: {failover_handler.get_current_state().value}")
    print()
    
    # Run the monitoring loop
    for iteration in range(10):
        time.sleep(1.2)  # Wait slightly longer than check interval
        
        # This is the exact code from the problem statement:
        # Automatic failover when primary fails
        if failover_handler.should_failover():
            failover_handler.initiate_failover("Primary connection lost")
            print()
            print(">>> FAILOVER EXECUTED <<<")
            print(f">>> New state: {failover_handler.get_current_state().value}")
            print()
            break
        
        # Show progress
        print(f"Check {iteration + 1}: Failures = {failover_handler.get_failure_count()}/{failover_handler.failure_threshold}")
    
    print()
    print("Final state:", failover_handler.get_current_state().value)
    
    # Show failover history
    history = failover_handler.get_failover_history()
    if history:
        print("\nFailover Event Details:")
        event = history[0]
        print(f"  - Timestamp: {time.ctime(event['timestamp'])}")
        print(f"  - From: {event['from_state']}")
        print(f"  - To: {event['to_state']}")
        print(f"  - Reason: {event['reason']}")
        print(f"  - Failure count: {event['failure_count']}")


if __name__ == "__main__":
    main()
