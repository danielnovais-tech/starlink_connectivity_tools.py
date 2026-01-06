"""
Power Manager
Manages power consumption and battery optimization
"""

import logging
from typing import Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)


class PowerMode(Enum):
    """Power consumption modes"""
    NORMAL = "normal"
    ECONOMY = "economy"
    CRISIS = "crisis"
    SURVIVAL = "survival"


class PowerManager:
    """Manages power consumption and battery life"""
    
    def __init__(self, total_battery_capacity: float = 1000.0):
        self.total_battery_capacity = total_battery_capacity
        self.current_battery = total_battery_capacity
        self.power_mode = PowerMode.NORMAL
        self.sleep_cycle_active = False
        self.sleep_config = {}
        self.target_runtime_hours = None
        
        logger.info(f"PowerManager initialized with {total_battery_capacity}Wh capacity")
    
    def set_power_mode(self, mode: PowerMode):
        """Set the power consumption mode"""
        self.power_mode = mode
        logger.info(f"Power mode set to {mode.value}")
    
    def schedule_sleep_cycle(self, active_duration_seconds: int, sleep_duration_seconds: int):
        """Schedule sleep/wake cycles to conserve power
        
        :param active_duration_seconds: Time in seconds to remain active before sleeping.
        :param sleep_duration_seconds: Time in seconds to remain in sleep mode.
        """
        self.sleep_cycle_active = True
        self.sleep_config = {
            'active_duration': active_duration_seconds,
            'sleep_duration': sleep_duration_seconds
        }
        logger.info(f"Sleep cycle scheduled: {active_duration_seconds}s active, {sleep_duration_seconds}s sleep")
    
    def optimize_for_battery_life(self, target_runtime_hours: int):
        """Optimize power consumption for target runtime"""
        self.target_runtime_hours = target_runtime_hours
        logger.info(f"Optimizing for {target_runtime_hours} hours runtime")
        # In a real implementation, would adjust power settings
    
    def get_power_report(self) -> Dict[str, Any]:
        """Get power status report"""
        return {
            'total_capacity': self.total_battery_capacity,
            'current_battery': self.current_battery,
            'battery_percentage': (self.current_battery / self.total_battery_capacity) * 100,
            'power_mode': self.power_mode.value,
            'sleep_cycle_active': self.sleep_cycle_active,
            'sleep_config': self.sleep_config,
            'target_runtime_hours': self.target_runtime_hours
        }
