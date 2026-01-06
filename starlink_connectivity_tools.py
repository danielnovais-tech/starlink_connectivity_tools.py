"""
Starlink Connectivity Tools

A Python library for monitoring and analyzing Starlink satellite internet connectivity.
Provides utilities for checking connection status, measuring performance metrics,
and analyzing network availability.
"""

import time
import random
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConnectivityMetrics:
    """Represents connectivity metrics for a Starlink connection."""
    timestamp: datetime
    is_connected: bool
    latency_ms: Optional[float] = None
    download_speed_mbps: Optional[float] = None
    upload_speed_mbps: Optional[float] = None
    packet_loss_percent: Optional[float] = None
    satellite_id: Optional[str] = None
    signal_strength: Optional[float] = None


class StarlinkConnectivity:
    """Main class for monitoring Starlink connectivity."""
    
    def __init__(self, location: str = "Unknown"):
        """
        Initialize the Starlink connectivity monitor.
        
        Args:
            location: Geographic location identifier
        """
        self.location = location
        self.metrics_history: List[ConnectivityMetrics] = []
    
    def check_connection(self) -> ConnectivityMetrics:
        """
        Check the current Starlink connection status.
        
        Returns:
            ConnectivityMetrics object with current connection data
        """
        # Simulate connectivity check
        # In a real implementation, this would interface with Starlink hardware/API
        is_connected = random.random() > 0.1  # 90% connectivity rate
        
        metrics = ConnectivityMetrics(
            timestamp=datetime.now(),
            is_connected=is_connected,
            latency_ms=random.uniform(20, 60) if is_connected else None,
            download_speed_mbps=random.uniform(50, 200) if is_connected else None,
            upload_speed_mbps=random.uniform(10, 40) if is_connected else None,
            packet_loss_percent=random.uniform(0, 5) if is_connected else None,
            satellite_id=f"SAT-{random.randint(1000, 9999)}" if is_connected else None,
            signal_strength=random.uniform(60, 100) if is_connected else None
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def monitor_connection(self, duration_seconds: int = 60, interval_seconds: int = 5) -> List[ConnectivityMetrics]:
        """
        Monitor connection over a period of time.
        
        Args:
            duration_seconds: Total monitoring duration
            interval_seconds: Time between checks
            
        Returns:
            List of ConnectivityMetrics collected during monitoring
        """
        print(f"Starting connection monitoring for {duration_seconds} seconds...")
        print(f"Location: {self.location}")
        print("-" * 80)
        
        results = []
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            metrics = self.check_connection()
            results.append(metrics)
            
            status = "CONNECTED" if metrics.is_connected else "DISCONNECTED"
            print(f"[{metrics.timestamp.strftime('%H:%M:%S')}] Status: {status}")
            
            if metrics.is_connected:
                if metrics.latency_ms is not None:
                    print(f"  Latency: {metrics.latency_ms:.1f}ms")
                if metrics.download_speed_mbps is not None:
                    print(f"  Download: {metrics.download_speed_mbps:.1f} Mbps")
                if metrics.upload_speed_mbps is not None:
                    print(f"  Upload: {metrics.upload_speed_mbps:.1f} Mbps")
                if metrics.packet_loss_percent is not None:
                    print(f"  Packet Loss: {metrics.packet_loss_percent:.2f}%")
                if metrics.signal_strength is not None:
                    print(f"  Signal Strength: {metrics.signal_strength:.1f}%")
                if metrics.satellite_id is not None:
                    print(f"  Satellite: {metrics.satellite_id}")
            
            print("-" * 80)
            time.sleep(interval_seconds)
        
        return results
    
    def get_statistics(self) -> Dict:
        """
        Calculate statistics from collected metrics.
        
        Returns:
            Dictionary containing statistical summary
        """
        if not self.metrics_history:
            return {"error": "No metrics collected"}
        
        connected_metrics = [m for m in self.metrics_history if m.is_connected]
        total_checks = len(self.metrics_history)
        connected_checks = len(connected_metrics)
        
        stats = {
            "location": self.location,
            "total_checks": total_checks,
            "connected_checks": connected_checks,
            "connectivity_rate": (connected_checks / total_checks * 100) if total_checks > 0 else 0,
        }
        
        if connected_metrics:
            latencies = [m.latency_ms for m in connected_metrics if m.latency_ms is not None]
            download_speeds = [m.download_speed_mbps for m in connected_metrics if m.download_speed_mbps is not None]
            upload_speeds = [m.upload_speed_mbps for m in connected_metrics if m.upload_speed_mbps is not None]
            packet_losses = [m.packet_loss_percent for m in connected_metrics if m.packet_loss_percent is not None]
            
            if latencies:
                stats["avg_latency_ms"] = sum(latencies) / len(latencies)
                stats["min_latency_ms"] = min(latencies)
                stats["max_latency_ms"] = max(latencies)
            
            if download_speeds:
                stats["avg_download_mbps"] = sum(download_speeds) / len(download_speeds)
                stats["min_download_mbps"] = min(download_speeds)
                stats["max_download_mbps"] = max(download_speeds)
            
            if upload_speeds:
                stats["avg_upload_mbps"] = sum(upload_speeds) / len(upload_speeds)
                stats["min_upload_mbps"] = min(upload_speeds)
                stats["max_upload_mbps"] = max(upload_speeds)
            
            if packet_losses:
                stats["avg_packet_loss_percent"] = sum(packet_losses) / len(packet_losses)
        
        return stats
    
    def print_statistics(self):
        """Print formatted statistics summary."""
        stats = self.get_statistics()
        
        if "error" in stats:
            print(stats["error"])
            return
        
        print("\n" + "=" * 80)
        print("CONNECTIVITY STATISTICS")
        print("=" * 80)
        print(f"Location: {stats['location']}")
        print(f"Total Checks: {stats['total_checks']}")
        print(f"Connected Checks: {stats['connected_checks']}")
        print(f"Connectivity Rate: {stats['connectivity_rate']:.2f}%")
        
        if "avg_latency_ms" in stats:
            print(f"\nLatency:")
            print(f"  Average: {stats['avg_latency_ms']:.2f}ms")
            print(f"  Min: {stats['min_latency_ms']:.2f}ms")
            print(f"  Max: {stats['max_latency_ms']:.2f}ms")
        
        if "avg_download_mbps" in stats:
            print(f"\nDownload Speed:")
            print(f"  Average: {stats['avg_download_mbps']:.2f} Mbps")
            print(f"  Min: {stats['min_download_mbps']:.2f} Mbps")
            print(f"  Max: {stats['max_download_mbps']:.2f} Mbps")
        
        if "avg_upload_mbps" in stats:
            print(f"\nUpload Speed:")
            print(f"  Average: {stats['avg_upload_mbps']:.2f} Mbps")
            print(f"  Min: {stats['min_upload_mbps']:.2f} Mbps")
            print(f"  Max: {stats['max_upload_mbps']:.2f} Mbps")
        
        if "avg_packet_loss_percent" in stats:
            print(f"\nPacket Loss:")
            print(f"  Average: {stats['avg_packet_loss_percent']:.2f}%")
        
        print("=" * 80)


def check_availability(location: str) -> bool:
    """
    Check if Starlink service is available in a given location.
    
    Args:
        location: Geographic location to check
        
    Returns:
        True if service is available, False otherwise
    """
    # Simplified simulation - in reality would check against Starlink coverage map
    print(f"Checking Starlink availability for: {location}")
    available = random.random() > 0.3  # 70% chance of availability
    
    if available:
        print(f"✓ Starlink service is available in {location}")
    else:
        print(f"✗ Starlink service is not yet available in {location}")
    
    return available
