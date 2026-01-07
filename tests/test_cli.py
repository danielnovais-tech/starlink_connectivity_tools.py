"""
Unit tests for Starlink Monitor CLI
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.starlink_cli import StarlinkCLI, setup_logging
from src.starlink_monitor import StarlinkMetrics


class TestStarlinkCLI(unittest.TestCase):
    """Test cases for StarlinkCLI"""

    def setUp(self):
        """Setup test fixtures"""
        # Create CLI with mocked dependencies
        with patch("cli.starlink_cli.StarlinkMonitor"), patch(
            "cli.starlink_cli.SatelliteConnectionManager"
        ), patch("cli.starlink_cli.Config"):
            self.cli = StarlinkCLI(host="192.168.100.1")

    def test_cli_initialization(self):
        """Test CLI initialization"""
        self.assertIsNotNone(self.cli)
        self.assertIn("red", self.cli.colors)
        self.assertIn("green", self.cli.colors)

    def test_colorize(self):
        """Test text colorization"""
        text = "Test"
        colored = self.cli.colorize(text, "red")
        self.assertIn(text, colored)
        self.assertIn("\033[91m", colored)

    def test_colorize_invalid_color(self):
        """Test colorization with invalid color"""
        text = "Test"
        result = self.cli.colorize(text, "invalid")
        self.assertEqual(result, text)

    @patch("builtins.print")
    def test_print_status_success(self, mock_print):
        """Test print_status with successful metrics retrieval"""
        mock_metrics = StarlinkMetrics(
            timestamp=1234567890.0,
            status="online",
            satellites_connected=8,
            download_speed=150.5,
            upload_speed=25.3,
            latency=35.2,
            packet_loss=0.5,
            signal_strength=-85.5,
            snr=12.5,
            azimuth=180.0,
            elevation=45.0,
            obstruction_percent=2.1,
            dish_power_usage=85.0,
            dish_temp=42.5,
            router_temp=38.0,
            boot_count=5,
        )

        self.cli.monitor.get_metrics = Mock(return_value=mock_metrics)
        self.cli.monitor.thresholds = {
            "min_download_speed": 25.0,
            "max_latency": 100.0,
            "max_packet_loss": 5.0,
            "max_obstruction": 10.0,
        }

        self.cli.print_status()
        self.assertTrue(mock_print.called)
        self.cli.monitor.get_metrics.assert_called_once()

    @patch("builtins.print")
    def test_print_status_failure(self, mock_print):
        """Test print_status when metrics retrieval fails"""
        self.cli.monitor.get_metrics = Mock(return_value=None)
        self.cli.print_status()
        self.assertTrue(mock_print.called)

    @patch("builtins.input", return_value="yes")
    @patch("builtins.print")
    def test_reboot_dish_confirmed(self, mock_print, mock_input):
        """Test reboot_dish with user confirmation"""
        self.cli.monitor.reboot_dish = Mock(return_value=True)
        self.cli.reboot_dish()
        self.cli.monitor.reboot_dish.assert_called_once()

    @patch("builtins.input", return_value="no")
    @patch("builtins.print")
    def test_reboot_dish_cancelled(self, mock_print, mock_input):
        """Test reboot_dish with user cancellation"""
        self.cli.monitor.reboot_dish = Mock(return_value=True)
        self.cli.reboot_dish()
        self.cli.monitor.reboot_dish.assert_not_called()

    @patch("builtins.open", create=True)
    @patch("json.dump")
    @patch("builtins.print")
    def test_export_data(self, mock_print, mock_json_dump, mock_open):
        """Test export_data"""
        mock_report = {"status": "ok", "samples": 10}
        self.cli.monitor.get_performance_report = Mock(return_value=mock_report)

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        self.cli.export_data("test.json", hours=12)
        self.cli.monitor.get_performance_report.assert_called_once_with(hours=12)
        mock_open.assert_called_once_with("test.json", "w")


if __name__ == "__main__":
    unittest.main()
