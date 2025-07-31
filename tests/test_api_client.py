import pytest
from unittest.mock import Mock, patch
from chartmogul_mcp.api_client import (
    handle_api_errors, 
    init_chartmogul_config,
    retrieve_account,
    list_sources,
    retrieve_source,
    list_customers,
    create_customer,
    retrieve_customer,
    update_customer,
    search_customers,
    parse_object
)


class TestHandleApiErrorsDecorator:
    """Test the error handling decorator."""
    
    def test_decorator_success_case(self):
        """Test decorator allows successful function execution."""
        @handle_api_errors("test operation")
        def successful_function():
            return "success"
        
        result = successful_function()
        assert result == "success"
    
    def test_decorator_error_case(self, capfd):
        """Test decorator handles exceptions and returns None."""
        with patch('chartmogul_mcp.api_client.LOGGER') as mock_logger:
            @handle_api_errors("test operation")
            def failing_function():
                raise ValueError("Test error")
            
            result = failing_function()
            
            assert result is None
            mock_logger.error.assert_called_once()
            error_call_args = mock_logger.error.call_args
            assert "Error test operation: Test error" in error_call_args[0][0]
            assert error_call_args[1]['exc_info'] is True
    
    def test_decorator_with_default_operation_name(self):
        """Test decorator uses function name when no operation name provided."""
        with patch('chartmogul_mcp.api_client.LOGGER') as mock_logger:
            @handle_api_errors()
            def some_function_name():
                raise RuntimeError("Test error")
            
            result = some_function_name()
            
            assert result is None
            mock_logger.error.assert_called_once()
            error_call_args = mock_logger.error.call_args
            assert "Error some function name: Test error" in error_call_args[0][0]
    
    def test_decorator_preserves_function_metadata(self):
        """Test decorator preserves original function metadata."""
        @handle_api_errors("test")
        def documented_function():
            """This is a test function."""
            return "test"
        
        assert documented_function.__doc__ == "This is a test function."
        assert documented_function.__name__ == "documented_function"


class TestInitChartMogulConfig:
    """Test ChartMogul configuration initialization."""
    
    @patch('chartmogul_mcp.api_client.utils.CHARTMOGUL_TOKEN', 'test_token')
    @patch('chartmogul_mcp.api_client.chartmogul.Config')
    def test_init_chartmogul_config(self, mock_config):
        """Test configuration initialization with token."""
        mock_config_instance = Mock()
        mock_config.return_value = mock_config_instance
        
        result = init_chartmogul_config()
        
        mock_config.assert_called_once_with('test_token')
        assert result == mock_config_instance


class TestParseObject:
    """Test the parse_object utility function."""
    
    def test_parse_datetime(self):
        """Test parsing datetime objects."""
        from datetime import datetime, date
        
        dt = datetime(2023, 1, 1, 12, 0, 0)
        result = parse_object(dt)
        assert result == "2023-01-01T12:00:00"
        
        d = date(2023, 1, 1)
        result = parse_object(d)
        assert result == "2023-01-01"
    
    def test_parse_object_with_dict(self):
        """Test parsing objects with __dict__ attribute."""
        class TestObj:
            def __init__(self):
                self.name = "test"
                self.value = 123
        
        obj = TestObj()
        result = parse_object(obj)
        
        assert result == {"name": "test", "value": 123}
    
    def test_parse_list(self):
        """Test parsing lists."""
        test_list = [1, 2, "test"]
        result = parse_object(test_list)
        assert result == [1, 2, "test"]
    
    def test_parse_nested_structure(self):
        """Test parsing nested structures."""
        class NestedObj:
            def __init__(self, name):
                self.name = name
        
        class MainObj:
            def __init__(self):
                self.nested = NestedObj("nested_test")
                self.items = [NestedObj("item1"), NestedObj("item2")]
        
        obj = MainObj()
        result = parse_object(obj)
        
        expected = {
            "nested": {"name": "nested_test"},
            "items": [{"name": "item1"}, {"name": "item2"}]
        }
        assert result == expected
    
    def test_parse_primitive_types(self):
        """Test parsing primitive types."""
        assert parse_object("string") == "string"
        assert parse_object(123) == 123
        assert parse_object(True) is True
        assert parse_object(None) is None


class TestAccountEndpoints:
    """Test account-related API endpoints."""
    
    @patch('chartmogul_mcp.api_client.chartmogul.Account')
    @patch('chartmogul_mcp.api_client.parse_object')
    def test_retrieve_account_success(self, mock_parse, mock_account):
        """Test successful account retrieval."""
        # Setup mocks
        mock_request = Mock()
        mock_response = Mock()
        mock_request.get.return_value = mock_response
        mock_account.retrieve.return_value = mock_request
        mock_parse.return_value = {"id": "acc_123", "name": "Test Account"}
        
        config = Mock()
        result = retrieve_account(config)
        
        mock_account.retrieve.assert_called_once_with(config)
        mock_request.get.assert_called_once()
        mock_parse.assert_called_once_with(mock_response)
        assert result == {"id": "acc_123", "name": "Test Account"}
    
    @patch('chartmogul_mcp.api_client.chartmogul.Account')
    @patch('chartmogul_mcp.api_client.LOGGER')
    def test_retrieve_account_error(self, mock_logger, mock_account):
        """Test account retrieval with error."""
        # Setup mocks to raise exception
        mock_request = Mock()
        mock_request.get.side_effect = Exception("API Error")
        mock_account.retrieve.return_value = mock_request
        
        config = Mock()
        result = retrieve_account(config)
        
        assert result is None
        mock_logger.error.assert_called_once()


class TestDataSourceEndpoints:
    """Test data source-related API endpoints."""
    
    @patch('chartmogul_mcp.api_client.chartmogul.DataSource')
    @patch('chartmogul_mcp.api_client.parse_object')
    def test_list_sources_success(self, mock_parse, mock_datasource):
        """Test successful data sources listing."""
        # Setup mocks
        mock_request = Mock()
        mock_response = Mock()
        mock_response.data_sources = [Mock(), Mock()]
        mock_request.get.return_value = mock_response
        mock_datasource.all.return_value = mock_request
        mock_parse.side_effect = lambda x: {"uuid": f"ds_{id(x)}"}
        
        config = Mock()
        result = list_sources(config, name="test", system="Custom")
        
        mock_datasource.all.assert_called_once_with(config, name="test", system="Custom")
        mock_request.get.assert_called_once()
        assert len(result) == 2
        assert all("uuid" in source for source in result)
    
    @patch('chartmogul_mcp.api_client.chartmogul.DataSource')
    @patch('chartmogul_mcp.api_client.parse_object')
    def test_retrieve_source_success(self, mock_parse, mock_datasource):
        """Test successful data source retrieval."""
        # Setup mocks
        mock_request = Mock()
        mock_response = Mock()
        mock_request.get.return_value = mock_response
        mock_datasource.retrieve.return_value = mock_request
        mock_parse.return_value = {"uuid": "ds_123", "name": "Test Source"}
        
        config = Mock()
        result = retrieve_source(config, "ds_123")
        
        mock_datasource.retrieve.assert_called_once_with(config, uuid="ds_123")
        mock_request.get.assert_called_once()
        assert result == {"uuid": "ds_123", "name": "Test Source"}


class TestCustomerEndpoints:
    """Test customer-related API endpoints."""
    
    @patch('chartmogul_mcp.api_client.chartmogul.Customer')
    @patch('chartmogul_mcp.api_client.parse_object')
    def test_list_customers_success(self, mock_parse, mock_customer):
        """Test successful customers listing."""
        # Setup mocks for pagination
        mock_request = Mock()
        mock_response = Mock()
        mock_response.entries = [Mock(), Mock()]
        mock_response.has_more = False
        mock_response.cursor = "cursor_123"
        mock_request.get.return_value = mock_response
        mock_customer.all.return_value = mock_request
        mock_parse.side_effect = lambda x: {"uuid": f"cus_{id(x)}"}
        
        config = Mock()
        result = list_customers(config, limit=20)
        
        mock_customer.all.assert_called_once()
        assert len(result) == 2
        assert all("uuid" in customer for customer in result)
    
    @patch('chartmogul_mcp.api_client.chartmogul.Customer')
    @patch('chartmogul_mcp.api_client.parse_object')
    def test_create_customer_success(self, mock_parse, mock_customer):
        """Test successful customer creation."""
        # Setup mocks
        mock_request = Mock()
        mock_response = Mock()
        mock_request.get.return_value = mock_response
        mock_customer.create.return_value = mock_request
        mock_parse.return_value = {"uuid": "cus_123", "name": "Test Customer"}
        
        config = Mock()
        customer_data = {"name": "Test Customer", "email": "test@example.com"}
        result = create_customer(config, customer_data)
        
        mock_customer.create.assert_called_once_with(config, data=customer_data)
        mock_request.get.assert_called_once()
        assert result == {"uuid": "cus_123", "name": "Test Customer"}
    
    @patch('chartmogul_mcp.api_client.chartmogul.Customer')
    @patch('chartmogul_mcp.api_client.parse_object')
    def test_retrieve_customer_success(self, mock_parse, mock_customer):
        """Test successful customer retrieval."""
        # Setup mocks
        mock_request = Mock()
        mock_response = Mock()
        mock_request.get.return_value = mock_response
        mock_customer.retrieve.return_value = mock_request
        mock_parse.return_value = {"uuid": "cus_123", "name": "Test Customer"}
        
        config = Mock()
        result = retrieve_customer(config, "cus_123")
        
        mock_customer.retrieve.assert_called_once_with(config, uuid="cus_123")
        mock_request.get.assert_called_once()
        assert result == {"uuid": "cus_123", "name": "Test Customer"}
    
    @patch('chartmogul_mcp.api_client.chartmogul.Customer')
    @patch('chartmogul_mcp.api_client.parse_object')
    def test_update_customer_success(self, mock_parse, mock_customer):
        """Test successful customer update."""
        # Setup mocks
        mock_request = Mock()
        mock_response = Mock()
        mock_request.get.return_value = mock_response
        mock_customer.modify.return_value = mock_request
        mock_parse.return_value = {"uuid": "cus_123", "name": "Updated Customer"}
        
        config = Mock()
        update_data = {"name": "Updated Customer"}
        result = update_customer(config, "cus_123", update_data)
        
        mock_customer.modify.assert_called_once_with(config, uuid="cus_123", data=update_data)
        mock_request.get.assert_called_once()
        assert result == {"uuid": "cus_123", "name": "Updated Customer"}
    
    @patch('chartmogul_mcp.api_client.chartmogul.Customer')
    @patch('chartmogul_mcp.api_client.parse_object')
    def test_search_customers_success(self, mock_parse, mock_customer):
        """Test successful customer search."""
        # Setup mocks for pagination
        mock_request = Mock()
        mock_response = Mock()
        mock_response.entries = [Mock()]
        mock_response.has_more = False
        mock_response.cursor = "cursor_123"
        mock_request.get.return_value = mock_response
        mock_customer.search.return_value = mock_request
        mock_parse.side_effect = lambda x: {"uuid": f"cus_{id(x)}", "email": "test@example.com"}
        
        config = Mock()
        result = search_customers(config, "test@example.com", limit=20)
        
        mock_customer.search.assert_called_once()
        assert len(result) == 1
        assert result[0]["email"] == "test@example.com"


class TestErrorHandlingIntegration:
    """Test that all API functions properly use the error handling decorator."""
    
    @patch('chartmogul_mcp.api_client.chartmogul.Account')
    @patch('chartmogul_mcp.api_client.LOGGER')
    def test_decorated_function_handles_errors(self, mock_logger, mock_account):
        """Test that decorated functions handle errors properly."""
        # Setup mock to raise exception
        mock_request = Mock()
        mock_request.get.side_effect = Exception("ChartMogul API Error")
        mock_account.retrieve.return_value = mock_request
        
        config = Mock()
        result = retrieve_account(config)
        
        # Should return None due to decorator error handling
        assert result is None
        
        # Should log the error
        mock_logger.error.assert_called_once()
        error_call_args = mock_logger.error.call_args
        assert "Error retrieving account: ChartMogul API Error" in error_call_args[0][0]
        assert error_call_args[1]['exc_info'] is True
    
    def test_all_api_functions_have_decorator(self):
        """Test that all main API functions have the error handling decorator."""
        functions_to_check = [
            retrieve_account,
            list_sources,
            retrieve_source,
            list_customers,
            create_customer,
            retrieve_customer,
            update_customer,
            search_customers
        ]
        
        for func in functions_to_check:
            # Check if function has been wrapped by decorator
            assert hasattr(func, '__wrapped__'), f"{func.__name__} should have decorator"


if __name__ == "__main__":
    pytest.main([__file__])