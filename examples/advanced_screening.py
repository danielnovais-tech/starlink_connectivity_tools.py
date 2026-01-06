#!/usr/bin/env python3
"""
Advanced example showing conjunction screening with custom time windows
and detailed analysis of results.
"""

from starlink_connectivity_tools import SpaceSafetyAPI
from datetime import datetime, timedelta
import os


def format_time_window(days_ahead=7):
    """Create a time window for conjunction screening."""
    start = datetime.utcnow()
    end = start + timedelta(days=days_ahead)
    
    return {
        "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%SZ")
    }


def analyze_conjunction_risk(conjunction):
    """Analyze the risk level of a conjunction event."""
    miss_distance = conjunction.get('miss_distance', float('inf'))
    poc = conjunction.get('probability_of_collision', 0.0)
    
    if poc > 1e-4 or miss_distance < 1.0:
        return "HIGH"
    elif poc > 1e-5 or miss_distance < 5.0:
        return "MEDIUM"
    else:
        return "LOW"


def main():
    api_key = os.getenv('STARLINK_API_KEY')
    
    with SpaceSafetyAPI(api_key=api_key) as api:
        print("=== Advanced Conjunction Screening Example ===\n")
        
        satellite_id = "ADVANCED-SAT-003"
        
        # Define a 7-day screening window
        time_window = format_time_window(days_ahead=7)
        print(f"Screening period:")
        print(f"  Start: {time_window['start']}")
        print(f"  End:   {time_window['end']}\n")
        
        try:
            # Perform conjunction screening
            results = api.screen_conjunction(
                satellite_id=satellite_id,
                time_window=time_window
            )
            
            total_events = results.get('total_events', 0)
            conjunctions = results.get('conjunctions', [])
            
            print(f"✓ Screening completed for {satellite_id}")
            print(f"  Total events detected: {total_events}\n")
            
            if total_events > 0:
                # Categorize events by risk level
                high_risk = []
                medium_risk = []
                low_risk = []
                
                for conj in conjunctions:
                    risk = analyze_conjunction_risk(conj)
                    if risk == "HIGH":
                        high_risk.append(conj)
                    elif risk == "MEDIUM":
                        medium_risk.append(conj)
                    else:
                        low_risk.append(conj)
                
                print("Risk Summary:")
                print(f"  HIGH risk events:   {len(high_risk)}")
                print(f"  MEDIUM risk events: {len(medium_risk)}")
                print(f"  LOW risk events:    {len(low_risk)}\n")
                
                # Display high risk events in detail
                if high_risk:
                    print("⚠ HIGH RISK CONJUNCTIONS - IMMEDIATE ATTENTION REQUIRED:")
                    for i, conj in enumerate(high_risk, 1):
                        print(f"\n  Event {i}:")
                        print(f"    Starlink Satellite: {conj.get('starlink_satellite_id')}")
                        print(f"    Time of Closest Approach: {conj.get('time_of_closest_approach')}")
                        print(f"    Miss Distance: {conj.get('miss_distance'):.3f} km")
                        print(f"    Probability of Collision: {conj.get('probability_of_collision'):.2e}")
                        if conj.get('screening_volume_entered'):
                            print(f"    ⚠ SCREENING VOLUME ENTERED")
                
                # Display medium risk events
                if medium_risk:
                    print("\n⚡ MEDIUM RISK CONJUNCTIONS - MONITORING RECOMMENDED:")
                    for i, conj in enumerate(medium_risk[:3], 1):  # Show top 3
                        print(f"\n  Event {i}:")
                        print(f"    Starlink Satellite: {conj.get('starlink_satellite_id')}")
                        print(f"    TCA: {conj.get('time_of_closest_approach')}")
                        print(f"    Miss Distance: {conj.get('miss_distance'):.3f} km")
                    
                    if len(medium_risk) > 3:
                        print(f"\n  ... and {len(medium_risk) - 3} more medium risk events")
                
                print(f"\n✓ Analysis complete")
            else:
                print("✓ No conjunction events detected in the specified time window")
                
        except Exception as e:
            print(f"✗ Error during conjunction screening: {e}")


if __name__ == "__main__":
    main()
