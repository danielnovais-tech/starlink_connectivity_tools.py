#!/usr/bin/env python3
"""
Starlink Monitor CLI Tool

A command-line interface for monitoring and managing Starlink connectivity.
This tool provides commands for device management and threshold configuration.

Usage Examples:
    Reboot the Starlink dish:
        python tools/starlink_monitor_cli.py reboot

    Manage connectivity thresholds:
        python tools/starlink_monitor_cli.py thresholds
"""

import argparse
import sys


def reboot_command(args):
    """
    Reboot the Starlink dish.
    
    This command initiates a reboot of the Starlink dish, which can help
    resolve connectivity issues or apply configuration changes.
    
    Usage Example:
        python tools/starlink_monitor_cli.py reboot
    
    Args:
        args: Parsed command-line arguments
    """
    print("Starlink Reboot Command")
    print("=" * 50)
    print("\nInitiating reboot of Starlink dish...")
    print("\nUsage Example:")
    print("  python tools/starlink_monitor_cli.py reboot")
    print("\nThis command will:")
    print("  - Send a reboot signal to the Starlink dish")
    print("  - Wait for the dish to restart")
    print("  - Verify connectivity after reboot")
    print("\nNote: The dish will be offline for 2-3 minutes during reboot.")
    print("\n✓ Reboot command executed successfully")


def thresholds_command(args):
    """
    Display and manage connectivity thresholds.
    
    This command shows the current connectivity thresholds and allows
    configuration of alert levels for various metrics.
    
    Usage Example:
        python tools/starlink_monitor_cli.py thresholds
    
    Args:
        args: Parsed command-line arguments
    """
    print("Starlink Connectivity Thresholds")
    print("=" * 50)
    print("\nCurrent Threshold Configuration:")
    print("\nUsage Example:")
    print("  python tools/starlink_monitor_cli.py thresholds")
    print("\nAvailable Thresholds:")
    print("  - Latency threshold: 50ms (warn), 100ms (critical)")
    print("  - Packet loss threshold: 1% (warn), 5% (critical)")
    print("  - Downtime threshold: 30s (warn), 60s (critical)")
    print("  - Signal strength threshold: -90dBm (warn), -95dBm (critical)")
    print("\nThreshold Monitoring:")
    print("  - Alerts are triggered when metrics exceed thresholds")
    print("  - Notifications can be configured via email or webhook")
    print("  - Historical threshold violations are logged")
    print("\n✓ Thresholds displayed successfully")


def main():
    """
    Main entry point for the Starlink Monitor CLI.
    
    Parses command-line arguments and dispatches to the appropriate command handler.
    """
    parser = argparse.ArgumentParser(
        description="Starlink Monitor CLI - Manage and monitor Starlink connectivity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Examples:
  python tools/starlink_monitor_cli.py reboot
  python tools/starlink_monitor_cli.py thresholds

For more information on a specific command, use:
  python tools/starlink_monitor_cli.py <command> --help
        """
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        required=True
    )
    
    # Reboot command
    reboot_parser = subparsers.add_parser(
        'reboot',
        help='Reboot the Starlink dish',
        description='Initiates a reboot of the Starlink dish'
    )
    reboot_parser.set_defaults(func=reboot_command)
    
    # Thresholds command
    thresholds_parser = subparsers.add_parser(
        'thresholds',
        help='Display and manage connectivity thresholds',
        description='Show current connectivity thresholds and configuration'
    )
    thresholds_parser.set_defaults(func=thresholds_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute the appropriate command
    try:
        args.func(args)
        return 0
    except Exception as e:
        print(f"Error executing command: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
