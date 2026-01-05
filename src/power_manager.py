"""
Power Manager Module

Manages power consumption and enables low-power modes for Starlink equipment.
"""


class PowerManager:
    """Manages power consumption for Starlink equipment."""

    def __init__(self):
        """Initialize the PowerManager."""
        self.power_mode = "normal"
        self.low_power_enabled = False
        self.power_consumption = 100  # Percentage

    def enable_low_power_mode(self):
        """
        Enable low power consumption mode.

        Returns:
            bool: True if low power mode enabled successfully
        """
        self.low_power_enabled = True
        self.power_mode = "low_power"
        self.power_consumption = 50  # Reduced to 50%
        return True

    def disable_low_power_mode(self):
        """
        Disable low power consumption mode.

        Returns:
            bool: True if low power mode disabled successfully
        """
        self.low_power_enabled = False
        self.power_mode = "normal"
        self.power_consumption = 100
        return True

    def set_power_mode(self, mode):
        """
        Set power consumption mode.

        Args:
            mode: Power mode ('normal', 'low_power', 'high_performance')

        Returns:
            bool: True if mode set successfully
        """
        valid_modes = ["normal", "low_power", "high_performance"]
        if mode not in valid_modes:
            return False

        self.power_mode = mode
        if mode == "low_power":
            self.low_power_enabled = True
            self.power_consumption = 50
        elif mode == "high_performance":
            self.low_power_enabled = False
            self.power_consumption = 120
        else:  # normal
            self.low_power_enabled = False
            self.power_consumption = 100

        return True

    def get_power_status(self):
        """
        Get current power consumption status.

        Returns:
            dict: Power status information
        """
        return {
            "power_mode": self.power_mode,
            "low_power_enabled": self.low_power_enabled,
            "power_consumption": self.power_consumption,
        }

    def estimate_runtime(self, battery_capacity):
        """
        Estimate runtime based on current power consumption.

        Args:
            battery_capacity: Battery capacity in Wh

        Returns:
            float: Estimated runtime in hours
        """
        # Simplified calculation (assuming base consumption of 100W at 100%)
        base_consumption = 100  # Watts
        actual_consumption = base_consumption * (self.power_consumption / 100)
        if actual_consumption == 0:
            return float('inf')
        return battery_capacity / actual_consumption
