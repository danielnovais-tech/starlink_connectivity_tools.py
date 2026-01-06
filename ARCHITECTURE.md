# Architecture and Design

## Overview

This library provides a Python interface to the Starlink dish gRPC API. The implementation is designed to be flexible and extensible while providing a simple, intuitive API for users.

## Design Principles

1. **Minimal Dependencies**: Only essential gRPC libraries required
2. **Extensibility**: Easy to add proto files when available
3. **Usability**: Simple API with sensible defaults
4. **Reflection-First**: Use server reflection when proto files unavailable
5. **Safety**: Proper error handling and resource management

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────┐
│                  StarlinkDishClient                     │
│  - Connection management                                │
│  - Context manager support                              │
│  - Method placeholders for proto-based calls            │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ uses
                 ▼
┌─────────────────────────────────────────────────────────┐
│              ProtoReflectionClient                      │
│  - Service discovery                                    │
│  - Proto file extraction                                │
│  - Dynamic message handling                             │
└─────────────────────────────────────────────────────────┘
```

### Connection Flow

```
User Code
   │
   ├─► StarlinkDishClient()
   │      │
   │      ├─► connect()
   │      │      │
   │      │      ├─► Create gRPC channel
   │      │      ├─► Test connection
   │      │      └─► Ready for use
   │      │
   │      ├─► discover_services()
   │      │      │
   │      │      └─► ProtoReflectionClient.list_services()
   │      │
   │      └─► close()
   │             └─► Cleanup resources
   │
   └─► Context Manager (__enter__/__exit__)
          └─► Automatic connect/close
```

## Extension Points

### Adding Proto Files

When you have Starlink proto files:

1. **Compile Proto Files**:
```bash
python -m grpc_tools.protoc \
    -I./protos \
    --python_out=./starlink_connectivity_tools \
    --grpc_python_out=./starlink_connectivity_tools \
    protos/*.proto
```

2. **Import in Client**:
```python
# In client.py
try:
    from . import starlink_pb2, starlink_pb2_grpc
    PROTO_AVAILABLE = True
except ImportError:
    PROTO_AVAILABLE = False
```

3. **Implement Methods**:
```python
def get_status(self) -> Dict[str, Any]:
    if not PROTO_AVAILABLE:
        raise NotImplementedError("Proto files required")
    
    stub = starlink_pb2_grpc.DeviceStub(self._channel)
    request = starlink_pb2.Request()
    response = stub.Handle(request)
    
    return {
        'uptime': response.dish_get_status.device_info.uptime,
        'connected': response.dish_get_status.state == starlink_pb2.CONNECTED,
        # ... more fields
    }
```

### Custom Method Calls

The `call_method()` placeholder can be implemented for generic RPC calls:

```python
def call_method(self, service_name, method_name, request_data):
    # Get service descriptor via reflection
    service_desc = self.reflection.get_service_descriptor(service_name)
    
    # Create request message dynamically
    factory = DynamicMessageFactory(self.reflection)
    request = factory.create_message(method_name + "Request", request_data)
    
    # Make RPC call
    # ... implementation
```

## Error Handling

The library uses a tiered error handling approach:

1. **Connection Errors**: Raised as `ConnectionError`
2. **RPC Errors**: Raised as `grpc.RpcError` with details
3. **Not Implemented**: `NotImplementedError` for proto-dependent features
4. **Runtime Errors**: For reflection and other operational issues

## Testing Strategy

- **Unit Tests**: Mock gRPC channels and responses
- **Integration Tests**: Would require actual Starlink hardware
- **Example Scripts**: Serve as integration tests when hardware available

## Performance Considerations

1. **Connection Reuse**: Use context managers or explicit connect/close
2. **Channel Options**: Configured for large messages (100MB)
3. **Timeouts**: Configurable, defaults to 10 seconds
4. **Lazy Loading**: Proto stubs loaded only when needed

## Security Notes

1. **Local Access**: No authentication required (by design)
2. **Remote Access**: Session cookies should be protected
3. **Cookie Expiry**: 15 days, must be refreshed
4. **No Secrets**: Library does not store credentials

## Future Enhancements

Potential improvements when proto files become available:

- [ ] Streaming telemetry support
- [ ] Configuration validation
- [ ] Connection pooling
- [ ] Async/await support
- [ ] CLI tool for common operations
- [ ] Prometheus exporter
- [ ] Home Assistant integration

## References

- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [Server Reflection Protocol](https://github.com/grpc/grpc/blob/master/doc/server-reflection.md)
- [Protocol Buffers Guide](https://developers.google.com/protocol-buffers)
