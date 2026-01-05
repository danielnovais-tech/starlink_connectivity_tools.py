"""
Use Case: Automatic Connection Failover

This example demonstrates how to use the FailoverHandler to automatically
switch to a backup connection when the primary connection fails.
"""

import time
import random
from starlink_connectivity_tools import FailoverHandler


# Simulated connection health check
# In a real scenario, this would check actual Starlink connection status
def check_starlink_health() -> bool:
    """
    Simulate checking Starlink connection health.
    
    Returns:
        bool: True if connection is healthy, False if failed
    """
    # Simulate random connection failures for demonstration
    # In production, this would perform actual health checks like:
    # - Ping test to known servers
    # - DNS resolution test
    # - HTTP request to reliable endpoint
    # - Check Starlink dish status via API
    
    return random.random() > 0.3  # 30% failure rate for demo


def main():
    """Demonstrate automatic failover when primary connection fails."""
    
    print("=" * 60)
    print("Starlink Connection Failover - Use Case Example")
    print("=" * 60)
    print()
    
    # Initialize failover handler
    # - failure_threshold: Failover after 3 consecutive failures
    # - check_interval: Check connection every 2 seconds
    # - health_check_callback: Function to verify connection health
    failover_handler = FailoverHandler(
        failure_threshold=3,
        check_interval=2.0,
        health_check_callback=check_starlink_health
    )
    
    print(f"Initial state: {failover_handler.get_current_state().value}")
    print(f"Configuration:")
    print(f"  - Failure threshold: {failover_handler.failure_threshold}")
    print(f"  - Check interval: {failover_handler.check_interval}s")
    print()
    
    # Monitor connection and handle failover
    print("Monitoring connection... (Press Ctrl+C to stop)")
    print()
    
    iteration = 0
    max_iterations = 20  # Run for limited time in this example
    
    try:
        while iteration < max_iterations:
            iteration += 1
            
            # Automatic failover when primary fails
            if failover_handler.should_failover():
                failover_handler.initiate_failover("Primary connection lost")
                print()
                print(f">>> FAILOVER COMPLETED <<<")
                print(f">>> Current state: {failover_handler.get_current_state().value}")
                print()
                
                # In a real application, you would:
                # 1. Switch network routes to backup connection
                # 2. Update DNS settings
                # 3. Notify monitoring systems
                # 4. Log the event for analysis
            
            # Display current status
            current_state = failover_handler.get_current_state()
            failure_count = failover_handler.get_failure_count()
            
            status = f"[{iteration:02d}] State: {current_state.value:8s} | "
            status += f"Failures: {failure_count}/{failover_handler.failure_threshold}"
            
            if current_state.value == "backup":
                status += " [USING BACKUP]"
            
            print(status)
            
            # Wait before next check
            time.sleep(2.5)
    
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    
    # Display failover history
    print()
    print("=" * 60)
    print("Failover History:")
    print("=" * 60)
    
    history = failover_handler.get_failover_history()
    if history:
        for idx, event in enumerate(history, 1):
            print(f"\nEvent {idx}:")
            print(f"  Time: {time.ctime(event['timestamp'])}")
            print(f"  Transition: {event['from_state']} -> {event['to_state']}")
            print(f"  Reason: {event['reason']}")
            print(f"  Failure count at time: {event['failure_count']}")
    else:
        print("\nNo failover events occurred during this run")
    
    print()


if __name__ == "__main__":
    main()
