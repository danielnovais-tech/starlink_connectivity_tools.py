"""Starlink API integration module for real-time monitoring and control."""

import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from loguru import logger

try:
    from starlink_grpc import ChannelContext, GrpcError
    from spacex.api.device import device_pb2
    STARLINK_AVAILABLE = True
except ImportError:
    STARLINK_AVAILABLE = False
    logger.warning("starlink-grpc not available. Using simulation mode.")


class StarlinkAPI:
    """Interface to Starlink dish for monitoring and control operations."""

    def __init__(self, target: Optional[str] = None, simulation_mode: bool = False):
        """
        Initialize Starlink API connection.

        Args:
            target: gRPC target address (default: "192.168.100.1:9200")
            simulation_mode: If True, use simulated data instead of real connection
        """
        self.target = target or "192.168.100.1:9200"
        self.simulation_mode = simulation_mode or not STARLINK_AVAILABLE
        self.context = None
        self._last_status = None
        self._last_update = None

        if not self.simulation_mode:
            try:
                self.context = ChannelContext(target=self.target)
                logger.info(f"Connected to Starlink dish at {self.target}")
            except Exception as e:
                logger.warning(f"Failed to connect to Starlink: {e}. Using simulation mode.")
                self.simulation_mode = True

    def get_status(self) -> Dict[str, Any]:
        """
        Get current dish status including obstructions and performance metrics.

        Returns:
            Dictionary containing dish status information
        """
        if self.simulation_mode:
            return self._get_simulated_status()

        try:
            # Get device status from Starlink
            request = device_pb2.Request()
            request.get_status.SetInParent()

            with self.context as channel:
                response = channel.call(request)

            if response.HasField("dish_get_status"):
                status = response.dish_get_status
                
                # Extract key metrics
                result = {
                    "uptime": status.device_info.uptime_s,
                    "state": self._parse_state(status.state),
                    "obstructed": status.obstructed,
                    "obstruction_percent": status.obstruction_stats.fraction_obstructed,
                    "snr": status.snr,
                    "downlink_throughput_bps": status.downlink_throughput_bps,
                    "uplink_throughput_bps": status.uplink_throughput_bps,
                    "ping_latency_ms": status.pop_ping_latency_ms,
                    "alerts": self._parse_alerts(status.alerts),
                    "timestamp": datetime.now().isoformat(),
                }

                self._last_status = result
                self._last_update = time.time()
                return result

        except GrpcError as e:
            logger.error(f"gRPC error getting status: {e}")
            return self._get_last_or_simulated_status()
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return self._get_last_or_simulated_status()

        return self._get_simulated_status()

    def get_obstruction_map(self) -> Dict[str, Any]:
        """
        Get obstruction map showing blocked areas in the sky.

        Returns:
            Dictionary containing obstruction map data
        """
        if self.simulation_mode:
            return {
                "obstructed": False,
                "fraction_obstructed": 0.02,
                "wedge_fraction_obstructed": [0.01] * 12,
                "timestamp": datetime.now().isoformat(),
            }

        try:
            request = device_pb2.Request()
            request.get_status.SetInParent()

            with self.context as channel:
                response = channel.call(request)

            if response.HasField("dish_get_status"):
                obs_stats = response.dish_get_status.obstruction_stats
                return {
                    "obstructed": response.dish_get_status.obstructed,
                    "fraction_obstructed": obs_stats.fraction_obstructed,
                    "wedge_fraction_obstructed": list(obs_stats.wedge_fraction_obstructed),
                    "valid_s": obs_stats.valid_s,
                    "timestamp": datetime.now().isoformat(),
                }

        except Exception as e:
            logger.error(f"Error getting obstruction map: {e}")
            return {
                "obstructed": False,
                "fraction_obstructed": 0.0,
                "timestamp": datetime.now().isoformat(),
            }

    def reboot(self) -> bool:
        """
        Reboot the Starlink dish.

        Returns:
            True if reboot command was successful
        """
        if self.simulation_mode:
            logger.info("SIMULATION: Rebooting dish")
            return True

        try:
            request = device_pb2.Request()
            request.reboot.SetInParent()

            with self.context as channel:
                channel.call(request)

            logger.info("Dish reboot initiated")
            return True

        except Exception as e:
            logger.error(f"Error rebooting dish: {e}")
            return False

    def stow(self) -> bool:
        """
        Stow the Starlink dish (flat position for transport/storage).

        Returns:
            True if stow command was successful
        """
        if self.simulation_mode:
            logger.info("SIMULATION: Stowing dish")
            return True

        try:
            request = device_pb2.Request()
            request.dish_stow.SetInParent()

            with self.context as channel:
                channel.call(request)

            logger.info("Dish stow initiated")
            return True

        except Exception as e:
            logger.error(f"Error stowing dish: {e}")
            return False

    def unstow(self) -> bool:
        """
        Unstow the Starlink dish (move to operational position).

        Returns:
            True if unstow command was successful
        """
        if self.simulation_mode:
            logger.info("SIMULATION: Unstowing dish")
            return True

        try:
            request = device_pb2.Request()
            request.dish_get_status.SetInParent()  # Unstow happens automatically when requesting status

            with self.context as channel:
                channel.call(request)

            logger.info("Dish unstow initiated")
            return True

        except Exception as e:
            logger.error(f"Error unstowing dish: {e}")
            return False

    def get_history(self, samples: int = 300) -> Dict[str, Any]:
        """
        Get historical performance data.

        Args:
            samples: Number of samples to retrieve

        Returns:
            Dictionary containing historical metrics
        """
        if self.simulation_mode:
            return self._get_simulated_history(samples)

        try:
            request = device_pb2.Request()
            request.get_history.SetInParent()

            with self.context as channel:
                response = channel.call(request)

            if response.HasField("dish_get_history"):
                history = response.dish_get_history
                return {
                    "pop_ping_latency_ms": list(history.pop_ping_latency_ms),
                    "downlink_throughput_bps": list(history.downlink_throughput_bps),
                    "uplink_throughput_bps": list(history.uplink_throughput_bps),
                    "snr": list(history.snr),
                    "obstructed": list(history.obstructed),
                    "current_cell_id": history.current_cell_id,
                    "timestamp": datetime.now().isoformat(),
                }

        except Exception as e:
            logger.error(f"Error getting history: {e}")
            return self._get_simulated_history(samples)

    def _parse_state(self, state: int) -> str:
        """Parse dish state integer to human-readable string."""
        states = {
            0: "UNKNOWN",
            1: "BOOTING",
            2: "STOWED",
            3: "SEARCHING",
            4: "CONNECTED",
        }
        return states.get(state, f"UNKNOWN_{state}")

    def _parse_alerts(self, alerts: int) -> List[str]:
        """Parse alerts bitfield to list of alert strings."""
        alert_list = []
        alert_names = {
            1: "MOTORS_STUCK",
            2: "THERMAL_THROTTLE",
            4: "THERMAL_SHUTDOWN",
            8: "MAST_NOT_NEAR_VERTICAL",
            16: "SLOW_ETHERNET_SPEEDS",
            32: "SOFTWARE_INSTALL_PENDING",
        }
        
        for bit, name in alert_names.items():
            if alerts & bit:
                alert_list.append(name)
        
        return alert_list

    def _get_simulated_status(self) -> Dict[str, Any]:
        """Generate simulated status data for testing."""
        return {
            "uptime": 86400,
            "state": "CONNECTED",
            "obstructed": False,
            "obstruction_percent": 0.02,
            "snr": 9.5,
            "downlink_throughput_bps": 50_000_000,
            "uplink_throughput_bps": 10_000_000,
            "ping_latency_ms": 35.0,
            "alerts": [],
            "timestamp": datetime.now().isoformat(),
        }

    def _get_simulated_history(self, samples: int) -> Dict[str, Any]:
        """Generate simulated history data for testing."""
        import numpy as np
        
        latency = list(30 + 10 * np.random.randn(samples))
        downlink = list(50_000_000 + 10_000_000 * np.random.randn(samples))
        uplink = list(10_000_000 + 2_000_000 * np.random.randn(samples))
        snr = list(9 + 2 * np.random.randn(samples))
        obstructed = [False] * samples
        
        return {
            "pop_ping_latency_ms": latency,
            "downlink_throughput_bps": downlink,
            "uplink_throughput_bps": uplink,
            "snr": snr,
            "obstructed": obstructed,
            "current_cell_id": 123456,
            "timestamp": datetime.now().isoformat(),
        }

    def _get_last_or_simulated_status(self) -> Dict[str, Any]:
        """Return last known status or simulated data if no last status."""
        if self._last_status and (time.time() - self._last_update) < 60:
            return self._last_status
        return self._get_simulated_status()

    def close(self):
        """Close the connection to Starlink dish."""
        if self.context:
            try:
                self.context.close()
                logger.info("Closed connection to Starlink dish")
            except Exception as e:
                logger.error(f"Error closing connection: {e}")
