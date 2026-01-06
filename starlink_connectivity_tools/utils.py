"""
Utility functions for Starlink connectivity tools.
"""


def check_connection(dish_id=None):
    """
    Check if a connection to Starlink is possible.

    Args:
        dish_id: Optional dish identifier

    Returns:
        bool: True if connection check passes
    """
    # Simple validation check
    if dish_id is None:
        return False
    if not isinstance(dish_id, str):
        return False
    if len(dish_id) == 0:
        return False
    return True


def format_speed(speed_mbps):
    """
    Format speed value in Mbps to a readable string.

    Args:
        speed_mbps: Speed value in Mbps

    Returns:
        str: Formatted speed string
    """
    if not isinstance(speed_mbps, (int, float)):
        raise ValueError("Speed must be a number")
    
    if speed_mbps < 0:
        raise ValueError("Speed cannot be negative")
    
    if speed_mbps >= 1000:
        return f"{speed_mbps / 1000:.2f} Gbps"
    return f"{speed_mbps:.2f} Mbps"
