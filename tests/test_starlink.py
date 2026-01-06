"""Tests for Starlink connectivity tools."""

import pytest
from datetime import datetime
from starlink_connectivity_tools import (
    StarlinkClient,
    DeviceStatus,
    NetworkStats,
    TelemetryData,
    DeviceLocation,
    WiFiStatus,
    WiFiConfig,
    DishConfig,
    AccountData,
    Alert,
    AlertLevel,
    DeviceState,
)
from starlink_connectivity_tools.client import (
    StarlinkConnectionError,
    StarlinkOperationError,
)


class TestDataModels:
    """Test data model functionality."""
    
    def test_device_status_is_online(self):
        """Test DeviceStatus.is_online() method."""
        status = DeviceStatus(
            state=DeviceState.ONLINE,
            uptime_seconds=1000,
            connected=True,
        )
        assert status.is_online() is True
        
        status_offline = DeviceStatus(
            state=DeviceState.OFFLINE,
            uptime_seconds=0,
            connected=False,
        )
        assert status_offline.is_online() is False
    
    def test_network_stats_is_healthy(self):
        """Test NetworkStats.is_healthy() method."""
        good_stats = NetworkStats(
            download_mbps=100.0,
            upload_mbps=20.0,
            latency_ms=50.0,
            packet_loss_percent=1.0,
            timestamp=datetime.now(),
        )
        assert good_stats.is_healthy() is True
        
        bad_stats = NetworkStats(
            download_mbps=100.0,
            upload_mbps=20.0,
            latency_ms=150.0,
            packet_loss_percent=10.0,
            timestamp=datetime.now(),
        )
        assert bad_stats.is_healthy() is False
    
    def test_telemetry_has_critical_alerts(self):
        """Test TelemetryData.has_critical_alerts() method."""
        critical_alert = Alert(
            level=AlertLevel.CRITICAL,
            message="Critical error",
            timestamp=datetime.now(),
        )
        
        telemetry = TelemetryData(alerts=[critical_alert])
        assert telemetry.has_critical_alerts() is True
        
        warning_alert = Alert(
            level=AlertLevel.WARNING,
            message="Warning",
            timestamp=datetime.now(),
        )
        telemetry_warn = TelemetryData(alerts=[warning_alert])
        assert telemetry_warn.has_critical_alerts() is False
    
    def test_device_location_has_coordinates(self):
        """Test DeviceLocation.has_coordinates() method."""
        location_with_coords = DeviceLocation(
            latitude=37.7749,
            longitude=-122.4194,
        )
        assert location_with_coords.has_coordinates() is True
        
        location_without_coords = DeviceLocation(h3_cell="8c2a1072b181bff")
        assert location_without_coords.has_coordinates() is False
    
    def test_wifi_status_client_count(self):
        """Test WiFiStatus.client_count() method."""
        wifi = WiFiStatus(ssid="TEST", enabled=True, connected_clients=[])
        assert wifi.client_count() == 0
    
    def test_wifi_config_validation(self):
        """Test WiFiConfig validation methods."""
        valid_config = WiFiConfig(
            ssid="ValidSSID",
            password="ValidPassword123",
        )
        assert valid_config.validate_ssid() is True
        assert valid_config.validate_password() is True
        
        invalid_ssid = WiFiConfig(ssid="a" * 40)  # Too long
        assert invalid_ssid.validate_ssid() is False
        
        invalid_password = WiFiConfig(password="short")  # Too short
        assert invalid_password.validate_password() is False
    
    def test_dish_config_is_power_saving(self):
        """Test DishConfig.is_power_saving() method."""
        config = DishConfig(power_save_mode_enabled=True)
        assert config.is_power_saving() is True
        
        config_no_save = DishConfig(power_save_mode_enabled=False, snow_melt_mode_enabled=False)
        assert config_no_save.is_power_saving() is False
    
    def test_account_data_is_near_limit(self):
        """Test AccountData.is_near_limit() method."""
        account = AccountData(
            data_limit_gb=100.0,
            data_used_gb=95.0,
        )
        assert account.is_near_limit(threshold_percent=90.0) is True
        
        account_safe = AccountData(
            data_limit_gb=100.0,
            data_used_gb=50.0,
        )
        assert account_safe.is_near_limit() is False


class TestStarlinkClient:
    """Test StarlinkClient functionality."""
    
    def test_client_initialization_local(self):
        """Test local client initialization."""
        client = StarlinkClient()
        assert client.host == StarlinkClient.DEFAULT_HOST
        assert client.port == StarlinkClient.DEFAULT_PORT
        assert client.use_remote is False
    
    def test_client_initialization_remote(self):
        """Test remote client initialization."""
        client = StarlinkClient(use_remote=True, api_key="test-key")
        assert client.use_remote is True
        assert client.api_key == "test-key"
    
    def test_client_initialization_remote_without_key(self):
        """Test remote client initialization fails without API key."""
        with pytest.raises(ValueError, match="api_key is required"):
            StarlinkClient(use_remote=True)
    
    def test_get_status_without_connection(self):
        """Test get_status fails when not connected."""
        client = StarlinkClient()
        with pytest.raises(StarlinkConnectionError, match="Not connected"):
            client.get_status()
    
    def test_get_network_stats_without_connection(self):
        """Test get_network_stats fails when not connected."""
        client = StarlinkClient()
        with pytest.raises(StarlinkConnectionError, match="Not connected"):
            client.get_network_stats()
    
    def test_get_telemetry_without_connection(self):
        """Test get_telemetry fails when not connected."""
        client = StarlinkClient()
        with pytest.raises(StarlinkConnectionError, match="Not connected"):
            client.get_telemetry()
    
    def test_reboot_dish_without_connection(self):
        """Test reboot_dish fails when not connected."""
        client = StarlinkClient()
        with pytest.raises(StarlinkConnectionError, match="Not connected"):
            client.reboot_dish()
    
    def test_get_account_data_local_connection(self):
        """Test get_account_data fails with local connection."""
        client = StarlinkClient()
        client.connect()
        try:
            with pytest.raises(StarlinkOperationError, match="remote API"):
                client.get_account_data()
        finally:
            client.disconnect()
    
    def test_context_manager(self):
        """Test client context manager."""
        with StarlinkClient() as client:
            # Connection should be established
            assert client._channel is not None
        # Connection should be closed after context
    
    def test_set_wifi_config_validation(self):
        """Test WiFi config validation in set_wifi_config."""
        client = StarlinkClient()
        client.connect()
        
        try:
            # Invalid SSID
            invalid_config = WiFiConfig(ssid="a" * 40)
            with pytest.raises(ValueError, match="SSID must be"):
                client.set_wifi_config(invalid_config)
            
            # Invalid password
            invalid_config = WiFiConfig(password="short")
            with pytest.raises(ValueError, match="Password must be"):
                client.set_wifi_config(invalid_config)
        finally:
            client.disconnect()


class TestEnums:
    """Test enum definitions."""
    
    def test_alert_level_enum(self):
        """Test AlertLevel enum values."""
        assert AlertLevel.INFO.value == "info"
        assert AlertLevel.WARNING.value == "warning"
        assert AlertLevel.ERROR.value == "error"
        assert AlertLevel.CRITICAL.value == "critical"
    
    def test_device_state_enum(self):
        """Test DeviceState enum values."""
        assert DeviceState.ONLINE.value == "online"
        assert DeviceState.OFFLINE.value == "offline"
        assert DeviceState.BOOTING.value == "booting"
        assert DeviceState.SEARCHING.value == "searching"
        assert DeviceState.CONNECTED.value == "connected"
