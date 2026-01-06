#!/usr/bin/env python3
"""
Example usage of the Starlink Connectivity Tool

This script demonstrates various ways to use the monitoring tool.
"""

import subprocess
import time

def run_command(cmd, description):
    """Run a command and display its output"""
    print("\n" + "="*60)
    print(f"EXAMPLE: {description}")
    print("="*60)
    print(f"Command: {cmd}")
    print("-"*60)
    
    result = subprocess.run(cmd, shell=True, capture_output=False)
    
    if result.returncode == 0:
        print(f"✓ {description} completed successfully")
    else:
        print(f"⚠ {description} exited with code {result.returncode}")
    
    return result.returncode


def main():
    """Run example commands"""
    print("\n" + "="*60)
    print("STARLINK CONNECTIVITY TOOL - USAGE EXAMPLES")
    print("="*60)
    
    examples = [
        # Configuration
        ("python starlink_connectivity.py create-config --output my_config.json",
         "Create a custom configuration file"),
        
        # Single check
        ("timeout 15 python starlink_connectivity.py single-check",
         "Perform a single connectivity check"),
        
        # Crisis mode
        ("timeout 15 python starlink_connectivity.py --crisis-mode single-check",
         "Single check in crisis mode"),
        
        # Verbose mode
        ("timeout 15 python starlink_connectivity.py --verbose single-check",
         "Single check with verbose logging"),
        
        # Monitor with custom interval (just for demo, will timeout)
        ("timeout 15 python starlink_connectivity.py monitor --interval 5 --duration 10",
         "Monitor with 5-second interval for 10 seconds"),
    ]
    
    for cmd, description in examples:
        run_command(cmd, description)
        time.sleep(1)
    
    print("\n" + "="*60)
    print("ADDITIONAL COMMANDS YOU CAN TRY:")
    print("="*60)
    print("1. Monitor continuously:")
    print("   python starlink_connectivity.py monitor")
    print()
    print("2. Generate a report (requires monitoring history):")
    print("   python starlink_connectivity.py report")
    print()
    print("3. Save report to file:")
    print("   python starlink_connectivity.py report --output report.json")
    print()
    print("4. Export logs:")
    print("   python starlink_connectivity.py report --export-logs logs.json")
    print()
    print("5. Use custom configuration:")
    print("   python starlink_connectivity.py --config my_config.json monitor")
    print()
    print("6. Crisis mode monitoring:")
    print("   python starlink_connectivity.py --crisis-mode monitor --duration 3600")
    print("="*60)


if __name__ == '__main__':
    main()
