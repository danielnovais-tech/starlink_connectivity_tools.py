#!/usr/bin/env python3
"""Example usage of the starlink-client library."""

from starlink_client import StarlinkClient

# Create a client with default settings (connects to local Starlink dish)
client = StarlinkClient()  # Local connection

# Get network statistics
stats = client.get_network_stats()
print(f"Download: {stats.download_speed} Mbps, Latency: {stats.latency} ms")
print(f"Upload: {stats.upload_speed} Mbps")
print(f"Connected: {stats.connected}")
print(f"Uptime: {stats.uptime} seconds")
print(f"Obstruction: {stats.obstruction_percentage}%")

# Reboot the dish (commented out for safety)
# client.reboot_dish()
# print("Dish reboot initiated")
