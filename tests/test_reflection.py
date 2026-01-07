"""Unit tests for ProtoReflectionClient."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from starlink_connectivity_tools.reflection import ProtoReflectionClient
from google.protobuf import descriptor_pb2


class TestProtoReflectionClient:
    """Test cases for ProtoReflectionClient."""

    def test_init(self):
        """Test initialization."""
        mock_channel = Mock()
        client = ProtoReflectionClient(mock_channel)

        assert client.channel is mock_channel
        assert client.stub is not None

    @patch(
        "starlink_connectivity_tools.reflection.reflection_pb2_grpc.ServerReflectionStub"
    )
    def test_list_services(self, mock_stub_class):
        """Test listing services."""
        # Setup mock
        mock_channel = Mock()
        mock_stub = Mock()
        mock_stub_class.return_value = mock_stub

        # Mock response
        mock_response = Mock()
        mock_service = Mock()
        mock_service.name = "SpaceX.API.Device.Device"
        mock_response.list_services_response.service = [mock_service]
        mock_response.HasField.return_value = True

        mock_stub.ServerReflectionInfo.return_value = [mock_response]

        client = ProtoReflectionClient(mock_channel)
        services = client.list_services()

        assert len(services) == 1
        assert services[0] == "SpaceX.API.Device.Device"

    def test_field_type_mapping(self):
        """Test field type mapping."""
        mock_channel = Mock()
        client = ProtoReflectionClient(mock_channel)

        # Test various field types
        field = Mock()
        field.type = 9  # string
        field.label = 1  # optional
        assert client._get_field_type(field) == "string"

        field.type = 8  # bool
        assert client._get_field_type(field) == "bool"

        field.type = 3  # int64
        assert client._get_field_type(field) == "int64"

        # Test repeated field
        field.type = 9
        field.label = 3  # repeated
        assert client._get_field_type(field) == "repeated string"
