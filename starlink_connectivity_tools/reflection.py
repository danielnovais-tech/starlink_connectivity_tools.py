"""Utilities for working with Starlink gRPC proto files and reflection.

This module provides utilities for extracting proto files from the Starlink
dish using server reflection and working with dynamic proto messages.
"""

import grpc
from typing import List, Dict, Any, Optional
from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory
from google.protobuf.descriptor import ServiceDescriptor, MethodDescriptor


class ProtoReflectionClient:
    """Client for extracting proto definitions using gRPC server reflection.
    
    The Starlink dish supports server reflection, which allows clients to
    discover available services and their proto definitions without having
    the .proto files locally.
    """
    
    def __init__(self, channel: grpc.Channel):
        """Initialize the reflection client.
        
        Args:
            channel: Active gRPC channel to the server.
        """
        self.channel = channel
        self.stub = reflection_pb2_grpc.ServerReflectionStub(channel)
        self._descriptor_pool = descriptor_pool.DescriptorPool()
        
    def list_services(self) -> List[str]:
        """List all available services on the server.
        
        Returns:
            List of fully qualified service names.
        """
        request = reflection_pb2.ServerReflectionRequest(list_services="")
        responses = self.stub.ServerReflectionInfo(iter([request]))
        
        services = []
        for response in responses:
            if response.HasField('list_services_response'):
                for service in response.list_services_response.service:
                    services.append(service.name)
                break
        
        return services
    
    def get_file_descriptor(self, symbol: str) -> descriptor_pb2.FileDescriptorProto:
        """Get file descriptor containing the specified symbol.
        
        Args:
            symbol: Fully qualified symbol name (service, message, etc.)
            
        Returns:
            File descriptor proto for the symbol.
        """
        request = reflection_pb2.ServerReflectionRequest(
            file_containing_symbol=symbol
        )
        responses = self.stub.ServerReflectionInfo(iter([request]))
        
        for response in responses:
            if response.HasField('file_descriptor_response'):
                # First file descriptor is the one we requested
                file_desc_proto = descriptor_pb2.FileDescriptorProto()
                file_desc_proto.ParseFromString(
                    response.file_descriptor_response.file_descriptor_proto[0]
                )
                return file_desc_proto
                
        raise ValueError(f"File descriptor not found for symbol: {symbol}")
    
    def get_service_descriptor(self, service_name: str) -> ServiceDescriptor:
        """Get service descriptor for a service.
        
        Args:
            service_name: Fully qualified service name.
            
        Returns:
            Service descriptor.
        """
        file_desc = self.get_file_descriptor(service_name)
        
        # Add file descriptor to pool
        self._descriptor_pool.Add(file_desc)
        
        # Get service descriptor
        return self._descriptor_pool.FindServiceByName(service_name)
    
    def export_proto_file(self, symbol: str, output_path: str) -> None:
        """Export proto file definition for a symbol to a file.
        
        This can be used to extract and save proto files from the server
        for later use or documentation.
        
        Args:
            symbol: Fully qualified symbol name.
            output_path: Path where to save the .proto file.
        """
        file_desc = self.get_file_descriptor(symbol)
        
        # Convert FileDescriptorProto to proto source
        proto_source = self._file_descriptor_to_proto(file_desc)
        
        with open(output_path, 'w') as f:
            f.write(proto_source)
    
    def _file_descriptor_to_proto(self, file_desc: descriptor_pb2.FileDescriptorProto) -> str:
        """Convert FileDescriptorProto to proto file source.
        
        Args:
            file_desc: File descriptor proto.
            
        Returns:
            Proto file source code as string.
        """
        lines = []
        
        # Syntax
        lines.append(f'syntax = "{file_desc.syntax or "proto3"}";')
        lines.append('')
        
        # Package
        if file_desc.package:
            lines.append(f'package {file_desc.package};')
            lines.append('')
        
        # Dependencies
        for dep in file_desc.dependency:
            lines.append(f'import "{dep}";')
        if file_desc.dependency:
            lines.append('')
        
        # Messages (simplified)
        for msg in file_desc.message_type:
            lines.append(f'message {msg.name} {{')
            for field in msg.field:
                field_type = self._get_field_type(field)
                lines.append(f'  {field_type} {field.name} = {field.number};')
            lines.append('}')
            lines.append('')
        
        # Services
        for service in file_desc.service:
            lines.append(f'service {service.name} {{')
            for method in service.method:
                lines.append(
                    f'  rpc {method.name}({method.input_type}) '
                    f'returns ({method.output_type});'
                )
            lines.append('}')
            lines.append('')
        
        return '\n'.join(lines)
    
    def _get_field_type(self, field) -> str:
        """Get proto field type string.
        
        Args:
            field: Field descriptor.
            
        Returns:
            Field type as string.
        """
        # Type mapping (simplified)
        type_map = {
            1: 'double',
            2: 'float',
            3: 'int64',
            4: 'uint64',
            5: 'int32',
            6: 'fixed64',
            7: 'fixed32',
            8: 'bool',
            9: 'string',
            11: 'message',
            12: 'bytes',
            13: 'uint32',
            14: 'enum',
        }
        
        field_type = type_map.get(field.type, 'unknown')
        
        # For messages and enums, use the type name
        if field.type in (11, 14) and field.type_name:
            field_type = field.type_name.split('.')[-1]
        
        # Handle repeated fields
        if field.label == 3:  # LABEL_REPEATED
            field_type = f'repeated {field_type}'
        
        return field_type


class DynamicMessageFactory:
    """Factory for creating dynamic proto messages from reflection.
    
    This allows calling gRPC methods without having compiled proto files,
    by creating message instances dynamically from server reflection.
    """
    
    def __init__(self, reflection_client: ProtoReflectionClient):
        """Initialize the message factory.
        
        Args:
            reflection_client: Proto reflection client.
        """
        self.reflection_client = reflection_client
        self.message_factory = message_factory.MessageFactory()
        
    def create_message(self, message_type: str, data: Optional[Dict[str, Any]] = None):
        """Create a message instance from a message type name.
        
        Args:
            message_type: Fully qualified message type name.
            data: Optional dictionary of field values.
            
        Returns:
            Message instance.
        """
        # Get file descriptor containing the message
        file_desc = self.reflection_client.get_file_descriptor(message_type)
        
        # Add to pool
        pool = descriptor_pool.DescriptorPool()
        pool.Add(file_desc)
        
        # Get message descriptor
        msg_desc = pool.FindMessageTypeByName(message_type)
        
        # Create message class
        msg_class = self.message_factory.GetPrototype(msg_desc)
        
        # Create instance
        msg = msg_class()
        
        # Set fields if data provided
        if data:
            for key, value in data.items():
                if hasattr(msg, key):
                    setattr(msg, key, value)
        
        return msg
