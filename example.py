"""
Example usage of the Starlink Connectivity Tools library
"""

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


def main():
    """Demonstrate the usage of various API endpoints"""
    
    # Initialize the client
    # In production, use environment variables or secure storage for the API key
    client = StarlinkClient(
        base_url="https://api.starlink.com",
        api_key="your_api_key_here"
    )
    
    # Example 1: Get account information
    print("=" * 50)
    print("Example 1: Get Account Information")
    print("=" * 50)
    accounts_api = AccountsAPI(client)
    # account = accounts_api.get_account()
    print("Usage: accounts_api.get_account()")
    print("Endpoint: GET /account")
    
    # Example 2: Create and retrieve addresses
    print("\n" + "=" * 50)
    print("Example 2: Manage Addresses")
    print("=" * 50)
    addresses_api = AddressesAPI(client)
    # new_address = addresses_api.create_address({
    #     'street': '123 Main St',
    #     'city': 'Seattle',
    #     'state': 'WA',
    #     'zip': '98101'
    # })
    print("Usage: addresses_api.create_address(address_data)")
    print("Endpoint: POST /addresses")
    print("Usage: addresses_api.get_address('addr_12345')")
    print("Endpoint: GET /addresses/{id}")
    
    # Example 3: Get data usage
    print("\n" + "=" * 50)
    print("Example 3: Get Data Usage")
    print("=" * 50)
    data_usage_api = DataUsageAPI(client)
    # usage = data_usage_api.get_data_usage()
    print("Usage: data_usage_api.get_data_usage()")
    print("Endpoint: GET /data-usage")
    
    # Example 4: Get router configuration
    print("\n" + "=" * 50)
    print("Example 4: Get Router Configuration")
    print("=" * 50)
    routers_api = RoutersAPI(client)
    # config = routers_api.get_router_config('router_12345')
    print("Usage: routers_api.get_router_config('router_12345')")
    print("Endpoint: GET /routers/{id}/config")
    
    # Example 5: Manage service lines
    print("\n" + "=" * 50)
    print("Example 5: Manage Service Lines")
    print("=" * 50)
    service_lines_api = ServiceLinesAPI(client)
    # new_line = service_lines_api.create_service_line({
    #     'address_id': 'addr_12345',
    #     'product_id': 'prod_12345'
    # })
    print("Usage: service_lines_api.create_service_line(line_data)")
    print("Endpoint: POST /service-lines")
    print("Usage: service_lines_api.get_service_line('line_12345')")
    print("Endpoint: GET /service-lines/{id}")
    
    # Example 6: Get subscriptions
    print("\n" + "=" * 50)
    print("Example 6: Get Subscriptions")
    print("=" * 50)
    subscriptions_api = SubscriptionsAPI(client)
    # subscriptions = subscriptions_api.get_subscriptions()
    print("Usage: subscriptions_api.get_subscriptions()")
    print("Endpoint: GET /subscriptions")
    
    # Example 7: Manage user terminals
    print("\n" + "=" * 50)
    print("Example 7: Manage User Terminals")
    print("=" * 50)
    terminals_api = UserTerminalsAPI(client)
    # terminal = terminals_api.get_user_terminal('term_12345')
    # new_terminal = terminals_api.create_user_terminal({
    #     'service_line_id': 'line_12345',
    #     'serial_number': 'SN12345'
    # })
    print("Usage: terminals_api.get_user_terminal('term_12345')")
    print("Endpoint: GET /user-terminals/{id}")
    print("Usage: terminals_api.create_user_terminal(terminal_data)")
    print("Endpoint: POST /user-terminals")
    
    # Example 8: Get TLS configuration
    print("\n" + "=" * 50)
    print("Example 8: Get TLS Configuration")
    print("=" * 50)
    tls_api = TLSAPI(client)
    # tls_config = tls_api.get_tls_config()
    print("Usage: tls_api.get_tls_config()")
    print("Endpoint: GET /tls")
    
    print("\n" + "=" * 50)
    print("All endpoints are available and ready to use!")
    print("=" * 50)


if __name__ == "__main__":
    main()
