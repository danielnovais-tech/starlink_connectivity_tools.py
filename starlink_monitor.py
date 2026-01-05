#!/usr/bin/env python3
"""
Starlink Connectivity Monitor

A Python tool to monitor and optimize Starlink satellite connectivity in crisis scenarios.
This script uses the starlink-client library to periodically check network stats, detect 
connectivity issues, and take automated actions like rebooting the dish if needed.

Inspired by use cases in areas like Venezuela where reliable internet is critical during crises.
"""

import logging
import time
import argparse
import sys
from logging.handlers import RotatingFileHandler
from typing import Dict, Optional, Tuple, List

try:
    from starlink import StarlinkClient
except ImportError:
    print("Error: starlink-client library not found. Install it with: pip install starlink-client")
    sys.exit(1)


# Default configuration values
DEFAULT_CONFIG = {
    'check_interval': 60,  # seconds between checks
    'log_file': 'starlink_connectivity.log',
    'log_max_bytes': 10 * 1024 * 1024,  # 10 MB
    'log_backup_count': 5,
    
    # Thresholds for detecting issues
    'min_uptime_seconds': 300,  # Minimum uptime before considering stable
    'max_ping_latency_ms': 100,  # Maximum acceptable ping latency
    'max_ping_drop_rate': 0.05,  # Maximum acceptable ping drop rate (5%)
    'min_download_mbps': 50,  # Minimum acceptable download speed
    'min_upload_mbps': 5,  # Minimum acceptable upload speed
    'max_obstruction_percentage': 5,  # Maximum acceptable obstruction percentage
    'consecutive_failures_before_reboot': 3,  # Number of failures before triggering reboot
}


class StarlinkMonitor:
    """Monitor Starlink connectivity and take automated actions."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the monitor with optional configuration."""
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.consecutive_failures = 0
        self.client = None
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging to file with rotation."""
        logger = logging.getLogger('StarlinkMonitor')
        logger.setLevel(logging.INFO)
        
        # Create rotating file handler
        file_handler = RotatingFileHandler(
            self.config['log_file'],
            maxBytes=self.config['log_max_bytes'],
            backupCount=self.config['log_backup_count']
        )
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def connect(self) -> bool:
        """Connect to the Starlink dish."""
        try:
            self.client = StarlinkClient()
            self.logger.info("Successfully connected to Starlink dish")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to Starlink dish: {e}")
            return False
    
    def get_stats(self) -> Optional[Dict]:
        """Retrieve current network statistics from the Starlink dish."""
        if not self.client:
            self.logger.error("Client not initialized. Call connect() first.")
            return None
        
        try:
            stats = self.client.get_status()
            return stats
        except Exception as e:
            self.logger.error(f"Failed to retrieve stats: {e}")
            return None
    
    def check_connectivity_health(self, stats: Dict) -> Tuple[bool, List[str]]:
        """
        Check if connectivity meets health thresholds.
        
        Returns:
            tuple: (is_healthy, list of issues detected)
        """
        issues = []
        
        # Check uptime
        uptime = stats.get('uptime', 0)
        if uptime < self.config['min_uptime_seconds']:
            issues.append(f"Low uptime: {uptime}s (min: {self.config['min_uptime_seconds']}s)")
        
        # Check ping latency
        ping_latency = stats.get('pop_ping_latency_ms', 0)
        if ping_latency > self.config['max_ping_latency_ms']:
            issues.append(f"High ping latency: {ping_latency}ms (max: {self.config['max_ping_latency_ms']}ms)")
        
        # Check ping drop rate
        ping_drop_rate = stats.get('pop_ping_drop_rate', 0)
        if ping_drop_rate > self.config['max_ping_drop_rate']:
            issues.append(f"High ping drop rate: {ping_drop_rate*100:.2f}% (max: {self.config['max_ping_drop_rate']*100}%)")
        
        # Check download speed
        download_mbps = stats.get('downlink_throughput_bps', 0) / 1_000_000
        if download_mbps < self.config['min_download_mbps']:
            issues.append(f"Low download speed: {download_mbps:.2f}Mbps (min: {self.config['min_download_mbps']}Mbps)")
        
        # Check upload speed
        upload_mbps = stats.get('uplink_throughput_bps', 0) / 1_000_000
        if upload_mbps < self.config['min_upload_mbps']:
            issues.append(f"Low upload speed: {upload_mbps:.2f}Mbps (min: {self.config['min_upload_mbps']}Mbps)")
        
        # Check obstruction percentage
        obstruction_pct = stats.get('obstruction_percent', 0) * 100
        if obstruction_pct > self.config['max_obstruction_percentage']:
            issues.append(f"High obstruction: {obstruction_pct:.2f}% (max: {self.config['max_obstruction_percentage']}%)")
        
        is_healthy = len(issues) == 0
        return is_healthy, issues
    
    def reboot_dish(self) -> bool:
        """Reboot the Starlink dish."""
        try:
            self.logger.warning("Attempting to reboot Starlink dish...")
            self.client.reboot()
            self.logger.info("Reboot command sent successfully")
            self.consecutive_failures = 0
            return True
        except Exception as e:
            self.logger.error(f"Failed to reboot dish: {e}")
            return False
    
    def log_stats(self, stats: Dict):
        """Log current statistics."""
        uptime = stats.get('uptime', 0)
        ping_latency = stats.get('pop_ping_latency_ms', 0)
        ping_drop_rate = stats.get('pop_ping_drop_rate', 0) * 100
        download_mbps = stats.get('downlink_throughput_bps', 0) / 1_000_000
        upload_mbps = stats.get('uplink_throughput_bps', 0) / 1_000_000
        obstruction_pct = stats.get('obstruction_percent', 0) * 100
        
        self.logger.info(
            f"Stats - Uptime: {uptime}s, "
            f"Ping: {ping_latency:.1f}ms, "
            f"Drop Rate: {ping_drop_rate:.2f}%, "
            f"Download: {download_mbps:.2f}Mbps, "
            f"Upload: {upload_mbps:.2f}Mbps, "
            f"Obstruction: {obstruction_pct:.2f}%"
        )
    
    def monitor_loop(self):
        """Main monitoring loop."""
        self.logger.info("Starting Starlink connectivity monitor...")
        self.logger.info(f"Configuration: {self.config}")
        
        if not self.connect():
            self.logger.error("Failed to connect to Starlink dish. Exiting.")
            return
        
        try:
            while True:
                stats = self.get_stats()
                
                if stats:
                    self.log_stats(stats)
                    is_healthy, issues = self.check_connectivity_health(stats)
                    
                    if is_healthy:
                        self.logger.info("✓ Connectivity is healthy")
                        self.consecutive_failures = 0
                    else:
                        self.consecutive_failures += 1
                        self.logger.warning(
                            f"✗ Connectivity issues detected ({self.consecutive_failures}/{self.config['consecutive_failures_before_reboot']}):"
                        )
                        for issue in issues:
                            self.logger.warning(f"  - {issue}")
                        
                        # Take action if threshold reached
                        if self.consecutive_failures >= self.config['consecutive_failures_before_reboot']:
                            self.logger.warning(
                                f"Consecutive failure threshold reached. Initiating reboot..."
                            )
                            self.reboot_dish()
                            # Wait longer after reboot to allow dish to stabilize
                            time.sleep(self.config['check_interval'] * 3)
                            continue
                else:
                    self.logger.error("Failed to retrieve stats")
                
                # Wait before next check
                time.sleep(self.config['check_interval'])
                
        except KeyboardInterrupt:
            self.logger.info("Monitor stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error in monitor loop: {e}", exc_info=True)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Monitor and optimize Starlink satellite connectivity'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=DEFAULT_CONFIG['check_interval'],
        help=f"Seconds between checks (default: {DEFAULT_CONFIG['check_interval']})"
    )
    parser.add_argument(
        '--log-file',
        type=str,
        default=DEFAULT_CONFIG['log_file'],
        help=f"Log file path (default: {DEFAULT_CONFIG['log_file']})"
    )
    parser.add_argument(
        '--max-latency',
        type=int,
        default=DEFAULT_CONFIG['max_ping_latency_ms'],
        help=f"Maximum acceptable ping latency in ms (default: {DEFAULT_CONFIG['max_ping_latency_ms']})"
    )
    parser.add_argument(
        '--min-download',
        type=int,
        default=DEFAULT_CONFIG['min_download_mbps'],
        help=f"Minimum acceptable download speed in Mbps (default: {DEFAULT_CONFIG['min_download_mbps']})"
    )
    parser.add_argument(
        '--failures-before-reboot',
        type=int,
        default=DEFAULT_CONFIG['consecutive_failures_before_reboot'],
        help=f"Consecutive failures before rebooting (default: {DEFAULT_CONFIG['consecutive_failures_before_reboot']})"
    )
    
    args = parser.parse_args()
    
    # Build custom configuration from arguments
    config = {
        'check_interval': args.interval,
        'log_file': args.log_file,
        'max_ping_latency_ms': args.max_latency,
        'min_download_mbps': args.min_download,
        'consecutive_failures_before_reboot': args.failures_before_reboot,
    }
    
    monitor = StarlinkMonitor(config)
    monitor.monitor_loop()


if __name__ == '__main__':
    main()
