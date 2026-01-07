"""Unit tests for StarlinkDishClient."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from starlink_connectivity_tools.client import StarlinkDishClient


class TestStarlinkDishClient:
    """Test cases for StarlinkDishClient."""

    def test_default_address(self):
        """Test that default address is set correctly."""
        client = StarlinkDishClient()
        assert client.address == "192.168.100.1:9200"

    def test_custom_address(self):
        """Test that custom address is used."""
        custom_address = "192.168.1.100:9200"
        client = StarlinkDishClient(address=custom_address)
        assert client.address == custom_address

    def test_session_cookie(self):
        """Test that session cookie is stored."""
        cookie = "test-session-cookie"
        client = StarlinkDishClient(session_cookie=cookie)
        assert client.session_cookie == cookie

    def test_timeout_setting(self):
        """Test that timeout is configurable."""
        timeout = 30
        client = StarlinkDishClient(timeout=timeout)
        assert client.timeout == timeout

    @patch("grpc.insecure_channel")
    @patch("grpc.channel_ready_future")
    def test_connect_success(self, mock_ready_future, mock_channel):
        """Test successful connection."""
        # Mock channel ready
        mock_future = Mock()
        mock_future.result.return_value = None
        mock_ready_future.return_value = mock_future

        client = StarlinkDishClient()
        client.connect()

        mock_channel.assert_called_once()
        assert client._channel is not None

    @patch("grpc.insecure_channel")
    @patch("grpc.channel_ready_future")
    def test_connect_timeout(self, mock_ready_future, mock_channel):
        """Test connection timeout."""
        # Mock timeout
        mock_future = Mock()
        mock_future.result.side_effect = Exception("Timeout")
        mock_ready_future.return_value = mock_future

        client = StarlinkDishClient()

        with pytest.raises(ConnectionError):
            client.connect()

    def test_close(self):
        """Test closing the channel."""
        client = StarlinkDishClient()
        mock_channel = Mock()
        client._channel = mock_channel

        client.close()

        mock_channel.close.assert_called_once()
        assert client._channel is None

    @patch("grpc.insecure_channel")
    @patch("grpc.channel_ready_future")
    def test_context_manager(self, mock_ready_future, mock_channel):
        """Test using client as context manager."""
        mock_future = Mock()
        mock_future.result.return_value = None
        mock_ready_future.return_value = mock_future

        mock_ch = Mock()
        mock_channel.return_value = mock_ch

        with StarlinkDishClient() as client:
            assert client._channel is not None

        mock_ch.close.assert_called_once()

    def test_get_status_not_implemented(self):
        """Test that get_status raises NotImplementedError without proto files."""
        client = StarlinkDishClient()

        with pytest.raises(NotImplementedError):
            client.get_status()

    def test_get_network_stats_not_implemented(self):
        """Test that get_network_stats raises NotImplementedError without proto files."""
        client = StarlinkDishClient()

        with pytest.raises(NotImplementedError):
            client.get_network_stats()

    def test_get_telemetry_not_implemented(self):
        """Test that get_telemetry raises NotImplementedError without proto files."""
        client = StarlinkDishClient()

        with pytest.raises(NotImplementedError):
            client.get_telemetry()

    def test_reboot_not_implemented(self):
        """Test that reboot raises NotImplementedError without proto files."""
        client = StarlinkDishClient()

        with pytest.raises(NotImplementedError):
            client.reboot()

    def test_set_configuration_not_implemented(self):
        """Test that set_configuration raises NotImplementedError without proto files."""
        client = StarlinkDishClient()

        with pytest.raises(NotImplementedError):
            client.set_configuration({})
