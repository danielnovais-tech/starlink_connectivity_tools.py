#!/usr/bin/env python3
"""
Starlink Monitor CLI Tool
Command-line interface for monitoring and managing Starlink connectivity

This tool provides comprehensive monitoring and management capabilities for
Starlink satellite internet connections including:
- Real-time status monitoring
- Performance reports and analytics
- Connection management
- Threshold-based alerting
- Data export (JSON, CSV)
- Interactive configuration

Examples:
    Check current status:
        $ starlink-cli status
    
    Monitor with custom interval:
        $ starlink-cli monitor --interval 30
    
    Generate 48-hour performance report:
        $ starlink-cli report --hours 48
    
    Export data to CSV:
        $ starlink-cli export --output data.csv --format csv
    
    Enable debug logging:
        $ starlink-cli status --log-level DEBUG
"""

import argparse
import sys
import os
import time
import json
import csv
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

# Exit codes
EXIT_CODE_SUCCESS = 0
EXIT_CODE_ERROR = 1
EXIT_CODE_INTERRUPT = 130  # Standard exit code for SIGINT

# Ensure proper import path when running as a script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.starlink_monitor import StarlinkMonitor
from src.connection_manager import SatelliteConnectionManager
from src.config import Config


class StarlinkCLI:
    """Command-line interface for Starlink monitoring"""
    
    def __init__(self, host: str = None, config: Config = None):
        """
        Initialize CLI
        
        Args:
            host: Starlink router IP address (overrides config)
            config: Configuration object (creates default if None)
        """
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        
        try:
            self.monitor = StarlinkMonitor(host=host, config=self.config)
            self.connection_manager = SatelliteConnectionManager(
                enable_starlink=True,
                starlink_host=host or self.config.get('monitor.default_host', '192.168.100.1')
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize CLI: {e}", exc_info=True)
            raise
        
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
        try:
            metrics = self.monitor.get_metrics()
            
            if not metrics:
                print(self.colorize("❌ Failed to get Starlink metrics", 'red'))
                self.logger.error("Failed to retrieve metrics")
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
            
        except Exception as e:
            self.logger.error(f"Error displaying status: {e}", exc_info=True)
            print(self.colorize(f"❌ Error: {e}", 'red'))
    
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
    
    def export_data(self, filename: str, hours: int = 24, format: str = 'json') -> None:
        """
        Export monitoring data to file
        
        Args:
            filename: Output file path
            hours: Hours of historical data to export
            format: Export format ('json' or 'csv')
        """
        try:
            report = self.monitor.get_performance_report(hours=hours)
            
            if format.lower() == 'csv':
                self._export_csv(filename, report)
            else:
                self._export_json(filename, report)
            
            print(f"Data exported to {filename} ({format.upper()} format)")
            self.logger.info(f"Data exported to {filename} in {format.upper()} format")
        except Exception as e:
            self.logger.error(f"Failed to export data: {e}", exc_info=True)
            print(self.colorize(f"❌ Failed to export data: {e}", 'red'))
    
    def _export_json(self, filename: str, report: Dict[str, Any]) -> None:
        """Export data in JSON format"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
    
    def _export_csv(self, filename: str, report: Dict[str, Any]) -> None:
        """Export data in CSV format"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['Metric', 'Value'])
            
            # Write basic info
            writer.writerow(['Status', report.get('status', 'unknown')])
            writer.writerow(['Samples', report.get('samples', 0)])
            writer.writerow(['Availability %', f"{report.get('availability_percent', 0):.2f}"])
            writer.writerow(['Issues Count', report.get('issues_count', 0)])
            writer.writerow(['Active Alerts', report.get('active_alerts', 0)])
            
            # Write averages
            writer.writerow([])
            writer.writerow(['Average Metrics', ''])
            if 'averages' in report:
                for key, value in report['averages'].items():
                    writer.writerow([f'Avg {key}', f'{value:.2f}'])
            
            # Write current metrics
            writer.writerow([])
            writer.writerow(['Current Metrics', ''])
            writer.writerow(['Current Status', report.get('current_status', 'unknown')])
            writer.writerow(['Current Download (Mbps)', f"{report.get('current_download', 0):.2f}"])
            writer.writerow(['Current Latency (ms)', f"{report.get('current_latency', 0):.2f}"])
    
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


def setup_logging(log_level: str = None, log_file: str = None):
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
    """
    config = Config()
    level = log_level or config.get('logging.level', 'INFO')
    log_format = config.get('logging.format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_path = log_file or config.get('logging.file')
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Configure root logger
    handlers = [logging.StreamHandler(sys.stderr)]
    
    if file_path:
        try:
            # Only create directory if file_path contains a directory component
            dir_path = os.path.dirname(file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            handlers.append(logging.FileHandler(file_path))
        except Exception as e:
            print(f"Warning: Failed to setup file logging: {e}", file=sys.stderr)
    
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=handlers
    )


def main() -> None:
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='starlink-cli',
        description="Starlink Connectivity Monitor CLI - Monitor and manage your Starlink connection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status                           # Show current status
  %(prog)s status --log-level DEBUG         # Show status with debug logging
  %(prog)s monitor --interval 30            # Monitor every 30 seconds
  %(prog)s monitor --duration 3600          # Monitor for 1 hour
  %(prog)s report --hours 48                # 48-hour performance report
  %(prog)s export --output data.json        # Export to JSON (default)
  %(prog)s export --output data.csv --format csv  # Export to CSV
  %(prog)s reboot                           # Reboot Starlink dish (requires confirmation)
  %(prog)s thresholds                       # Interactively set monitoring thresholds
  %(prog)s connection                       # Check connection manager status

Configuration:
  Configuration file: ~/.config/starlink_monitor/config.json
  Edit this file to customize thresholds, logging, and defaults.

For more information, visit: https://github.com/danielnovais-tech/starlink_connectivity_tools.py
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
        help='Starlink router IP address (default: from config or 192.168.100.1)',
        metavar='IP'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        help='Monitoring interval in seconds (default: from config or 60)',
        metavar='SECONDS'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        help='Monitoring duration in seconds (for monitor command)',
        metavar='SECONDS'
    )
    
    parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Hours of data for report/export commands (default: 24)',
        metavar='HOURS'
    )
    
    parser.add_argument(
        '--output',
        default='starlink_data.json',
        help='Output file for export command (default: starlink_data.json)',
        metavar='FILE'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'csv'],
        default='json',
        help='Export format: json or csv (default: json)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level (default: from config or INFO)',
        metavar='LEVEL'
    )
    
    parser.add_argument(
        '--log-file',
        help='Log file path (default: from config or stderr only)',
        metavar='FILE'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(log_level=args.log_level, log_file=args.log_file)
    logger = logging.getLogger(__name__)
    
    # Initialize CLI
    try:
        cli = StarlinkCLI(host=args.host)
    except Exception as e:
        logger.critical(f"Failed to initialize CLI: {e}", exc_info=True)
        print(f"\n❌ Fatal Error: {e}", file=sys.stderr)
        sys.exit(EXIT_CODE_ERROR)
    
    # Execute command
    try:
        logger.info(f"Executing command: {args.command}")
        
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
            cli.export_data(filename=args.output, hours=args.hours, format=args.format)
        
        elif args.command == 'connection':
            cli.print_connection_manager_status()
        
        print()  # Final newline
        logger.info(f"Command '{args.command}' completed successfully")
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        print("\n\nOperation cancelled by user.")
        sys.exit(EXIT_CODE_INTERRUPT)
    except Exception as e:
        logger.error(f"Command failed: {e}", exc_info=True)
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(EXIT_CODE_ERROR)


if __name__ == "__main__":
    main()
