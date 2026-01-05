#!/usr/bin/env python3
"""
Starlink Monitor CLI - NEW: Command-line monitoring tool

Command-line tool for real-time Starlink connection monitoring.
Provides live metrics, alerts, and diagnostic information.
"""

import sys
import time
import argparse
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.starlink_monitor import StarlinkMonitor
from src.diagnostics import Diagnostics
from src.config.settings import Settings

logging.basicConfig(
    level=getattr(logging, Settings.LOG_LEVEL),
    format=Settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)


def monitor_live(monitor: StarlinkMonitor, interval: int = 5) -> None:
    """
    Display live monitoring data.
    
    Args:
        monitor: StarlinkMonitor instance
        interval: Update interval in seconds
    """
    print("\n" + "="*60)
    print("Starlink Live Monitor")
    print("="*60)
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            metrics = monitor.get_current_metrics()
            alerts = monitor.check_alerts()
            
            # Clear screen (works on most terminals)
            print("\033[2J\033[H", end="")
            
            # Display header
            print("="*60)
            print(f"Starlink Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)
            
            # Display metrics
            print(f"\n📡 Signal Quality: {metrics['signal_quality']}%")
            print(f"🛰️  Satellites: {metrics['satellites_visible']}")
            print(f"⏱️  Latency: {metrics['latency_ms']:.1f} ms")
            print(f"⬇️  Download: {metrics['download_mbps']:.1f} Mbps")
            print(f"⬆️  Upload: {metrics['upload_mbps']:.1f} Mbps")
            print(f"📊 Packet Loss: {metrics['packet_loss_percent']:.2f}%")
            print(f"🚫 Obstruction: {metrics['obstruction_percent']:.2f}%")
            print(f"🌡️  Temperature: {metrics['dish_temperature_c']:.1f}°C")
            print(f"⏰ Uptime: {metrics['uptime_seconds'] / 3600:.1f} hours")
            
            # Display alerts
            if alerts:
                print("\n⚠️  ALERTS:")
                for alert in alerts:
                    severity_icon = "🔴" if alert["severity"] == "critical" else "🟡"
                    print(f"  {severity_icon} {alert['message']}")
            else:
                print("\n✅ No alerts - All systems normal")
            
            print("\n" + "="*60)
            print(f"Next update in {interval} seconds...")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")


def show_statistics(monitor: StarlinkMonitor, duration: int = 60) -> None:
    """
    Display statistics summary.
    
    Args:
        monitor: StarlinkMonitor instance
        duration: Duration in minutes
    """
    print("\n" + "="*60)
    print(f"Statistics (Last {duration} minutes)")
    print("="*60)
    
    stats = monitor.get_statistics(duration)
    
    if "error" in stats:
        print(f"\n{stats['error']}")
        return
    
    print(f"\nSamples: {stats['sample_count']}")
    
    print("\nLatency (ms):")
    print(f"  Average: {stats['latency']['avg']:.1f}")
    print(f"  Min: {stats['latency']['min']:.1f}")
    print(f"  Max: {stats['latency']['max']:.1f}")
    
    print("\nDownload Speed (Mbps):")
    print(f"  Average: {stats['download']['avg']:.1f}")
    print(f"  Min: {stats['download']['min']:.1f}")
    print(f"  Max: {stats['download']['max']:.1f}")
    
    print("\nUpload Speed (Mbps):")
    print(f"  Average: {stats['upload']['avg']:.1f}")
    print(f"  Min: {stats['upload']['min']:.1f}")
    print(f"  Max: {stats['upload']['max']:.1f}")
    
    print("\nSignal Quality (%):")
    print(f"  Average: {stats['signal_quality']['avg']:.1f}")
    print(f"  Min: {stats['signal_quality']['min']:.1f}")
    print(f"  Max: {stats['signal_quality']['max']:.1f}")
    
    print("\n" + "="*60)


def run_diagnostics(diagnostics: Diagnostics) -> None:
    """
    Run and display diagnostics.
    
    Args:
        diagnostics: Diagnostics instance
    """
    print("\n" + "="*60)
    print("Running Diagnostics...")
    print("="*60)
    
    report = diagnostics.get_diagnostic_report()
    print(report)
    
    steps = diagnostics.get_troubleshooting_steps()
    if steps:
        print("\n📋 Recommended Actions:")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Starlink Monitor CLI - Real-time monitoring tool"
    )
    
    parser.add_argument(
        "command",
        choices=["monitor", "stats", "diagnostics", "export"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Monitoring interval in seconds (default: 5)"
    )
    
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Duration for statistics in minutes (default: 60)"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Export format (default: json)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output file for export"
    )
    
    parser.add_argument(
        "--endpoint",
        type=str,
        default=Settings.STARLINK_ENDPOINT,
        help=f"Starlink endpoint (default: {Settings.STARLINK_ENDPOINT})"
    )
    
    args = parser.parse_args()
    
    # Initialize components
    monitor = StarlinkMonitor(starlink_endpoint=args.endpoint)
    diagnostics = Diagnostics(starlink_endpoint=args.endpoint)
    
    # Execute command
    if args.command == "monitor":
        monitor_live(monitor, args.interval)
    
    elif args.command == "stats":
        # Collect some samples first
        print("Collecting metrics...")
        for _ in range(5):
            monitor.get_current_metrics()
            time.sleep(1)
        show_statistics(monitor, args.duration)
    
    elif args.command == "diagnostics":
        run_diagnostics(diagnostics)
    
    elif args.command == "export":
        # Collect samples
        print("Collecting metrics for export...")
        for _ in range(10):
            monitor.get_current_metrics()
            time.sleep(1)
        
        data = monitor.export_metrics(args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(data)
            print(f"Metrics exported to {args.output}")
        else:
            print(data)


if __name__ == "__main__":
    main()
