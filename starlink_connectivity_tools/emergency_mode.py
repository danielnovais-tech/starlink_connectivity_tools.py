"""
EmergencyMode - Handle emergency connectivity scenarios.
"""

import time
from datetime import datetime


class EmergencyMode:
    """
    Emergency mode handler for critical connectivity situations.
    
    Provides automated monitoring, diagnostics, and recovery procedures
    for Starlink connectivity in emergency scenarios.
    """
    
    # Configuration constants
    SNR_THRESHOLD = 8.0  # Signal-to-noise ratio threshold for good signal quality
    REBOOT_WAIT_TIME = 5  # Seconds to wait after initiating reboot
    POST_REBOOT_CHECK_DELAY = 2  # Seconds to wait before checking connectivity after reboot
    
    def __init__(self, dish):
        """
        Initialize emergency mode handler.
        
        Args:
            dish: StarlinkDish instance to manage
        """
        self.dish = dish
        self.emergency_active = False
        self.log_entries = []
        
    def log(self, message, level="INFO"):
        """
        Log a message with timestamp.
        
        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR, CRITICAL)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.log_entries.append(log_entry)
        print(log_entry)
        
    def activate(self):
        """Activate emergency mode."""
        self.emergency_active = True
        self.log("Emergency mode ACTIVATED", "CRITICAL")
        
    def deactivate(self):
        """Deactivate emergency mode."""
        self.emergency_active = False
        self.log("Emergency mode DEACTIVATED", "INFO")
        
    def check_connectivity(self):
        """
        Check current connectivity status.
        
        Returns:
            dict: Connectivity assessment results
        """
        self.log("Checking connectivity status...")
        
        try:
            status = self.dish.get_status()
            alerts = self.dish.get_alerts()
            
            # Assess connectivity
            assessment = {
                "operational": status["state"] == "CONNECTED",
                "obstructed": status.get("obstructed", False),
                "signal_quality": "GOOD" if status.get("snr", 0) > self.SNR_THRESHOLD else "POOR",
                "latency": status.get("ping_latency", 0),
                "alerts": alerts,
                "status": status
            }
            
            # Log assessment
            if assessment["operational"]:
                self.log("Connectivity: OPERATIONAL", "INFO")
            else:
                self.log("Connectivity: DEGRADED", "WARNING")
                
            if assessment["obstructed"]:
                self.log("WARNING: Dish is obstructed!", "WARNING")
                
            if alerts:
                self.log(f"Active alerts: {', '.join(alerts)}", "WARNING")
            else:
                self.log("No active alerts", "INFO")
                
            return assessment
            
        except Exception as e:
            self.log(f"Error checking connectivity: {e}", "ERROR")
            return None
    
    def attempt_recovery(self):
        """
        Attempt automatic recovery procedures.
        
        Returns:
            bool: True if recovery was successful
        """
        self.log("Initiating recovery procedures...", "WARNING")
        
        # Check current status
        assessment = self.check_connectivity()
        
        if not assessment:
            self.log("Cannot assess connectivity for recovery", "ERROR")
            return False
        
        # If we have alerts, try reboot
        if assessment.get("alerts"):
            self.log("Attempting dish reboot to clear alerts...", "WARNING")
            try:
                self.dish.reboot()
                self.log(f"Reboot initiated, waiting {self.REBOOT_WAIT_TIME} seconds for dish to come back online...", "INFO")
                time.sleep(self.REBOOT_WAIT_TIME)  # Wait for reboot
                
                # Re-check connectivity
                time.sleep(self.POST_REBOOT_CHECK_DELAY)
                new_assessment = self.check_connectivity()
                
                if new_assessment and new_assessment["operational"]:
                    self.log("Recovery successful!", "INFO")
                    return True
                else:
                    self.log("Recovery incomplete, manual intervention may be required", "WARNING")
                    return False
                    
            except Exception as e:
                self.log(f"Recovery failed: {e}", "ERROR")
                return False
        else:
            self.log("No recovery action needed - connectivity appears stable", "INFO")
            return True
    
    def monitor(self, duration=60, interval=10):
        """
        Monitor connectivity for a specified duration.
        
        Args:
            duration: Total monitoring duration in seconds
            interval: Check interval in seconds
        """
        self.log(f"Starting connectivity monitoring for {duration} seconds (interval: {interval}s)", "INFO")
        
        start_time = time.time()
        check_count = 0
        
        while time.time() - start_time < duration:
            check_count += 1
            self.log(f"--- Monitoring check #{check_count} ---", "INFO")
            
            assessment = self.check_connectivity()
            
            if assessment and not assessment["operational"]:
                self.log("Connectivity degraded during monitoring!", "WARNING")
                if self.emergency_active:
                    self.log("Emergency mode active - attempting recovery...", "CRITICAL")
                    self.attempt_recovery()
            
            # Wait for next check
            time.sleep(interval)
        
        self.log("Monitoring period completed", "INFO")
    
    def get_logs(self):
        """
        Get all log entries.
        
        Returns:
            list: All log entries
        """
        return self.log_entries
    
    def print_summary(self):
        """Print a summary of emergency mode operations."""
        print("\n" + "="*60)
        print("EMERGENCY MODE SUMMARY")
        print("="*60)
        print(f"Total log entries: {len(self.log_entries)}")
        print(f"Emergency mode active: {self.emergency_active}")
        print("\nLog history:")
        for entry in self.log_entries:
            print(entry)
        print("="*60 + "\n")
