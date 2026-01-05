"""
Use Case: Medical Emergency Communications

This example demonstrates how to use the Starlink Connectivity Tools
to prioritize medical data transmission during emergency situations.

Medical evacuation and emergency response scenarios often require reliable,
high-bandwidth connections for transmitting critical patient data, telemedicine
consultations, and real-time monitoring information.
"""

import sys
import os

# Add parent directory to path to import starlink_connectivity
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from starlink_connectivity import BandwidthOptimizer


def medical_emergency_example():
    """
    Example: Prioritizing medical data transmission during an emergency evacuation.
    
    Scenario: A remote medical evacuation is in progress, requiring bandwidth
    for transmitting patient vital signs, medical imaging, and telemedicine
    consultation.
    """
    print("=" * 70)
    print("Medical Emergency Communications - Use Case Example")
    print("=" * 70)
    print()
    
    # Initialize the bandwidth optimizer with available Starlink bandwidth
    optimizer = BandwidthOptimizer(total_bandwidth=100.0)  # 100 Mbps available
    print(f"Initialized {optimizer}")
    print()
    
    # Prioritize medical data transmission
    print("Allocating bandwidth for medical emergency evacuation...")
    medical_allocation = optimizer.allocate_bandwidth(
        connection_id="medical_evac",
        destination="medical.data",
        requested_bandwidth=10.0
    )
    
    print(f"✓ Medical Allocation: {medical_allocation}")
    print(f"  Status: {medical_allocation.status}")
    print(f"  Allocated: {medical_allocation.allocated_bandwidth} Mbps")
    print()
    
    # Show remaining bandwidth
    print(f"Remaining available bandwidth: {optimizer.get_available_bandwidth()} Mbps")
    print()
    
    # Additional medical connections
    print("Allocating additional medical services...")
    
    # Telemedicine video consultation
    telemedicine_allocation = optimizer.allocate_bandwidth(
        connection_id="telemedicine_consult",
        destination="hospital.remote.video",
        requested_bandwidth=5.0,
        priority=5
    )
    print(f"✓ Telemedicine: {telemedicine_allocation.allocated_bandwidth} Mbps allocated")
    
    # Patient monitoring data
    monitoring_allocation = optimizer.allocate_bandwidth(
        connection_id="patient_monitoring",
        destination="monitoring.stream",
        requested_bandwidth=2.0,
        priority=5
    )
    print(f"✓ Patient Monitoring: {monitoring_allocation.allocated_bandwidth} Mbps allocated")
    
    # Medical imaging transfer
    imaging_allocation = optimizer.allocate_bandwidth(
        connection_id="medical_imaging",
        destination="radiology.upload",
        requested_bandwidth=15.0,
        priority=4
    )
    print(f"✓ Medical Imaging: {imaging_allocation.allocated_bandwidth} Mbps allocated")
    print()
    
    # Show all allocations
    print("Current Bandwidth Allocations:")
    print("-" * 70)
    all_allocations = optimizer.get_all_allocations()
    for conn_id, allocation in all_allocations.items():
        print(f"  {conn_id:25} | {allocation.allocated_bandwidth:6.1f} Mbps | Priority: {allocation.priority}")
    print("-" * 70)
    print(f"Total Allocated: {sum(a.allocated_bandwidth for a in all_allocations.values()):.1f} Mbps")
    print(f"Available: {optimizer.get_available_bandwidth():.1f} Mbps")
    print()
    
    # Demonstrate connection release
    print("Emergency complete - releasing medical evacuation bandwidth...")
    optimizer.release_bandwidth("medical_evac")
    print(f"✓ Released medical_evac connection")
    print(f"  Available bandwidth now: {optimizer.get_available_bandwidth()} Mbps")
    print()
    
    print("=" * 70)
    print("Medical emergency communications example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    medical_emergency_example()
