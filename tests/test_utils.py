"""
Tests for utility functions.
"""

import pytest
from starlink_connectivity_tools.utils import check_connection, format_speed


class TestCheckConnection:
    """Test cases for check_connection function."""

    def test_check_connection_none(self):
        """Test check_connection with None dish_id."""
        assert check_connection(None) is False

    def test_check_connection_empty_string(self):
        """Test check_connection with empty string."""
        assert check_connection("") is False

    def test_check_connection_invalid_type(self):
        """Test check_connection with invalid type."""
        assert check_connection(12345) is False
        assert check_connection([]) is False
        assert check_connection({}) is False

    def test_check_connection_valid_dish_id(self):
        """Test check_connection with valid dish_id."""
        assert check_connection("DISH-12345") is True
        assert check_connection("ABC") is True


class TestFormatSpeed:
    """Test cases for format_speed function."""

    def test_format_speed_mbps(self):
        """Test format_speed for values in Mbps."""
        assert format_speed(100) == "100.00 Mbps"
        assert format_speed(250.5) == "250.50 Mbps"
        assert format_speed(999.99) == "999.99 Mbps"

    def test_format_speed_gbps(self):
        """Test format_speed for values in Gbps."""
        assert format_speed(1000) == "1.00 Gbps"
        assert format_speed(1500) == "1.50 Gbps"
        assert format_speed(2048) == "2.05 Gbps"

    def test_format_speed_zero(self):
        """Test format_speed with zero."""
        assert format_speed(0) == "0.00 Mbps"

    def test_format_speed_small_value(self):
        """Test format_speed with small decimal values."""
        assert format_speed(0.5) == "0.50 Mbps"
        assert format_speed(1.25) == "1.25 Mbps"

    def test_format_speed_invalid_type(self):
        """Test format_speed with invalid type."""
        with pytest.raises(ValueError, match="Speed must be a number"):
            format_speed("100")
        with pytest.raises(ValueError, match="Speed must be a number"):
            format_speed(None)

    def test_format_speed_negative(self):
        """Test format_speed with negative value."""
        with pytest.raises(ValueError, match="Speed cannot be negative"):
            format_speed(-100)
