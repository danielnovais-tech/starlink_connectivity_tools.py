"""
Power Manager
Manages power consumption and battery optimization
"""

import logging
from enum import Enum
from typing import Dict

logger = logging.getLogger(__name__)


class PowerMode(Enum):
    """Power consumption modes"""
    NORMAL = "normal"           # Full power operation
    EFFICIENT = "efficient"     # Balanced power/performance
    CONSERVATION = "conservation"  # Reduced power consumption
    CRISIS = "crisis"           # Maximum battery preservation
    SURVIVAL = "survival"       # Absolute minimum power


class PowerManager:
    """
    Manages power consumption and battery optimization
    """
    
    def __init__(self, total_battery_capacity: float = 500.0):
        """
        Initialize power manager
        
        Args:
            total_battery_capacity: Total battery capacity in Wh
        """
        self.total_battery_capacity = total_battery_capacity
        self.current_battery_capacity = total_battery_capacity
        self.power_mode = PowerMode.NORMAL
        
        # Power consumption rates (watts) by mode
        self.power_consumption_rates = {
            PowerMode.NORMAL: 50.0,
            PowerMode.EFFICIENT: 35.0,
            PowerMode.CONSERVATION: 20.0,
            PowerMode.CRISIS: 10.0,
            PowerMode.SURVIVAL: 5.0
        }
        
        logger.info(f"PowerManager initialized with {total_battery_capacity} Wh capacity")
    
    def set_power_mode(self, mode: PowerMode):
        """
        Set power consumption mode
        
        Args:
            mode: Power mode to set
        """
        old_mode = self.power_mode
        self.power_mode = mode
        
        logger.info(f"Power mode changed: {old_mode.value} -> {mode.value}")
        logger.info(f"Power consumption: {self.power_consumption_rates[mode]} W")
    
    def get_current_power_consumption(self) -> float:
        """
        Get current power consumption
        
        Returns:
            Current power consumption in watts
        """
        return self.power_consumption_rates[self.power_mode]
    
    def get_estimated_runtime(self) -> float:
        """
        Get estimated runtime in hours
        
        Returns:
            Estimated runtime in hours
        """
        if self.current_battery_capacity <= 0:
            return 0.0
        
        power_consumption = self.get_current_power_consumption()
        
        if power_consumption == 0:
            return float('inf')
        
        return self.current_battery_capacity / power_consumption
    
    def optimize_for_battery_life(self, target_runtime_hours: float):
        """
        Optimize power mode to achieve target runtime
        
        Args:
            target_runtime_hours: Target runtime in hours
        """
        logger.info(f"Optimizing for {target_runtime_hours}h runtime")
        
        current_runtime = self.get_estimated_runtime()
        
        if current_runtime >= target_runtime_hours:
            logger.info(f"Current runtime {current_runtime:.1f}h meets target")
            return
        
        # Find most efficient mode that meets target
        for mode in [PowerMode.EFFICIENT, PowerMode.CONSERVATION, PowerMode.CRISIS, PowerMode.SURVIVAL]:
            test_consumption = self.power_consumption_rates[mode]
            test_runtime = self.current_battery_capacity / test_consumption
            
            if test_runtime >= target_runtime_hours:
                self.set_power_mode(mode)
                logger.info(f"Set power mode to {mode.value} for {test_runtime:.1f}h runtime")
                return
        
        # If we get here, even survival mode won't meet target
        self.set_power_mode(PowerMode.SURVIVAL)
        logger.warning(f"Cannot meet target runtime, using SURVIVAL mode: {self.get_estimated_runtime():.1f}h")
    
    def consume_power(self, hours: float):
        """
        Simulate power consumption over time
        
        Args:
            hours: Time period in hours
        """
        power_consumed = self.get_current_power_consumption() * hours
        self.current_battery_capacity -= power_consumed
        
        if self.current_battery_capacity < 0:
            self.current_battery_capacity = 0
    
    def get_power_report(self) -> Dict:
        """
        Get power status report
        
        Returns:
            Dictionary with power information
        """
        return {
            'power_mode': self.power_mode.value,
            'battery_capacity': self.current_battery_capacity,
            'total_capacity': self.total_battery_capacity,
            'battery_percent': (self.current_battery_capacity / self.total_battery_capacity) * 100,
            'power_consumption': self.get_current_power_consumption(),
            'estimated_runtime_hours': self.get_estimated_runtime()
        }
