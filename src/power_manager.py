"""
Power Manager

Manages power consumption for network equipment.
Implements power-saving modes and monitors energy usage.
"""

import logging
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class PowerMode(Enum):
    """Power consumption modes."""
    NORMAL = "normal"
    ECO = "eco"
    LOW_POWER = "low_power"
    EMERGENCY = "emergency"


@dataclass
class PowerProfile:
    """Power consumption profile."""
    mode: PowerMode
    max_power_watts: float
    features_enabled: list
    description: str


class PowerManager:
    """Manages power consumption for network equipment."""
    
    def __init__(self):
        """Initialize the PowerManager."""
        self.current_mode = PowerMode.NORMAL
        self.current_power_watts = 0.0
        self.profiles = self._initialize_profiles()
        self.power_history = []
        
    def _initialize_profiles(self) -> Dict[PowerMode, PowerProfile]:
        """
        Initialize power profiles.
        
        Returns:
            dict: Available power profiles
        """
        return {
            PowerMode.NORMAL: PowerProfile(
                mode=PowerMode.NORMAL,
                max_power_watts=100.0,
                features_enabled=["full_bandwidth", "all_radios", "auto_updates"],
                description="Normal operation mode with all features enabled"
            ),
            PowerMode.ECO: PowerProfile(
                mode=PowerMode.ECO,
                max_power_watts=60.0,
                features_enabled=["reduced_bandwidth", "primary_radio", "scheduled_updates"],
                description="Eco mode with reduced power consumption"
            ),
            PowerMode.LOW_POWER: PowerProfile(
                mode=PowerMode.LOW_POWER,
                max_power_watts=30.0,
                features_enabled=["minimal_bandwidth", "essential_only"],
                description="Low power mode for extended operation"
            ),
            PowerMode.EMERGENCY: PowerProfile(
                mode=PowerMode.EMERGENCY,
                max_power_watts=15.0,
                features_enabled=["emergency_only"],
                description="Emergency mode for critical communications only"
            )
        }
    
    def set_power_mode(self, mode: PowerMode) -> bool:
        """
        Set the power consumption mode.
        
        Args:
            mode: Power mode to activate
            
        Returns:
            bool: True if mode was set successfully
        """
        if mode not in self.profiles:
            logger.error(f"Invalid power mode: {mode}")
            return False
        
        profile = self.profiles[mode]
        logger.info(f"Setting power mode to {mode.value}: {profile.description}")
        
        self.current_mode = mode
        self._apply_power_profile(profile)
        
        return True
    
    def _apply_power_profile(self, profile: PowerProfile) -> None:
        """
        Apply power profile settings.
        
        Args:
            profile: Power profile to apply
        """
        logger.info(f"Applying power profile: {profile.mode.value}")
        logger.info(f"Max power: {profile.max_power_watts}W")
        logger.info(f"Enabled features: {', '.join(profile.features_enabled)}")
        
        # Simulate applying power settings
        self.current_power_watts = profile.max_power_watts * 0.7  # Typical usage
    
    def get_power_status(self) -> Dict[str, Any]:
        """
        Get current power consumption status.
        
        Returns:
            dict: Power status information
        """
        profile = self.profiles[self.current_mode]
        
        return {
            "current_mode": self.current_mode.value,
            "current_power_watts": self.current_power_watts,
            "max_power_watts": profile.max_power_watts,
            "power_efficiency": (1 - self.current_power_watts / profile.max_power_watts) * 100,
            "features_enabled": profile.features_enabled
        }
    
    def estimate_runtime(self, battery_capacity_wh: float) -> float:
        """
        Estimate remaining runtime on battery.
        
        Args:
            battery_capacity_wh: Battery capacity in watt-hours
            
        Returns:
            float: Estimated runtime in hours
        """
        if self.current_power_watts <= 0:
            return float('inf')
        
        runtime_hours = battery_capacity_wh / self.current_power_watts
        logger.info(f"Estimated runtime: {runtime_hours:.2f} hours at {self.current_power_watts}W")
        
        return runtime_hours
    
    def optimize_for_battery(self, target_runtime_hours: float, battery_capacity_wh: float) -> PowerMode:
        """
        Optimize power mode to achieve target runtime on battery.
        
        Args:
            target_runtime_hours: Desired runtime in hours
            battery_capacity_wh: Available battery capacity in watt-hours
            
        Returns:
            PowerMode: Recommended power mode
        """
        required_power = battery_capacity_wh / target_runtime_hours
        logger.info(f"Required power for {target_runtime_hours}h runtime: {required_power:.2f}W")
        
        # Find the most feature-rich mode that meets power requirement
        for mode in [PowerMode.NORMAL, PowerMode.ECO, PowerMode.LOW_POWER, PowerMode.EMERGENCY]:
            profile = self.profiles[mode]
            if profile.max_power_watts <= required_power:
                logger.info(f"Recommended power mode: {mode.value}")
                return mode
        
        # If even emergency mode is too high, return emergency anyway
        logger.warning("Target runtime not achievable, using emergency mode")
        return PowerMode.EMERGENCY
    
    def get_power_recommendations(self) -> list:
        """
        Get power optimization recommendations.
        
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        if self.current_mode == PowerMode.NORMAL:
            recommendations.append("Consider switching to ECO mode to reduce power consumption")
        
        if self.current_power_watts > self.profiles[self.current_mode].max_power_watts * 0.9:
            recommendations.append("Power usage is high. Consider reducing active features")
        
        return recommendations
    
    def log_power_usage(self) -> None:
        """Log current power usage to history."""
        self.power_history.append({
            "timestamp": time.time(),
            "mode": self.current_mode.value,
            "power_watts": self.current_power_watts
        })
        
        # Keep only last 100 entries
        if len(self.power_history) > 100:
            self.power_history = self.power_history[-100:]


import time
