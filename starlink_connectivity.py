#!/usr/bin/env python3
"""
Starlink Connectivity Monitoring Tool

A comprehensive tool for monitoring Starlink connectivity with features including:
- Command-line interface with multiple operation modes
- Crisis mode for emergency situations
- Enhanced logging and reporting
- Thread-safe background monitoring
- Configuration management
- Venezuela-inspired resilience features
"""

import argparse
import json
import logging
import os
import signal
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import statistics


# Default configuration
DEFAULT_CONFIG = {
    "thresholds": {
        "ping_timeout": 5,
        "max_failures": 3,
        "min_success_rate": 0.8,
        "alert_latency_ms": 100
    },
    "crisis_thresholds": {
        "ping_timeout": 10,
        "max_failures": 5,
        "min_success_rate": 0.5,
        "alert_latency_ms": 300
    },
    "monitoring": {
        "check_interval": 60,
        "history_size": 1000
    },
    "logging": {
        "log_file": "starlink_monitor.log",
        "log_level": "INFO",
        "console_output": True
    },
    "starlink": {
        "dish_ip": "192.168.100.1",
        "router_ip": "192.168.1.1"
    },
    "notifications": {
        "enabled": False,
        "email": None,
        "webhook_url": None
    }
}


class StarlinkMonitor:
    """Main monitoring class for Starlink connectivity"""
    
    def __init__(self, config: Dict[str, Any], crisis_mode: bool = False):
        """
        Initialize the Starlink monitor
        
        Args:
            config: Configuration dictionary
            crisis_mode: Enable crisis mode with relaxed thresholds
        """
        self.config = config
        self.crisis_mode = crisis_mode
        self.thresholds = config['crisis_thresholds' if crisis_mode else 'thresholds']
        self.history: List[Dict[str, Any]] = []
        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        
        # Setup logging
        self._setup_logging()
        
        if crisis_mode:
            self.logger.warning("🚨 CRISIS MODE ACTIVATED - Using relaxed thresholds for emergency scenarios")
    
    def _setup_logging(self):
        """Configure logging with both file and console output"""
        log_config = self.config['logging']
        log_level = getattr(logging, log_config['log_level'].upper(), logging.INFO)
        
        # Create logger
        self.logger = logging.getLogger('StarlinkMonitor')
        self.logger.setLevel(log_level)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # File handler
        log_file = Path(log_config['log_file'])
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        if log_config['console_output']:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
    
    def check_connectivity(self) -> Dict[str, Any]:
        """
        Check Starlink connectivity and return status
        
        Returns:
            Dictionary with connectivity status and metrics
        """
        import subprocess
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'latency_ms': None,
            'packet_loss': 0,
            'error': None
        }
        
        try:
            # Try to ping Starlink dish
            dish_ip = self.config['starlink']['dish_ip']
            timeout = self.thresholds['ping_timeout']
            
            # Use ping command (cross-platform)
            ping_cmd = ['ping', '-c', '4', '-W', str(timeout), dish_ip]
            if sys.platform == 'win32':
                ping_cmd = ['ping', '-n', '4', '-w', str(timeout * 1000), dish_ip]
            
            process = subprocess.run(
                ping_cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 5
            )
            
            if process.returncode == 0:
                # Parse ping output for latency
                output = process.stdout
                
                # Extract average latency (platform-specific parsing)
                if sys.platform == 'win32':
                    # Windows: "Average = XXXms"
                    if 'Average' in output:
                        avg_line = [l for l in output.split('\n') if 'Average' in l][0]
                        latency = float(avg_line.split('=')[-1].replace('ms', '').strip())
                        result['latency_ms'] = latency
                else:
                    # Linux/Mac: "min/avg/max/stddev = ..."
                    if 'avg' in output or 'rtt' in output:
                        stats_line = [l for l in output.split('\n') if 'avg' in l or 'rtt' in l]
                        if stats_line:
                            parts = stats_line[0].split('=')[-1].strip().split('/')
                            if len(parts) >= 2:
                                result['latency_ms'] = float(parts[1])
                
                # Check for packet loss
                if 'packet loss' in output.lower():
                    loss_line = [l for l in output.split('\n') if 'packet loss' in l.lower()][0]
                    loss_pct = float(loss_line.split('%')[0].split()[-1])
                    result['packet_loss'] = loss_pct / 100.0
                
                # Determine status
                if result['packet_loss'] == 0 and result['latency_ms']:
                    if result['latency_ms'] < self.thresholds['alert_latency_ms']:
                        result['status'] = 'excellent'
                    else:
                        result['status'] = 'good'
                elif result['packet_loss'] < 0.25:
                    result['status'] = 'degraded'
                else:
                    result['status'] = 'poor'
            else:
                result['status'] = 'offline'
                result['error'] = 'Failed to reach Starlink dish'
                
        except subprocess.TimeoutExpired:
            result['status'] = 'timeout'
            result['error'] = 'Ping timeout exceeded'
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            self.logger.error(f"Error checking connectivity: {e}")
        
        return result
    
    def _add_to_history(self, check_result: Dict[str, Any]):
        """Thread-safe addition to history with size limit"""
        with self.lock:
            self.history.append(check_result)
            max_size = self.config['monitoring']['history_size']
            if len(self.history) > max_size:
                self.history = self.history[-max_size:]
    
    def single_check(self) -> Dict[str, Any]:
        """
        Perform a single connectivity check
        
        Returns:
            Connectivity check result
        """
        self.logger.info("Performing single connectivity check...")
        result = self.check_connectivity()
        
        # Log result
        status = result['status']
        if status in ['excellent', 'good']:
            self.logger.info(f"✓ Connectivity: {status.upper()} - Latency: {result.get('latency_ms', 'N/A')}ms")
        elif status in ['degraded', 'poor']:
            self.logger.warning(f"⚠ Connectivity: {status.upper()} - Latency: {result.get('latency_ms', 'N/A')}ms, Packet Loss: {result.get('packet_loss', 0)*100:.1f}%")
        else:
            self.logger.error(f"✗ Connectivity: {status.upper()} - {result.get('error', 'Unknown error')}")
        
        self._add_to_history(result)
        return result
    
    def monitor(self, duration: Optional[int] = None):
        """
        Start continuous monitoring
        
        Args:
            duration: Optional monitoring duration in seconds (None = infinite)
        """
        self.running = True
        interval = self.config['monitoring']['check_interval']
        start_time = time.time()
        
        self.logger.info(f"Starting continuous monitoring (interval: {interval}s)...")
        
        consecutive_failures = 0
        
        try:
            while self.running:
                result = self.check_connectivity()
                self._add_to_history(result)
                
                # Check for alerts
                if result['status'] in ['offline', 'timeout', 'error']:
                    consecutive_failures += 1
                    self.logger.error(f"Connection failure {consecutive_failures}/{self.thresholds['max_failures']}: {result['error']}")
                    
                    if consecutive_failures >= self.thresholds['max_failures']:
                        self._send_alert(f"CRITICAL: {consecutive_failures} consecutive failures detected!")
                else:
                    if consecutive_failures > 0:
                        self.logger.info(f"Connection restored after {consecutive_failures} failures")
                    consecutive_failures = 0
                    
                    # Check latency alerts
                    if result.get('latency_ms') and result['latency_ms'] > self.thresholds['alert_latency_ms']:
                        self.logger.warning(f"High latency detected: {result['latency_ms']}ms")
                
                # Check duration
                if duration and (time.time() - start_time) >= duration:
                    self.logger.info(f"Monitoring duration ({duration}s) completed")
                    break
                
                # Wait for next check
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring interrupted by user")
        finally:
            self.running = False
    
    def start_background_monitor(self):
        """Start monitoring in a background thread"""
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.logger.warning("Background monitoring already running")
            return
        
        self.monitor_thread = threading.Thread(target=self.monitor, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Background monitoring started")
    
    def stop_background_monitor(self):
        """Stop background monitoring thread"""
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.running = False
            self.monitor_thread.join(timeout=10)
            self.logger.info("Background monitoring stopped")
    
    def _send_alert(self, message: str):
        """
        Send alert notification
        
        Args:
            message: Alert message to send
        """
        self.logger.critical(f"🚨 ALERT: {message}")
        
        # Here you could add email, SMS, or webhook notifications
        if self.config['notifications']['enabled']:
            # Placeholder for actual notification implementation
            self.logger.info(f"Notification sent: {message}")
    
    def reboot_starlink(self) -> bool:
        """
        Attempt to reboot Starlink dish (if API available)
        
        Returns:
            True if reboot command was sent successfully
        """
        self.logger.warning("Reboot functionality requires Starlink API access (not implemented)")
        self.logger.info("Alternative: Power cycle the dish manually or via smart outlet")
        return False
    
    def generate_report(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive performance report
        
        Args:
            output_file: Optional file path to save report (JSON format)
        
        Returns:
            Report dictionary with statistics
        """
        with self.lock:
            history = self.history.copy()
        
        if not history:
            self.logger.warning("No data available for report generation")
            return {}
        
        # Calculate statistics
        total_checks = len(history)
        status_counts = {}
        latencies = []
        packet_losses = []
        
        for entry in history:
            status = entry['status']
            status_counts[status] = status_counts.get(status, 0) + 1
            
            if entry.get('latency_ms'):
                latencies.append(entry['latency_ms'])
            if entry.get('packet_loss') is not None:
                packet_losses.append(entry['packet_loss'])
        
        successful_checks = sum(status_counts.get(s, 0) for s in ['excellent', 'good', 'degraded'])
        success_rate = successful_checks / total_checks if total_checks > 0 else 0
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'crisis_mode': self.crisis_mode,
            'period': {
                'start': history[0]['timestamp'] if history else None,
                'end': history[-1]['timestamp'] if history else None,
                'total_checks': total_checks
            },
            'connectivity': {
                'success_rate': success_rate,
                'status_breakdown': status_counts
            },
            'performance': {
                'latency': {
                    'min': min(latencies) if latencies else None,
                    'max': max(latencies) if latencies else None,
                    'avg': statistics.mean(latencies) if latencies else None,
                    'median': statistics.median(latencies) if latencies else None
                },
                'packet_loss': {
                    'avg': statistics.mean(packet_losses) if packet_losses else None,
                    'max': max(packet_losses) if packet_losses else None
                }
            },
            'alerts': {
                'success_rate_threshold_met': success_rate >= self.thresholds['min_success_rate']
            }
        }
        
        # Save to file if requested
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            self.logger.info(f"Report saved to {output_file}")
        
        return report
    
    def export_logs(self, output_file: str):
        """
        Export monitoring history to JSON file
        
        Args:
            output_file: Path to save the exported logs
        """
        with self.lock:
            history = self.history.copy()
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(history, f, indent=2)
        
        self.logger.info(f"Exported {len(history)} log entries to {output_file}")
    
    def print_report(self):
        """Print a formatted report to console"""
        report = self.generate_report()
        
        if not report:
            return
        
        print("\n" + "="*60)
        print("STARLINK CONNECTIVITY REPORT")
        print("="*60)
        
        if self.crisis_mode:
            print("⚠️  CRISIS MODE ACTIVE")
        
        print(f"\nPeriod: {report['period']['start']} to {report['period']['end']}")
        print(f"Total Checks: {report['period']['total_checks']}")
        
        print(f"\nConnectivity Success Rate: {report['connectivity']['success_rate']:.1%}")
        print("\nStatus Breakdown:")
        for status, count in sorted(report['connectivity']['status_breakdown'].items()):
            pct = count / report['period']['total_checks'] * 100
            print(f"  {status.upper():12s}: {count:4d} ({pct:5.1f}%)")
        
        if report['performance']['latency']['avg']:
            print(f"\nLatency Statistics:")
            print(f"  Min:    {report['performance']['latency']['min']:.1f} ms")
            print(f"  Max:    {report['performance']['latency']['max']:.1f} ms")
            print(f"  Avg:    {report['performance']['latency']['avg']:.1f} ms")
            print(f"  Median: {report['performance']['latency']['median']:.1f} ms")
        
        if report['performance']['packet_loss']['avg'] is not None:
            print(f"\nPacket Loss:")
            print(f"  Avg: {report['performance']['packet_loss']['avg']:.1%}")
            print(f"  Max: {report['performance']['packet_loss']['max']:.1%}")
        
        threshold_met = "✓" if report['alerts']['success_rate_threshold_met'] else "✗"
        print(f"\nThreshold Status: {threshold_met}")
        
        print("="*60 + "\n")


def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file or use defaults
    
    Args:
        config_file: Optional path to JSON configuration file
    
    Returns:
        Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    
    if config_file and Path(config_file).exists():
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
            
            # Deep merge configurations
            for key, value in user_config.items():
                if isinstance(value, dict) and key in config:
                    config[key].update(value)
                else:
                    config[key] = value
            
            logging.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            logging.error(f"Error loading config file: {e}")
    
    return config


def create_example_config(output_file: str = "starlink_config.json"):
    """Create an example configuration file"""
    output_path = Path(output_file)
    
    if output_path.exists():
        print(f"Configuration file already exists: {output_file}")
        return
    
    with open(output_path, 'w') as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    
    print(f"Example configuration created: {output_file}")
    print("Edit this file to customize monitoring parameters")


def main():
    """Main entry point for the Starlink connectivity tool"""
    parser = argparse.ArgumentParser(
        description='Starlink Connectivity Monitoring Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s monitor --interval 30                    # Monitor every 30 seconds
  %(prog)s single-check                             # Perform one connectivity check
  %(prog)s report --output report.json              # Generate report
  %(prog)s monitor --crisis-mode --duration 3600    # Monitor in crisis mode for 1 hour
  %(prog)s --config custom.json monitor             # Use custom configuration
        """
    )
    
    # Global options
    parser.add_argument('--config', type=str, help='Path to JSON configuration file')
    parser.add_argument('--crisis-mode', action='store_true', 
                       help='Enable crisis mode with relaxed thresholds')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Operation mode')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Continuous monitoring mode')
    monitor_parser.add_argument('--interval', type=int, 
                               help='Check interval in seconds (overrides config)')
    monitor_parser.add_argument('--duration', type=int,
                               help='Monitoring duration in seconds (default: infinite)')
    
    # Single check command
    subparsers.add_parser('single-check', help='Perform a single connectivity check')
    
    # Reboot command
    subparsers.add_parser('reboot', help='Attempt to reboot Starlink dish')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate performance report')
    report_parser.add_argument('--output', '-o', type=str,
                              help='Output file for report (JSON format)')
    report_parser.add_argument('--export-logs', type=str,
                              help='Export raw logs to JSON file')
    
    # Create config command
    config_parser = subparsers.add_parser('create-config', 
                                          help='Create example configuration file')
    config_parser.add_argument('--output', '-o', type=str, default='starlink_config.json',
                              help='Output file for configuration')
    
    args = parser.parse_args()
    
    # Handle create-config command
    if args.command == 'create-config':
        create_example_config(args.output)
        return 0
    
    # Load configuration
    config = load_config(args.config)
    
    # Apply command-line overrides
    if args.verbose:
        config['logging']['log_level'] = 'DEBUG'
    
    if hasattr(args, 'interval') and args.interval:
        config['monitoring']['check_interval'] = args.interval
    
    # Create monitor instance
    monitor = StarlinkMonitor(config, crisis_mode=args.crisis_mode)
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        print("\nShutdown signal received...")
        monitor.stop_background_monitor()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Execute command
    try:
        if args.command == 'monitor' or args.command is None:
            duration = getattr(args, 'duration', None)
            monitor.monitor(duration=duration)
        
        elif args.command == 'single-check':
            result = monitor.single_check()
            print(json.dumps(result, indent=2))
        
        elif args.command == 'reboot':
            success = monitor.reboot_starlink()
            return 0 if success else 1
        
        elif args.command == 'report':
            if hasattr(args, 'export_logs') and args.export_logs:
                monitor.export_logs(args.export_logs)
            
            output = getattr(args, 'output', None)
            monitor.generate_report(output_file=output)
            monitor.print_report()
        
        return 0
    
    except Exception as e:
        monitor.logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
