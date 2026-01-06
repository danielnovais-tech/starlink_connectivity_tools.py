#!/usr/bin/env python3
import argparse
import json
import sys
import time
from typing import Dict, Any, Optional, Union, Tuple
import grpc
import device_pb2
import device_pb2_grpc
from google.protobuf.json_format import MessageToDict

STARLINK_ROUTER_GRPC_ADDR = "192.168.1.1:9000"
STARLINK_DISH_GRPC_ADDR = "192.168.100.1:9200"
TIMEOUT_SECONDS = 10

class StarlinkClient:
    def __init__(self, router_addr: str = STARLINK_ROUTER_GRPC_ADDR,
                 dish_addr: str = STARLINK_DISH_GRPC_ADDR):
        self.router_addr = router_addr
        self.dish_addr = dish_addr

    def _create_channel(self, addr: str) -> grpc.Channel:
        return grpc.insecure_channel(
            addr,
            options=[
                ('grpc.keepalive_time_ms', 10000),
                ('grpc.keepalive_timeout_ms', 5000),
            ]
        )

    def _get_stub(self, addr: str) -> device_pb2_grpc.DeviceStub:
        channel = self._create_channel(addr)
        return device_pb2_grpc.DeviceStub(channel)

    def get_diagnostics(self, target: str = "both") -> Dict[str, Any]:
        results = {}
        if target in ["router", "both"]:
            try:
                stub = self._get_stub(self.router_addr)
                request = device_pb2.Request(
                    get_diagnostics=device_pb2.GetDiagnosticsRequest()
                )
                response = stub.Handle(request, timeout=TIMEOUT_SECONDS)
                results["router"] = MessageToDict(response)
            except grpc.RpcError as e:
                results["router"] = {"error": f"{e.code()}: {e.details()}"}
        if target in ["dish", "both"]:
            try:
                stub = self._get_stub(self.dish_addr)
                request = device_pb2.Request(
                    get_diagnostics=device_pb2.GetDiagnosticsRequest()
                )
                response = stub.Handle(request, timeout=TIMEOUT_SECONDS)
                results["dish"] = MessageToDict(response)
            except grpc.RpcError as e:
                results["dish"] = {"error": f"{e.code()}: {e.details()}"}
        return results

    def get_status(self, target: str = "both") -> Dict[str, Any]:
        results = {}
        if target in ["router", "both"]:
            try:
                stub = self._get_stub(self.router_addr)
                request = device_pb2.Request(
                    get_status=device_pb2.GetStatusRequest()
                )
                response = stub.Handle(request, timeout=TIMEOUT_SECONDS)
                results["router"] = MessageToDict(response)
            except grpc.RpcError as e:
                results["router"] = {"error": f"{e.code()}: {e.details()}"}
        if target in ["dish", "both"]:
            try:
                stub = self._get_stub(self.dish_addr)
                request = device_pb2.Request(
                    get_status=device_pb2.GetStatusRequest()
                )
                response = stub.Handle(request, timeout=TIMEOUT_SECONDS)
                results["dish"] = MessageToDict(response)
            except grpc.RpcError as e:
                results["dish"] = {"error": f"{e.code()}: {e.details()}"}
        return results

    def get_ping_metrics(self) -> Dict[str, Any]:
        try:
            stub = self._get_stub(self.dish_addr)
            request = device_pb2.Request(
                get_ping_metrics=device_pb2.GetPingMetricsRequest()
            )
            response = stub.Handle(request, timeout=TIMEOUT_SECONDS)
            return MessageToDict(response)
        except grpc.RpcError as e:
            return {"error": f"{e.code()}: {e.details()}"}

    def reboot(self, target: str) -> Dict[str, Any]:
        addr = self.router_addr if target == "router" else self.dish_addr
        try:
            stub = self._get_stub(addr)
            request = device_pb2.Request(
                reboot=device_pb2.RebootRequest()
            )
            response = stub.Handle(request, timeout=TIMEOUT_SECONDS)
            return MessageToDict(response)
        except grpc.RpcError as e:
            return {"error": f"{e.code()}: {e.details()}"}

    def get_speed_test(self) -> Dict[str, Any]:
        try:
            stub = self._get_stub(self.router_addr)
            request = device_pb2.Request(
                get_speed_test=device_pb2.GetSpeedTestRequest()
            )
            response = stub.Handle(request, timeout=TIMEOUT_SECONDS)
            return MessageToDict(response)
        except grpc.RpcError as e:
            return {"error": f"{e.code()}: {e.details()}"}

    def run_speed_test(self) -> Dict[str, Any]:
        try:
            stub = self._get_stub(self.router_addr)
            request = device_pb2.Request(
                run_speed_test=device_pb2.RunSpeedTestRequest()
            )
            response = stub.Handle(request, timeout=30)
            return MessageToDict(response)
        except grpc.RpcError as e:
            return {"error": f"{e.code()}: {e.details()}"}

    def get_device_info(self, target: str = "both") -> Dict[str, Any]:
        results = {}
        if target in ["router", "both"]:
            try:
                stub = self._get_stub(self.router_addr)
                request = device_pb2.Request(
                    get_device_info=device_pb2.GetDeviceInfoRequest()
                )
                response = stub.Handle(request, timeout=TIMEOUT_SECONDS)
                results["router"] = MessageToDict(response)
            except grpc.RpcError as e:
                results["router"] = {"error": f"{e.code()}: {e.details()}"}
        if target in ["dish", "both"]:
            try:
                stub = self._get_stub(self.dish_addr)
                request = device_pb2.Request(
                    get_device_info=device_pb2.GetDeviceInfoRequest()
                )
                response = stub.Handle(request, timeout=TIMEOUT_SECONDS)
                results["dish"] = MessageToDict(response)
            except grpc.RpcError as e:
                results["dish"] = {"error": f"{e.code()}: {e.details()}"}
        return results


def main():
    parser = argparse.ArgumentParser(description="Starlink API Client")
    parser.add_argument(
        "--command", "-c",
        choices=["diagnostics", "status", "ping", "reboot", "speed-test",
                 "run-speed-test", "device-info"],
        default="diagnostics",
        help="Command to execute"
    )
    parser.add_argument(
        "--target", "-t",
        choices=["router", "dish", "both"],
        default="both",
        help="Target device"
    )
    parser.add_argument(
        "--router-addr",
        default=STARLINK_ROUTER_GRPC_ADDR,
        help="Router gRPC address"
    )
    parser.add_argument(
        "--dish-addr",
        default=STARLINK_DISH_GRPC_ADDR,
        help="Dish gRPC address"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "pretty"],
        default="pretty",
        help="Output format"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file"
    )
    args = parser.parse_args()
    client = StarlinkClient(args.router_addr, args.dish_addr)
    result = None
    if args.command == "diagnostics":
        result = client.get_diagnostics(args.target)
    elif args.command == "status":
        result = client.get_status(args.target)
    elif args.command == "ping":
        result = client.get_ping_metrics()
    elif args.command == "reboot":
        if args.target == "both":
            print("Error: Cannot reboot both devices simultaneously. Specify --target.")
            sys.exit(1)
        result = client.reboot(args.target)
    elif args.command == "speed-test":
        result = client.get_speed_test()
    elif args.command == "run-speed-test":
        print("Running speed test (this may take a moment)...")
        result = client.run_speed_test()
    elif args.command == "device-info":
        result = client.get_device_info(args.target)

    if args.format == "json":
        output = json.dumps(result)
    else:
        output = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
