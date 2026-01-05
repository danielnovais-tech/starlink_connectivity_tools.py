"""
Data models for Starlink connectivity tools.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DeviceState(Enum):
    """Device operational states."""
    ONLINE = "online"
    OFFLINE = "offline"
    BOOTING = "booting"
    SEARCHING = "searching"
    CONNECTED = "connected"


@dataclass
class Alert:
    """Represents a device alert."""
    level: AlertLevel
    message: str
    timestamp: datetime
    code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class DeviceStatus:
    """Current status of the Starlink device."""
    state: DeviceState
    uptime_seconds: int
    connected: bool
    alerts: List[Alert] = field(default_factory=list)
    hardware_version: Optional[str] = None
    software_version: Optional[str] = None
    id: Optional[str] = None
    timestamp: Optional[datetime] = None
    
    def is_online(self) -> bool:
        """Check if device is online."""
        return self.state == DeviceState.ONLINE and self.connected


@dataclass
class NetworkStats:
    """Network performance statistics."""
    download_mbps: float
    upload_mbps: float
    latency_ms: float
    packet_loss_percent: float
    timestamp: datetime
    ping_drop_rate: Optional[float] = None
    obstructions_percent: Optional[float] = None
    downlink_throughput_bps: Optional[float] = None
    uplink_throughput_bps: Optional[float] = None
    
    def is_healthy(self, max_latency_ms: float = 100, max_packet_loss: float = 5.0) -> bool:
        """Check if network performance is within acceptable thresholds."""
        return (
            self.latency_ms <= max_latency_ms and
            self.packet_loss_percent <= max_packet_loss
        )


@dataclass
class TelemetryData:
    """Device telemetry including alerts, errors, and warnings."""
    alerts: List[Alert] = field(default_factory=list)
    temperature_celsius: Optional[float] = None
    power_input_watts: Optional[float] = None
    uptime_seconds: Optional[int] = None
    timestamp: Optional[datetime] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def has_critical_alerts(self) -> bool:
        """Check if there are any critical alerts."""
        return any(alert.level == AlertLevel.CRITICAL for alert in self.alerts)
    
    def get_alerts_by_level(self, level: AlertLevel) -> List[Alert]:
        """Get all alerts of a specific level."""
        return [alert for alert in self.alerts if alert.level == level]


@dataclass
class DeviceLocation:
    """Device geographical location."""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude_meters: Optional[float] = None
    h3_cell: Optional[str] = None  # H3 geospatial index for remote location
    is_precise: bool = False  # True for local, False for remote
    
    def has_coordinates(self) -> bool:
        """Check if precise coordinates are available."""
        return self.latitude is not None and self.longitude is not None


@dataclass
class WiFiClient:
    """Information about a connected WiFi client."""
    mac_address: str
    ip_address: Optional[str] = None
    hostname: Optional[str] = None
    signal_strength: Optional[int] = None
    connected_seconds: Optional[int] = None


@dataclass
class WiFiStatus:
    """Current WiFi status and information."""
    ssid: str
    enabled: bool
    channel: Optional[int] = None
    connected_clients: List[WiFiClient] = field(default_factory=list)
    signal_strength: Optional[int] = None
    is_5ghz: Optional[bool] = None
    is_2_4ghz: Optional[bool] = None
    
    def client_count(self) -> int:
        """Get number of connected clients."""
        return len(self.connected_clients)


@dataclass
class WiFiConfig:
    """WiFi configuration settings."""
    ssid: Optional[str] = None
    password: Optional[str] = None
    bypass_mode_enabled: Optional[bool] = None
    is_guest_enabled: Optional[bool] = None
    guest_ssid: Optional[str] = None
    guest_password: Optional[str] = None
    channel_2_4ghz: Optional[int] = None
    channel_5ghz: Optional[int] = None
    
    def validate_ssid(self) -> bool:
        """Validate SSID length."""
        if self.ssid is None:
            return True
        return 1 <= len(self.ssid) <= 32
    
    def validate_password(self) -> bool:
        """Validate password length."""
        if self.password is None:
            return True
        return 8 <= len(self.password) <= 63


@dataclass
class DishConfig:
    """Dish configuration settings."""
    snow_melt_mode_enabled: Optional[bool] = None
    power_save_mode_enabled: Optional[bool] = None
    stow_requested: Optional[bool] = None
    location_request_mode: Optional[str] = None
    
    def is_power_saving(self) -> bool:
        """Check if any power saving features are enabled."""
        return (
            self.power_save_mode_enabled is True or
            (self.snow_melt_mode_enabled is False and self.power_save_mode_enabled is not False)
        )


@dataclass
class AccountData:
    """Basic account information (remote only)."""
    service_line_number: Optional[str] = None
    account_number: Optional[str] = None
    active_subscription: bool = False
    data_limit_gb: Optional[float] = None
    data_used_gb: Optional[float] = None
    
    def is_near_limit(self, threshold_percent: float = 90.0) -> bool:
        """Check if data usage is near the limit."""
        if self.data_limit_gb is None or self.data_used_gb is None:
            return False
        usage_percent = (self.data_used_gb / self.data_limit_gb) * 100
        return usage_percent >= threshold_percent


@dataclass
class HistoricalData:
    """Historical data point for status and network stats."""
    timestamp: datetime
    status: Optional[DeviceStatus] = None
    network_stats: Optional[NetworkStats] = None
