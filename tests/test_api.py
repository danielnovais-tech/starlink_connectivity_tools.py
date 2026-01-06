"""
Tests for API endpoints
"""

import unittest
from unittest.mock import Mock, patch
from starlink_connectivity_tools import (
    StarlinkClient,
    AccountsAPI,
    AddressesAPI,
    DataUsageAPI,
    RoutersAPI,
    ServiceLinesAPI,
    SubscriptionsAPI,
    UserTerminalsAPI,
    TLSAPI,
)


class TestStarlinkClient(unittest.TestCase):
    """Test the base StarlinkClient"""
    
    def setUp(self):
        self.client = StarlinkClient(base_url="https://api.starlink.test", api_key="test_key")
    
    def test_client_initialization(self):
        """Test client initializes with correct base URL"""
        self.assertEqual(self.client.base_url, "https://api.starlink.test")
        self.assertEqual(self.client.api_key, "test_key")
    
    def test_client_authorization_header(self):
        """Test client sets authorization header"""
        self.assertIn("Authorization", self.client.session.headers)
        self.assertEqual(self.client.session.headers["Authorization"], "Bearer test_key")


class TestAccountsAPI(unittest.TestCase):
    """Test the AccountsAPI"""
    
    def setUp(self):
        self.client = StarlinkClient(base_url="https://api.starlink.test")
        self.accounts_api = AccountsAPI(self.client)
    
    @patch.object(StarlinkClient, 'get')
    def test_get_account(self, mock_get):
        """Test get_account calls correct endpoint"""
        mock_get.return_value = {"email": "test@example.com", "customer_id": "123"}
        result = self.accounts_api.get_account()
        mock_get.assert_called_once_with('/account')
        self.assertEqual(result["email"], "test@example.com")


class TestAddressesAPI(unittest.TestCase):
    """Test the AddressesAPI"""
    
    def setUp(self):
        self.client = StarlinkClient(base_url="https://api.starlink.test")
        self.addresses_api = AddressesAPI(self.client)
    
    @patch.object(StarlinkClient, 'post')
    def test_create_address(self, mock_post):
        """Test create_address calls correct endpoint"""
        address_data = {"street": "123 Main St", "city": "Seattle"}
        mock_post.return_value = {"id": "addr_123", **address_data}
        result = self.addresses_api.create_address(address_data)
        mock_post.assert_called_once_with('/addresses', json_data=address_data)
        self.assertEqual(result["id"], "addr_123")
    
    @patch.object(StarlinkClient, 'get')
    def test_get_address(self, mock_get):
        """Test get_address calls correct endpoint"""
        mock_get.return_value = {"id": "addr_123", "street": "123 Main St"}
        result = self.addresses_api.get_address("addr_123")
        mock_get.assert_called_once_with('/addresses/addr_123')
        self.assertEqual(result["id"], "addr_123")


class TestDataUsageAPI(unittest.TestCase):
    """Test the DataUsageAPI"""
    
    def setUp(self):
        self.client = StarlinkClient(base_url="https://api.starlink.test")
        self.data_usage_api = DataUsageAPI(self.client)
    
    @patch.object(StarlinkClient, 'get')
    def test_get_data_usage(self, mock_get):
        """Test get_data_usage calls correct endpoint"""
        mock_get.return_value = {"total_bytes": 1000000}
        result = self.data_usage_api.get_data_usage()
        mock_get.assert_called_once_with('/data-usage')
        self.assertEqual(result["total_bytes"], 1000000)


class TestRoutersAPI(unittest.TestCase):
    """Test the RoutersAPI"""
    
    def setUp(self):
        self.client = StarlinkClient(base_url="https://api.starlink.test")
        self.routers_api = RoutersAPI(self.client)
    
    @patch.object(StarlinkClient, 'get')
    def test_get_router_config(self, mock_get):
        """Test get_router_config calls correct endpoint"""
        mock_get.return_value = {"ssid": "Starlink-WiFi", "password": "secret"}
        result = self.routers_api.get_router_config("router_123")
        mock_get.assert_called_once_with('/routers/router_123/config')
        self.assertEqual(result["ssid"], "Starlink-WiFi")


class TestServiceLinesAPI(unittest.TestCase):
    """Test the ServiceLinesAPI"""
    
    def setUp(self):
        self.client = StarlinkClient(base_url="https://api.starlink.test")
        self.service_lines_api = ServiceLinesAPI(self.client)
    
    @patch.object(StarlinkClient, 'post')
    def test_create_service_line(self, mock_post):
        """Test create_service_line calls correct endpoint"""
        line_data = {"address_id": "addr_123", "product_id": "prod_123"}
        mock_post.return_value = {"id": "line_123", **line_data}
        result = self.service_lines_api.create_service_line(line_data)
        mock_post.assert_called_once_with('/service-lines', json_data=line_data)
        self.assertEqual(result["id"], "line_123")
    
    @patch.object(StarlinkClient, 'get')
    def test_get_service_line(self, mock_get):
        """Test get_service_line calls correct endpoint"""
        mock_get.return_value = {"id": "line_123", "status": "active"}
        result = self.service_lines_api.get_service_line("line_123")
        mock_get.assert_called_once_with('/service-lines/line_123')
        self.assertEqual(result["id"], "line_123")


class TestSubscriptionsAPI(unittest.TestCase):
    """Test the SubscriptionsAPI"""
    
    def setUp(self):
        self.client = StarlinkClient(base_url="https://api.starlink.test")
        self.subscriptions_api = SubscriptionsAPI(self.client)
    
    @patch.object(StarlinkClient, 'get')
    def test_get_subscriptions(self, mock_get):
        """Test get_subscriptions calls correct endpoint"""
        mock_get.return_value = {"items": [{"name": "Standard"}, {"name": "Premium"}]}
        result = self.subscriptions_api.get_subscriptions()
        mock_get.assert_called_once_with('/subscriptions')
        self.assertEqual(len(result["items"]), 2)


class TestUserTerminalsAPI(unittest.TestCase):
    """Test the UserTerminalsAPI"""
    
    def setUp(self):
        self.client = StarlinkClient(base_url="https://api.starlink.test")
        self.terminals_api = UserTerminalsAPI(self.client)
    
    @patch.object(StarlinkClient, 'get')
    def test_get_user_terminal(self, mock_get):
        """Test get_user_terminal calls correct endpoint"""
        mock_get.return_value = {"id": "term_123", "status": "online"}
        result = self.terminals_api.get_user_terminal("term_123")
        mock_get.assert_called_once_with('/user-terminals/term_123')
        self.assertEqual(result["id"], "term_123")
    
    @patch.object(StarlinkClient, 'post')
    def test_create_user_terminal(self, mock_post):
        """Test create_user_terminal calls correct endpoint"""
        terminal_data = {"service_line_id": "line_123", "serial_number": "SN123"}
        mock_post.return_value = {"id": "term_123", **terminal_data}
        result = self.terminals_api.create_user_terminal(terminal_data)
        mock_post.assert_called_once_with('/user-terminals', json_data=terminal_data)
        self.assertEqual(result["id"], "term_123")


class TestTLSAPI(unittest.TestCase):
    """Test the TLSAPI"""
    
    def setUp(self):
        self.client = StarlinkClient(base_url="https://api.starlink.test")
        self.tls_api = TLSAPI(self.client)
    
    @patch.object(StarlinkClient, 'get')
    def test_get_tls_config(self, mock_get):
        """Test get_tls_config calls correct endpoint"""
        mock_get.return_value = {"certificate": "cert_data", "key": "key_data"}
        result = self.tls_api.get_tls_config()
        mock_get.assert_called_once_with('/tls')
        self.assertEqual(result["certificate"], "cert_data")


if __name__ == '__main__':
    unittest.main()
