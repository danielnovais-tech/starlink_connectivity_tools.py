#!/usr/bin/env python3
"""
Starlink Monitor CLI Tool
Command-line interface for monitoring and managing Starlink connectivity
"""

import argparse
import sys
import os
import time
import json
from datetime import datetime
from typing import Dict, List

# Ensure proper import path when running as a script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.starlink_monitor import StarlinkMonitor
from src.connection_manager import SatelliteConnectionManager


class StarlinkCLI:
    """Command-line interface for Starlink monitoring"""
    
    def __init__(self, host: str = "192.168.100.1"):
        self.monitor = StarlinkMonitor(host=host)
        self.connection_manager = SatelliteConnectionManager(
            enable_starlink=True,
            starlink_host=host
        )
        
        # Color codes for terminal output
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'reset': '\033[0m',
            'bold': '\033[1m'
        }
    
    def colorize(self, text: str, color: str) -> str:
        """Add color to text for terminal output"""
        if color in self.colors:
            return f"{self.colors[color]}{text}{self.colors['reset']}"
        return text
    
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "="*60)
        print(f"{self.colors['bold']}{title}{self.colors['reset']}")
        print("="*60)
    
    def print_status(self, detailed: bool = False):
        """Print current Starlink status"""
        metrics = self.monitor.get_metrics()
        
        if not metrics:
            print(self.colorize("❌ Failed to get Starlink metrics", 'red'))
            return
        
        self.print_header("STARLINK STATUS")
        
        # Basic status
        status_color = 'green' if metrics.status == 'online' else 'red'
        print(f"Status: {self.colorize(metrics.status.upper(), status_color)}")
        print(f"Connected Satellites: {metrics.satellites_connected}")
        print(f"Obstruction: {metrics.obstruction_percent:.1f}%")
        
        # Network metrics
        print(f"\n{self.colors['bold']}Network Performance:{self.colors['reset']}")
        print(f"  Download: {self.colorize(f'{metrics.download_speed:.1f} Mbps', 'cyan')}")
        print(f"  Upload: {self.colorize(f'{metrics.upload_speed:.1f} Mbps', 'cyan')}")
        print(f"  Latency: {self.colorize(f'{metrics.latency:.1f} ms', 'cyan')}")
        print(f"  Packet Loss: {metrics.packet_loss:.1f}%")
        
        # Signal quality
        print(f"\n{self.colors['bold']}Signal Quality:{self.colors['reset']}")
        print(f"  Strength: {metrics.signal_strength:.1f} dBm")
        print(f"  SNR: {metrics.snr:.1f} dB")
        print(f"  Azimuth: {metrics.azimuth:.1f}°")
        print(f"  Elevation: {metrics.elevation:.1f}°")
        
        # Device info
        print(f"\n{self.colors['bold']}Device Info:{self.colors['reset']}")
        print(f"  Dish Power: {metrics.dish_power_usage:.1f} W")
        print(f"  Dish Temp: {metrics.dish_temp:.1f}°C")
        print(f"  Router Temp: {metrics.router_temp:.1f}°C")
        print(f"  Boot Count: {metrics.boot_count}")
        
        # Check thresholds
        self._check_and_print_thresholds(metrics)
        
        # Print timestamp
        timestamp = datetime.fromtimestamp(metrics.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print(f"\nLast Updated: {timestamp}")
    
    def _check_and_print_thresholds(self, metrics):
        """Check metrics against thresholds and print warnings"""
        issues = []
        
        if metrics.download_speed < self.monitor.thresholds['min_download_speed']:
            issues.append(f"Low download speed ({metrics.download_speed:.1f} Mbps)")
        
        if metrics.latency > self.monitor.thresholds['max_latency']:
            issues.append(f"High latency ({metrics.latency:.1f} ms)")
        
        if metrics.packet_loss > self.monitor.thresholds['max_packet_loss']:
            issues.append(f"High packet loss ({metrics.packet_loss:.1f}%)")
        
        if metrics.obstruction_percent > self.monitor.thresholds['max_obstruction']:
            issues.append(f"High obstruction ({metrics.obstruction_percent:.1f}%)")
        
        if issues:
            print(f"\n{self.colorize('⚠️  Issues Detected:', 'yellow')}")
            for issue in issues:
                print(f"  • {issue}")
    
    def print_performance_report(self, hours: int = 24):
        """Print performance report"""
        report = self.monitor.get_performance_report(hours=hours)
        
        self.print_header(f"PERFORMANCE REPORT (Last {hours} hours)")
        
        if report['status'] == 'no_data':
            print("No data available for the specified period")
            return
        
        print(f"Samples: {report['samples']}")
        print(f"Availability: {report['availability_percent']:.1f}%")
        print(f"Issues Detected: {report['issues_count']}")
        print(f"Active Alerts: {report['active_alerts']}")
        
        print(f"\n{self.colors['bold']}Averages:{self.colors['reset']}")
        print(f"  Download: {report['averages']['download_speed']:.1f} Mbps")
        print(f"  Upload: {report['averages']['upload_speed']:.1f} Mbps")
        print(f"  Latency: {report['averages']['latency']:.1f} ms")
        
        print(f"\n{self.colors['bold']}Current:{self.colors['reset']}")
        print(f"  Status: {report['current_status']}")
        print(f"  Download: {report['current_download']:.1f} Mbps")
        print(f"  Latency: {report['current_latency']:.1f} ms")
    
    def print_connection_manager_status(self):
        """Print connection manager status"""
        self.connection_manager.scan_available_connections()
        
        if self.monitor.initialized:
            # Try to connect to Starlink
            success = self.connection_manager.connect("starlink_satellite")
            
            if success:
                report = self.connection_manager.get_connection_report()
                
                self.print_header("CONNECTION MANAGER STATUS")
                
                print(f"Active Connection: {report['active_connection']}")
                print(f"Crisis Mode: {report['crisis_mode']}")
                print(f"Connection Score: {report.get('connection_score', 0):.2f}/1.0")
                
                if 'current_metrics' in report:
                    metrics = report['current_metrics']
                    print(f"\nCurrent Metrics:")
                    print(f"  Download: {metrics['bandwidth_down']:.1f} Mbps")
                    print(f"  Upload: {metrics['bandwidth_up']:.1f} Mbps")
                    print(f"  Latency: {metrics['latency']:.1f} ms")
                    print(f"  Signal: {metrics['signal_strength']:.1f} dBm")
            
            self.connection_manager.disconnect()
    
    def start_monitoring(self, interval: int = 60, duration: int = None):
        """Start continuous monitoring"""
        print(f"Starting continuous monitoring (interval: {interval}s)...")
        print("Press Ctrl+C to stop\n")
        
        self.monitor.start_monitoring(interval=interval)
        
        try:
            start_time = time.time()
            while True:
                if duration and (time.time() - start_time) > duration:
                    print(f"\nMonitoring duration ({duration}s) completed.")
                    break
                
                # Print status every interval
                time.sleep(interval)
                self.print_status(detailed=False)
                print()  # Blank line
                
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user.")
        finally:
            self.monitor.stop_monitoring()
    
    def reboot_dish(self):
        """Reboot Starlink dish with confirmation"""
        print(self.colorize("⚠️  WARNING: This will reboot your Starlink dish!", 'yellow'))
        print("The dish will be offline for approximately 5-10 minutes.")
        
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            print("Rebooting dish...")
            success = self.monitor.reboot_dish()
            
            if success:
                print(self.colorize("✓ Reboot command sent successfully", 'green'))
                print("Dish will restart and reconnect automatically.")
            else:
                print(self.colorize("✗ Failed to send reboot command", 'red'))
        else:
            print("Reboot cancelled.")
    
    def export_data(self, filename: str, hours: int = 24):
        """Export monitoring data to JSON file"""
        report = self.monitor.get_performance_report(hours=hours)
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Data exported to {filename}")
    
    def set_thresholds_interactive(self):
        """Interactively set monitoring thresholds"""
        print("\nCurrent Thresholds:")
        for key, value in self.monitor.thresholds.items():
            print(f"  {key}: {value}")
        
        print("\nEnter new threshold values (press Enter to keep current):")
        
        new_thresholds = {}
        for key, current in self.monitor.thresholds.items():
            value = input(f"{key} [{current}]: ").strip()
            if value:
                try:
                    new_thresholds[key] = float(value)
                except ValueError:
                    print(f"Invalid value for {key}, keeping current value")
        
        if new_thresholds:
            self.monitor.set_thresholds(**new_thresholds)
            print("Thresholds updated successfully.")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Starlink Connectivity Monitor CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status                    # Show current status
  %(prog)s monitor --interval 30     # Monitor every 30 seconds
  %(prog)s report --hours 48         # 48-hour performance report
  %(prog)s reboot                    # Reboot Starlink dish
  %(prog)s thresholds                # Set monitoring thresholds
        """
    )
    
    parser.add_argument(
        'command',
        choices=['status', 'monitor', 'report', 'reboot', 
                'thresholds', 'export', 'connection'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--host',
        default='192.168.100.1',
        help='Starlink router IP address'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Monitoring interval in seconds (for monitor command)'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        help='Monitoring duration in seconds (for monitor command)'
    )
    
    parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Hours of data for report/export commands'
    )
    
    parser.add_argument(
        '--output',
        default='starlink_data.json',
        help='Output file for export command'
    )
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = StarlinkCLI(host=args.host)
    
    # Execute command
    try:
        if args.command == 'status':
            cli.print_status(detailed=True)
        
        elif args.command == 'monitor':
            cli.start_monitoring(interval=args.interval, duration=args.duration)
        
        elif args.command == 'report':
            cli.print_performance_report(hours=args.hours)
        
        elif args.command == 'reboot':
            cli.reboot_dish()
        
        elif args.command == 'thresholds':
            cli.set_thresholds_interactive()
        
        elif args.command == 'export':
            cli.export_data(filename=args.output, hours=args.hours)
        
        elif args.command == 'connection':
            cli.print_connection_manager_status()
        
        print()  # Final newline
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n{cli.colorize('Error:', 'red')} {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
