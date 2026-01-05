#!/usr/bin/env python3
"""
starlink_simple_monitor.py
A standalone Python tool to monitor and optimize Starlink satellite connectivity in crisis scenarios.
This script uses the starlink-client library to periodically check network stats,
detect connectivity issues, and take automated actions like rebooting the dish if needed.
Enhanced with features inspired by cases such as Venezuela where reliable internet is critical.

Installation:
pip install starlink-client

Usage:
python starlink_simple_monitor.py [--host 192.168.100.1] [--interval 60] [--min-download 5.0] [--max-latency 100]
"""

import time
import json
import logging
import argparse
import sys
import os
from datetime import datetime
from typing import Dict, Optional, List
import threading

try:
    from starlink_client import StarlinkClient
    STARLINK_AVAILABLE = True
except ImportError:
    STARLINK_AVAILABLE = False
    print("Error: starlink-client library not installed.")
    print("Install with: pip install starlink-client")
    sys.exit(1)


class StarlinkSimpleMonitor:
    """
    Simple yet powerful Starlink monitor for crisis scenarios
    """
    
    def __init__(self, 
                 host: str = "192.168.100.1",
                 log_file: str = "starlink_log.txt",
                 config_file: str = None):
        """
        Initialize Starlink monitor
        
        Args:
            host: Starlink router IP address
            log_file: Log file for tracking connectivity
            config_file: JSON configuration file (optional)
        """
        self.host = host
        self.log_file = log_file
        self.config = self._load_config(config_file)
        
        # Set up logging
        self._setup_logging()
        
        # Initialize Starlink client
        self.client = None
        self._initialize_client()
        
        # Monitoring parameters
        self.min_download_speed = self.config.get('min_download_speed', 5.0)  # Mbps
        self.max_latency = self.config.get('max_latency', 100)  # ms
        self.max_packet_loss = self.config.get('max_packet_loss', 10)  # %
        self.check_interval = self.config.get('check_interval', 60)  # seconds
        self.max_issue_count = self.config.get('max_issue_count', 3)  # consecutive issues before action
        
        # Crisis mode settings
        self.crisis_mode = self.config.get('crisis_mode', False)
        self.enable_auto_recovery = self.config.get('enable_auto_recovery', True)
        self.notify_on_issues = self.config.get('notify_on_issues', True)
        
        # State tracking
        self.issue_count = 0
        self.total_issues = 0
        self.consecutive_good_checks = 0
        self.last_reboot_time = None
        self.monitoring = False
        self.monitor_thread = None
        
        # Performance history
        self.performance_history = []
        self.max_history_size = 1000
        
        # Alert history
        self.alerts = []
        
        logging.info(f"Starlink Simple Monitor initialized for {host}")
        logging.info(f"Thresholds: Download>{self.min_download_speed}Mbps, Latency<{self.max_latency}ms")
    
    def _load_config(self, config_file: Optional[str]) -> Dict:
        """Load configuration from JSON file"""
        default_config = {
            'min_download_speed': 5.0,
            'max_latency': 100,
            'max_packet_loss': 10,
            'check_interval': 60,
            'max_issue_count': 3,
            'crisis_mode': False,
            'enable_auto_recovery': True,
            'notify_on_issues': True,
            'auto_reboot_on_persistent_issues': True,
            'notify_email': None,
            'webhook_url': None
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                # Merge with defaults
                default_config.update(user_config)
                logging.info(f"Loaded configuration from {config_file}")
            except Exception as e:
                logging.error(f"Failed to load config file: {e}")
        
        return default_config
    
    def _setup_logging(self):
        """Setup logging to file and console"""
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def _initialize_client(self):
        """Initialize Starlink client connection"""
        try:
            self.client = StarlinkClient(host=self.host)
            logging.info(f"Connected to Starlink router at {self.host}")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to Starlink: {e}")
            logging.error("Ensure the Starlink router is reachable at the specified IP")
            return False
    
    def get_network_stats(self) -> Optional[Dict]:
        """Get network statistics from Starlink"""
        try:
            if not self.client:
                if not self._initialize_client():
                    return None
            
            stats = self.client.get_network_stats()
            
            # Convert to dictionary for easier handling
            stats_dict = {
                'timestamp': datetime.now().isoformat(),
                'download_speed': stats.download_speed,
                'upload_speed': stats.upload_speed if hasattr(stats, 'upload_speed') else 0,
                'latency': stats.latency,
                'jitter': stats.jitter if hasattr(stats, 'jitter') else 0,
                'packet_loss': stats.packet_loss if hasattr(stats, 'packet_loss') else 0
            }
            
            # Store in history
            self._store_performance_data(stats_dict)
            
            return stats_dict
            
        except Exception as e:
            logging.error(f"Error getting network stats: {e}")
            return None
    
    def get_telemetry_alerts(self) -> List[str]:
        """Get telemetry alerts from Starlink"""
        try:
            if not self.client:
                return []
            
            telemetry = self.client.get_telemetry()
            alerts = []
            
            if telemetry and hasattr(telemetry, 'alerts') and telemetry.alerts:
                for alert in telemetry.alerts:
                    alert_str = f"{alert.type}: {alert.message}"
                    alerts.append(alert_str)
                    if self.notify_on_issues:
                        logging.warning(f"Telemetry Alert: {alert_str}")
            
            return alerts
            
        except Exception as e:
            logging.warning(f"Could not get telemetry: {e}")
            return []
    
    def _store_performance_data(self, stats: Dict):
        """Store performance data in history"""
        self.performance_history.append(stats)
        
        # Trim history if too large
        if len(self.performance_history) > self.max_history_size:
            self.performance_history = self.performance_history[-self.max_history_size:]
    
    def check_connectivity_issues(self, stats: Dict) -> List[str]:
        """
        Check for connectivity issues based on thresholds
        
        Returns:
            List of issue descriptions
        """
        issues = []
        
        if stats['download_speed'] < self.min_download_speed:
            issues.append(f"Low download speed: {stats['download_speed']} Mbps (min: {self.min_download_speed})")
        
        if stats['latency'] > self.max_latency:
            issues.append(f"High latency: {stats['latency']} ms (max: {self.max_latency})")
        
        if 'packet_loss' in stats and stats['packet_loss'] > self.max_packet_loss:
            issues.append(f"High packet loss: {stats['packet_loss']}% (max: {self.max_packet_loss})")
        
        return issues
    
    def enable_crisis_mode(self, min_download: float = 2.0, max_latency: float = 200):
        """
        Enable crisis mode with relaxed thresholds for emergency situations
        
        Args:
            min_download: Minimum download speed in Mbps for crisis mode
            max_latency: Maximum latency in ms for crisis mode
        """
        self.crisis_mode = True
        old_min = self.min_download_speed
        old_max = self.max_latency
        
        self.min_download_speed = min_download
        self.max_latency = max_latency
        
        logging.warning(f"CRISIS MODE ENABLED")
        logging.warning(f"Thresholds adjusted: Download>{min_download}Mbps (was {old_min}), Latency<{max_latency}ms (was {old_max})")
        logging.warning("Auto-recovery enabled, relaxed thresholds for emergency connectivity")
    
    def reboot_dish(self) -> bool:
        """Reboot the Starlink dish"""
        try:
            if self.last_reboot_time:
                time_since_reboot = time.time() - self.last_reboot_time
                if time_since_reboot < 300:  # 5 minutes
                    logging.warning(f"Dish rebooted recently ({time_since_reboot:.0f}s ago). Skipping reboot.")
                    return False
            
            logging.critical("REBOOTING STARLINK DISH")
            
            # Check if reboot method is available
            if hasattr(self.client, 'reboot_dish'):
                self.client.reboot_dish()
            else:
                # Try alternative reboot method
                logging.warning("reboot_dish method not available, trying alternative...")
                # In some versions, it might be reboot() instead
                if hasattr(self.client, 'reboot'):
                    self.client.reboot()
                else:
                    logging.error("No reboot method found on StarlinkClient")
                    return False
            
            self.last_reboot_time = time.time()
            self.issue_count = 0  # Reset issue count after reboot
            
            # Log reboot action
            reboot_log = {
                'timestamp': datetime.now().isoformat(),
                'action': 'dish_reboot',
                'reason': f'Persistent issues (count: {self.max_issue_count})',
                'issues_before_reboot': self.total_issues
            }
            self.alerts.append(reboot_log)
            
            logging.info("Dish reboot command sent successfully")
            logging.info("Dish will be offline for approximately 5-10 minutes")
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to reboot dish: {e}")
            return False
    
    def send_notification(self, message: str, issue_type: str = "warning"):
        """
        Send notification about connectivity issues
        
        Args:
            message: Notification message
            issue_type: Type of issue (warning, critical, info)
        """
        # Get current metrics, but use cached data if available to avoid recursion
        metrics = None
        if self.performance_history:
            metrics = self.performance_history[-1]  # Use most recent cached data
        
        notification = {
            'timestamp': datetime.now().isoformat(),
            'type': issue_type,
            'message': message,
            'metrics': metrics
        }
        
        self.alerts.append(notification)
        
        # Log based on issue type
        if issue_type == "critical":
            logging.critical(f"NOTIFICATION: {message}")
        elif issue_type == "warning":
            logging.warning(f"NOTIFICATION: {message}")
        else:
            logging.info(f"NOTIFICATION: {message}")
        
        # In a real implementation, this could send email, SMS, or webhook
        if self.config.get('webhook_url'):
            self._send_webhook_notification(notification)
    
    def _send_webhook_notification(self, notification: Dict):
        """Send notification to webhook (placeholder for implementation)"""
        # This would be implemented based on specific notification service
        # Example: requests.post(self.config['webhook_url'], json=notification)
        logging.debug(f"Webhook notification not configured. Notification: {notification['type']} - {notification['message']}")
        pass
    
    def run_single_check(self) -> bool:
        """
        Run a single connectivity check
        
        Returns:
            True if connectivity is good, False if issues detected
        """
        stats = self.get_network_stats()
        
        if not stats:
            self.issue_count += 1
            self.total_issues += 1
            logging.error("Failed to get network statistics")
            
            if self.issue_count >= self.max_issue_count:
                self.send_notification(
                    f"Failed to get stats {self.issue_count} times consecutively",
                    "critical"
                )
            
            return False
        
        # Log current stats
        logging.info(
            f"Download: {stats['download_speed']:.1f} Mbps, "
            f"Upload: {stats['upload_speed']:.1f} Mbps, "
            f"Latency: {stats['latency']:.1f} ms"
        )
        
        # Check for issues
        issues = self.check_connectivity_issues(stats)
        
        if issues:
            self.issue_count += 1
            self.total_issues += 1
            self.consecutive_good_checks = 0
            
            for issue in issues:
                logging.warning(f"Issue detected: {issue}")
            
            # Send notification if enabled
            if self.notify_on_issues:
                issue_summary = ", ".join(issues)
                self.send_notification(
                    f"Connectivity issues: {issue_summary}",
                    "critical" if self.issue_count >= self.max_issue_count else "warning"
                )
            
            # Check if we need to take action
            if self.issue_count >= self.max_issue_count and self.enable_auto_recovery:
                logging.error(f"Persistent issues detected ({self.issue_count} consecutive). Taking action...")
                
                if self.config.get('auto_reboot_on_persistent_issues', True):
                    self.reboot_dish()
                    # Wait after reboot with ability to interrupt
                    wait_time = 300  # 5 minutes
                    logging.info(f"Waiting {wait_time}s for dish to reboot and reconnect...")
                    for _ in range(wait_time):
                        if not self.monitoring:
                            break
                        time.sleep(1)
                    self.issue_count = 0
                else:
                    logging.warning("Auto-reboot disabled. Manual intervention required.")
            
            return False
        else:
            # Connectivity is good
            self.issue_count = 0
            self.consecutive_good_checks += 1
            
            if self.consecutive_good_checks == 1:  # Just recovered
                logging.info("Connectivity restored to normal")
                if self.notify_on_issues:
                    self.send_notification("Connectivity restored to normal", "info")
            
            # Check telemetry alerts
            telemetry_alerts = self.get_telemetry_alerts()
            for alert in telemetry_alerts:
                logging.warning(f"Telemetry Alert: {alert}")
            
            return True
    
    def start_continuous_monitoring(self, interval: int = None):
        """
        Start continuous monitoring
        
        Args:
            interval: Check interval in seconds (overrides config)
        """
        if interval:
            self.check_interval = interval
        
        self.monitoring = True
        logging.info(f"Starting continuous monitoring (interval: {self.check_interval}s)")
        
        # Run in a separate thread
        def monitor_loop():
            while self.monitoring:
                self.run_single_check()
                
                # Sleep for interval
                for _ in range(self.check_interval):
                    if not self.monitoring:
                        break
                    time.sleep(1)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logging.info("Monitoring stopped")
    
    def get_performance_report(self, hours: int = 24) -> Dict:
        """
        Generate performance report
        
        Args:
            hours: Hours of data to include in report
            
        Returns:
            Dictionary with performance statistics
        """
        # Filter data from specified time period
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        recent_data = [
            d for d in self.performance_history
            if datetime.fromisoformat(d['timestamp']).timestamp() > cutoff_time
        ]
        
        if not recent_data:
            return {'status': 'no_data', 'hours': hours}
        
        # Calculate statistics
        download_speeds = [d['download_speed'] for d in recent_data]
        upload_speeds = [d['upload_speed'] for d in recent_data]
        latencies = [d['latency'] for d in recent_data]
        
        report = {
            'period_hours': hours,
            'samples': len(recent_data),
            'timestamp': datetime.now().isoformat(),
            'averages': {
                'download_speed': sum(download_speeds) / len(download_speeds),
                'upload_speed': sum(upload_speeds) / len(upload_speeds),
                'latency': sum(latencies) / len(latencies),
            },
            'maximums': {
                'download_speed': max(download_speeds),
                'upload_speed': max(upload_speeds),
                'latency': max(latencies),
            },
            'minimums': {
                'download_speed': min(download_speeds),
                'upload_speed': min(upload_speeds),
                'latency': min(latencies),
            },
            'issues': {
                'total_issues': self.total_issues,
                'recent_alerts': len([a for a in self.alerts[-10:] if a['type'] in ['warning', 'critical']]),
                'last_reboot': self.last_reboot_time
            },
            'current_thresholds': {
                'min_download_speed': self.min_download_speed,
                'max_latency': self.max_latency,
                'max_packet_loss': self.max_packet_loss,
            },
            'crisis_mode': self.crisis_mode
        }
        
        return report
    
    def save_report(self, filename: str = "starlink_report.json", hours: int = 24):
        """Save performance report to JSON file"""
        report = self.get_performance_report(hours=hours)
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logging.info(f"Report saved to {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to save report: {e}")
            return False
    
    def export_logs(self, filename: str = "starlink_logs_export.json"):
        """Export logs and alerts to JSON file"""
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'monitor_config': self.config,
            'performance_history': self.performance_history[-100:],  # Last 100 entries
            'alerts': self.alerts,
            'summary': {
                'total_issues': self.total_issues,
                'crisis_mode': self.crisis_mode,
                'last_reboot': self.last_reboot_time,
                'check_interval': self.check_interval
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            logging.info(f"Logs exported to {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to export logs: {e}")
            return False


def main():
    """Main function for command-line execution"""
    parser = argparse.ArgumentParser(
        description="Starlink Connectivity Monitor for Crisis Scenarios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Start monitoring with default settings
  %(prog)s --interval 30            # Check every 30 seconds
  %(prog)s --crisis-mode            # Enable crisis mode (relaxed thresholds)
  %(prog)s --single-check           # Run single check and exit
  %(prog)s --reboot                 # Reboot dish and exit
  %(prog)s --report --hours 48      # Generate 48-hour report and exit
  %(prog)s --config myconfig.json   # Use custom configuration file
        
Inspired by connectivity challenges in Venezuela and other crisis scenarios.
        """
    )
    
    parser.add_argument(
        '--host',
        default='192.168.100.1',
        help='Starlink router IP address (default: 192.168.100.1)'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=None,
        help='Check interval in seconds (default: 60)'
    )
    
    parser.add_argument(
        '--min-download',
        type=float,
        default=None,
        help='Minimum download speed in Mbps (default: 5.0)'
    )
    
    parser.add_argument(
        '--max-latency',
        type=int,
        default=None,
        help='Maximum latency in ms (default: 100)'
    )
    
    parser.add_argument(
        '--max-issues',
        type=int,
        default=None,
        help='Consecutive issues before action (default: 3)'
    )
    
    parser.add_argument(
        '--crisis-mode',
        action='store_true',
        help='Enable crisis mode with relaxed thresholds'
    )
    
    parser.add_argument(
        '--single-check',
        action='store_true',
        help='Run a single check and exit'
    )
    
    parser.add_argument(
        '--reboot',
        action='store_true',
        help='Reboot Starlink dish and exit'
    )
    
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate performance report and exit'
    )
    
    parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Hours of data for report (default: 24)'
    )
    
    parser.add_argument(
        '--config',
        help='JSON configuration file'
    )
    
    parser.add_argument(
        '--log-file',
        default='starlink_log.txt',
        help='Log file path (default: starlink_log.txt)'
    )
    
    parser.add_argument(
        '--export-logs',
        action='store_true',
        help='Export logs to JSON file and exit'
    )
    
    args = parser.parse_args()
    
    # Initialize monitor
    monitor = StarlinkSimpleMonitor(
        host=args.host,
        log_file=args.log_file,
        config_file=args.config
    )
    
    # Override config with command-line arguments
    if args.interval is not None:
        monitor.check_interval = args.interval
    
    if args.min_download is not None:
        monitor.min_download_speed = args.min_download
    
    if args.max_latency is not None:
        monitor.max_latency = args.max_latency
    
    if args.max_issues is not None:
        monitor.max_issue_count = args.max_issues
    
    if args.crisis_mode:
        monitor.enable_crisis_mode(
            min_download=max(1.0, monitor.min_download_speed * 0.5),
            max_latency=min(500, monitor.max_latency * 2)
        )
    
    try:
        if args.reboot:
            # Reboot dish
            print(f"Rebooting Starlink dish at {args.host}...")
            success = monitor.reboot_dish()
            if success:
                print("Reboot command sent successfully.")
                print("Dish will be offline for 5-10 minutes.")
            else:
                print("Failed to send reboot command.")
            
        elif args.report:
            # Generate report
            report = monitor.get_performance_report(hours=args.hours)
            print("\n" + "="*60)
            print("STARLINK PERFORMANCE REPORT")
            print("="*60)
            print(f"Period: Last {args.hours} hours")
            print(f"Samples: {report.get('samples', 0)}")
            
            if 'averages' in report:
                print("\nAverages:")
                print(f"  Download: {report['averages']['download_speed']:.1f} Mbps")
                print(f"  Upload: {report['averages']['upload_speed']:.1f} Mbps")
                print(f"  Latency: {report['averages']['latency']:.1f} ms")
            
            print(f"\nTotal Issues: {report.get('issues', {}).get('total_issues', 0)}")
            print(f"Crisis Mode: {report.get('crisis_mode', False)}")
            
            # Save report to file
            filename = f"starlink_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            monitor.save_report(filename=filename, hours=args.hours)
            print(f"\nReport saved to: {filename}")
            
        elif args.export_logs:
            # Export logs
            filename = f"starlink_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            success = monitor.export_logs(filename=filename)
            if success:
                print(f"Logs exported to: {filename}")
            else:
                print("Failed to export logs.")
                
        elif args.single_check:
            # Run single check
            print(f"Checking Starlink connectivity at {args.host}...")
            success = monitor.run_single_check()
            if success:
                print("Connectivity check: OK")
            else:
                print("Connectivity check: ISSUES DETECTED")
                
        else:
            # Start continuous monitoring
            print("\n" + "="*60)
            print("STARLINK CONNECTIVITY MONITOR")
            print("="*60)
            print(f"Host: {args.host}")
            print(f"Check Interval: {monitor.check_interval}s")
            print(f"Thresholds: Download > {monitor.min_download_speed}Mbps, Latency < {monitor.max_latency}ms")
            print(f"Crisis Mode: {monitor.crisis_mode}")
            print("\nPress Ctrl+C to stop monitoring")
            print("="*60 + "\n")
            
            monitor.start_continuous_monitoring()
            
            try:
                # Keep main thread alive
                while monitor.monitoring:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\nMonitoring stopped by user.")
            finally:
                monitor.stop_monitoring()
                
                # Generate final report
                report = monitor.get_performance_report(hours=1)  # Last hour
                print("\n" + "="*60)
                print("FINAL MONITORING REPORT")
                print("="*60)
                print(f"Total checks: {report.get('samples', 0)}")
                print(f"Total issues detected: {report.get('issues', {}).get('total_issues', 0)}")
                if 'averages' in report:
                    print(f"Average download: {report['averages']['download_speed']:.1f} Mbps")
                    print(f"Average latency: {report['averages']['latency']:.1f} ms")
                
                # Save final report
                final_report_file = f"starlink_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                monitor.save_report(filename=final_report_file, hours=24)
                print(f"\nFinal report saved to: {final_report_file}")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
