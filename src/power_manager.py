"""
Power management for energy-constrained crisis scenarios
"""
import time
import logging
import threading
from typing import Dict
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class PowerMode(Enum):
    """Power management modes"""
    NORMAL = "normal"
    CONSERVATION = "conservation"
    CRISIS = "crisis"
    SURVIVAL = "survival"


@dataclass
class PowerProfile:
    """Power consumption profile for a component"""
    component: str
    normal_power: float  # Watts
    conservation_power: float  # Watts
    crisis_power: float  # Watts
    sleep_power: float  # Watts
    can_sleep: bool = True


class PowerManager:
    """Manages power consumption for satellite connectivity equipment"""
    
    def __init__(self, total_battery_capacity: float = 500.0):  # Wh
        self.battery_level = total_battery_capacity
        self.battery_capacity = total_battery_capacity
        self.power_mode = PowerMode.NORMAL
        self.estimated_runtime = 0.0
        self.scheduled_sleep = False
        
        # Component power profiles
        self.power_profiles: Dict[str, PowerProfile] = {
            'satellite_modem': PowerProfile(
                component='satellite_modem',
                normal_power=60.0,
                conservation_power=40.0,
                crisis_power=20.0,
                sleep_power=5.0
            ),
            'router': PowerProfile(
                component='router',
                normal_power=10.0,
                conservation_power=7.0,
                crisis_power=5.0,
                sleep_power=2.0
            ),
            'cellular_modem': PowerProfile(
                component='cellular_modem',
                normal_power=8.0,
                conservation_power=6.0,
                crisis_power=4.0,
                sleep_power=1.0
            ),
            'compute_unit': PowerProfile(
                component='compute_unit',
                normal_power=25.0,
                conservation_power=15.0,
                crisis_power=10.0,
                sleep_power=3.0
            )
        }
        
        # Active components
        self.active_components = set(self.power_profiles.keys())
        
        # Update estimated runtime
        self._update_estimated_runtime()
    
    def set_power_mode(self, mode: PowerMode):
        """Set power management mode"""
        self.power_mode = mode
        logger.info(f"Power mode set to: {mode.value}")
        
        # Apply power settings for each component
        for component in self.active_components:
            self._apply_component_power(component)
        
        self._update_estimated_runtime()
    
    def _apply_component_power(self, component: str):
        """Apply power settings for a specific component"""
        if component not in self.power_profiles:
            return
        
        profile = self.power_profiles[component]
        
        # In real implementation, this would send commands to hardware
        # to adjust power settings
        
        logger.debug(f"Applied {self.power_mode.value} power settings to {component}")
    
    def enable_component(self, component: str):
        """Enable a specific component"""
        if component in self.power_profiles:
            self.active_components.add(component)
            self._apply_component_power(component)
            self._update_estimated_runtime()
            logger.info(f"Enabled component: {component}")
    
    def disable_component(self, component: str):
        """Disable a specific component (put to sleep if possible)"""
        if component in self.power_profiles and component in self.active_components:
            self.active_components.remove(component)
            logger.info(f"Disabled component: {component}")
            self._update_estimated_runtime()
    
    def get_component_power(self, component: str) -> float:
        """Get current power consumption for a component"""
        if component not in self.power_profiles:
            return 0.0
        
        profile = self.power_profiles[component]
        
        if component not in self.active_components:
            return profile.sleep_power
        
        # Return power based on current mode
        if self.power_mode == PowerMode.NORMAL:
            return profile.normal_power
        elif self.power_mode == PowerMode.CONSERVATION:
            return profile.conservation_power
        elif self.power_mode == PowerMode.CRISIS:
            return profile.crisis_power
        elif self.power_mode == PowerMode.SURVIVAL:
            return profile.sleep_power
        
        return profile.normal_power
    
    def get_total_power_consumption(self) -> float:
        """Calculate total power consumption"""
        total = 0.0
        for component in self.power_profiles:
            total += self.get_component_power(component)
        return total
    
    def _update_estimated_runtime(self):
        """Update estimated battery runtime"""
        consumption = self.get_total_power_consumption()
        
        if consumption > 0:
            self.estimated_runtime = self.battery_level / consumption
        else:
            self.estimated_runtime = float('inf')
    
    def update_battery_level(self, level: float):
        """Update current battery level"""
        self.battery_level = max(0, min(level, self.battery_capacity))
        self._update_estimated_runtime()
    
    def schedule_sleep_cycle(self, 
                            active_duration: int = 300,  # 5 minutes
                            sleep_duration: int = 1800):  # 30 minutes
        """
        Schedule periodic sleep cycles to conserve power
        
        Args:
            active_duration: Time active in seconds
            sleep_duration: Time sleeping in seconds
        """
        self.scheduled_sleep = True
        
        def sleep_cycle():
            while self.scheduled_sleep:
                # Stay active
                logger.info(f"Active for {active_duration} seconds")
                time.sleep(active_duration)
                
                # Store current mode before sleeping
                previous_mode = self.power_mode
                
                # Sleep
                logger.info(f"Sleeping for {sleep_duration} seconds")
                self.set_power_mode(PowerMode.SURVIVAL)
                time.sleep(sleep_duration)
                
                # Wake up and restore previous mode
                logger.info("Waking up")
                self.set_power_mode(previous_mode)
        
        thread = threading.Thread(target=sleep_cycle, daemon=True)
        thread.start()
        
        logger.info(f"Scheduled sleep cycle: {active_duration}s active, "
                   f"{sleep_duration}s sleep")
    
    def optimize_for_battery_life(self, 
                                 target_runtime_hours: float = 24.0):
        """
        Optimize power settings to achieve target battery runtime
        """
        current_runtime_hours = self.estimated_runtime
        
        if current_runtime_hours >= target_runtime_hours:
            logger.info(f"Current runtime {current_runtime_hours:.1f}h "
                       f"already meets target {target_runtime_hours}h")
            return
        
        # Calculate required power reduction
        required_power = self.battery_level / target_runtime_hours
        current_power = self.get_total_power_consumption()
        
        if required_power >= current_power:
            logger.warning(f"Cannot achieve target runtime {target_runtime_hours}h "
                          f"with current power {current_power:.1f}W "
                          f"(need {required_power:.1f}W)")
            return
        
        # Adjust power mode based on requirements
        power_reduction = current_power - required_power
        power_reduction_percent = (power_reduction / current_power) * 100
        
        if power_reduction_percent <= 20:
            self.set_power_mode(PowerMode.CONSERVATION)
        elif power_reduction_percent <= 50:
            self.set_power_mode(PowerMode.CRISIS)
        else:
            self.set_power_mode(PowerMode.SURVIVAL)
            # Consider disabling non-essential components
            non_essential = ['compute_unit', 'cellular_modem']
            for component in non_essential:
                self.disable_component(component)
        
        logger.info(f"Optimized for {target_runtime_hours}h runtime. "
                   f"New estimated runtime: {self.estimated_runtime:.1f}h")
    
    def get_power_report(self) -> Dict:
        """Generate power consumption report"""
        battery_percent = (self.battery_level / self.battery_capacity * 100 
                          if self.battery_capacity > 0 else 0.0)
        
        report = {
            'power_mode': self.power_mode.value,
            'battery_level_wh': self.battery_level,
            'battery_capacity_wh': self.battery_capacity,
            'battery_percent': battery_percent,
            'estimated_runtime_hours': self.estimated_runtime,
            'total_power_consumption_w': self.get_total_power_consumption(),
            'active_components': list(self.active_components),
            'scheduled_sleep': self.scheduled_sleep,
            'timestamp': time.time()
        }
        
        # Add component details
        report['components'] = {}
        for component, profile in self.power_profiles.items():
            report['components'][component] = {
                'current_power_w': self.get_component_power(component),
                'is_active': component in self.active_components,
                'can_sleep': profile.can_sleep
            }
        
        return report
