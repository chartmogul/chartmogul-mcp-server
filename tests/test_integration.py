import pytest
from unittest.mock import Mock, patch
import os


class TestEndToEndIntegration:
    """Integration tests that test the complete workflow."""
    
    @patch.dict(os.environ, {'CHARTMOGUL_TOKEN': 'test_token'})
    @patch('chartmogul_mcp.mcp_server.load_dotenv')
    @patch('chartmogul_mcp.mcp_server.api_client.chartmogul')
    @patch('chartmogul_mcp.mcp_server.FastMCP')
    def test_full_server_initialization_and_api_call(self, mock_fastmcp, mock_chartmogul, mock_load_dotenv):
        """Test complete server initialization and API call workflow."""
        # Setup mocks
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        # Mock ChartMogul config and API response
        mock_config = Mock()
        mock_chartmogul.Config.return_value = mock_config
        
        mock_request = Mock()
        mock_response = Mock()
        mock_response.__dict__ = {'id': 'acc_123', 'name': 'Test Account'}
        mock_request.get.return_value = mock_response
        mock_chartmogul.Account.retrieve.return_value = mock_request
        
        # Import and create server
        from chartmogul_mcp.mcp_server import ChartMogulMcp
        server = ChartMogulMcp()
        
        # Verify server was initialized correctly
        assert server.mcp == mock_mcp_instance
        assert server.config == mock_config
        
        # Test API call through the server's config
        from chartmogul_mcp.api_client import retrieve_account
        result = retrieve_account(server.config)
        
        # Verify the API call worked
        mock_chartmogul.Account.retrieve.assert_called_once_with(mock_config)
        assert result == {'id': 'acc_123', 'name': 'Test Account'}
    
    @patch.dict(os.environ, {'CHARTMOGUL_TOKEN': 'test_token'})
    @patch('chartmogul_mcp.mcp_server.api_client.chartmogul')
    def test_api_client_decorator_integration_with_real_functions(self, mock_chartmogul):
        """Test that decorator works with actual API client functions."""
        # Setup mocks for multiple API calls
        mock_config = Mock()
        mock_chartmogul.Config.return_value = mock_config
        
        # Test successful case
        mock_request = Mock()
        mock_response = Mock()
        mock_response.__dict__ = {'uuid': 'ds_123', 'name': 'Test Source'}
        mock_request.get.return_value = mock_response
        mock_chartmogul.DataSource.retrieve.return_value = mock_request
        
        from chartmogul_mcp.api_client import retrieve_source, init_chartmogul_config
        
        config = init_chartmogul_config()
        result = retrieve_source(config, 'ds_123')
        
        assert result == {'uuid': 'ds_123', 'name': 'Test Source'}
        
        # Test error case
        mock_request.get.side_effect = Exception("API Error")
        
        with patch('chartmogul_mcp.api_client.LOGGER') as mock_logger:
            result = retrieve_source(config, 'ds_123')
            
            assert result is None
            mock_logger.error.assert_called()
    
    @patch.dict(os.environ, {'CHARTMOGUL_TOKEN': 'test_token'})
    def test_module_imports_and_dependencies(self):
        """Test that all modules can be imported and work together."""
        # Test importing all main modules
        try:
            from chartmogul_mcp import utils
            from chartmogul_mcp import api_client
            from chartmogul_mcp import mcp_server
            
            # Test that they can access each other's components
            assert utils.CHARTMOGUL_TOKEN == 'test_token'
            assert hasattr(api_client, 'handle_api_errors')
            assert hasattr(mcp_server, 'ChartMogulMcp')
            
        except ImportError as e:
            pytest.fail(f"Module import failed: {e}")
    
    def test_error_handling_consistency_across_all_functions(self):
        """Test that all API functions handle errors consistently."""
        from chartmogul_mcp import api_client
        
        # Get all functions that should have the decorator
        api_functions = [
            getattr(api_client, name) for name in dir(api_client)
            if callable(getattr(api_client, name)) 
            and not name.startswith('_')
            and name not in ['handle_api_errors', 'init_chartmogul_config', 'parse_object']
        ]
        
        # Test that functions with decorator return None on errors
        functions_with_decorator = []
        for func in api_functions:
            if hasattr(func, '__wrapped__'):
                functions_with_decorator.append(func)
        
        # Should have many functions with decorators
        assert len(functions_with_decorator) > 10, "Many functions should have error handling decorator"
        
        # Test a few key functions have the decorator
        key_functions = ['retrieve_account', 'list_sources', 'list_customers', 'create_customer']
        for func_name in key_functions:
            func = getattr(api_client, func_name)
            assert hasattr(func, '__wrapped__'), f"{func_name} should have error handling decorator"


class TestConfigurationIntegration:
    """Test configuration and environment variable integration."""
    
    @patch.dict(os.environ, {'CHARTMOGUL_TOKEN': 'integration_test_token'})
    def test_environment_variable_integration(self):
        """Test that environment variables are properly loaded."""
        # Force reload of utils module to pick up environment changes
        import importlib
        from chartmogul_mcp import utils
        importlib.reload(utils)
        
        assert utils.CHARTMOGUL_TOKEN == 'integration_test_token'
    
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_environment_variable_handling(self):
        """Test behavior when environment variables are missing."""
        # Force reload of utils module
        import importlib
        from chartmogul_mcp import utils
        importlib.reload(utils)
        
        # Should handle missing token gracefully
        assert utils.CHARTMOGUL_TOKEN is None
    
    @patch('chartmogul_mcp.api_client.utils.CHARTMOGUL_TOKEN', None)
    @patch('chartmogul_mcp.api_client.chartmogul.Config')
    def test_config_with_none_token(self, mock_config):
        """Test configuration creation with None token."""
        from chartmogul_mcp.api_client import init_chartmogul_config
        
        config = init_chartmogul_config()
        
        # Should still create config, even with None token
        mock_config.assert_called_once_with(None)


class TestErrorPropagation:
    """Test that errors are properly propagated through the system."""
    
    @patch('chartmogul_mcp.api_client.chartmogul')
    @patch('chartmogul_mcp.api_client.LOGGER')
    def test_api_error_logging_integration(self, mock_logger, mock_chartmogul):
        """Test that API errors are properly logged through the system."""
        # Setup mock to raise exception
        mock_config = Mock()
        mock_request = Mock()
        mock_request.get.side_effect = ConnectionError("Network error")
        mock_chartmogul.Account.retrieve.return_value = mock_request
        
        from chartmogul_mcp.api_client import retrieve_account
        
        result = retrieve_account(mock_config)
        
        # Should return None
        assert result is None
        
        # Should log the error
        mock_logger.error.assert_called_once()
        error_args = mock_logger.error.call_args
        assert "Error retrieving account: Network error" in error_args[0][0]
        assert error_args[1]['exc_info'] is True
    
    @patch('chartmogul_mcp.api_client.chartmogul')
    def test_multiple_error_scenarios(self, mock_chartmogul):
        """Test different types of exceptions are handled consistently."""
        from chartmogul_mcp.api_client import retrieve_account
        
        mock_config = Mock()
        mock_request = Mock()
        mock_chartmogul.Account.retrieve.return_value = mock_request
        
        # Test different exception types
        exception_types = [
            ValueError("Invalid value"),
            ConnectionError("Network error"),
            TimeoutError("Request timeout"),
            RuntimeError("Runtime error"),
        ]
        
        for exception in exception_types:
            mock_request.get.side_effect = exception
            
            with patch('chartmogul_mcp.api_client.LOGGER'):
                result = retrieve_account(mock_config)
                assert result is None, f"Should return None for {type(exception).__name__}"


class TestSystemIntegration:
    """Test system-level integration scenarios."""
    
    def test_package_structure_integrity(self):
        """Test that the package structure is intact."""
        import chartmogul_mcp
        
        # Test that main modules exist
        assert hasattr(chartmogul_mcp, 'api_client')
        assert hasattr(chartmogul_mcp, 'utils')
        assert hasattr(chartmogul_mcp, 'mcp_server')
    
    def test_logging_system_integration(self):
        """Test that logging system works across modules."""
        from chartmogul_mcp.utils import LOGGER
        from chartmogul_mcp.api_client import LOGGER as api_logger
        from chartmogul_mcp.mcp_server import LOGGER as server_logger
        
        # All should reference the same logger instance or have same name
        assert LOGGER.name == api_logger.name == server_logger.name
    
    @patch.dict(os.environ, {'CHARTMOGUL_TOKEN': 'test_token'})
    @patch('chartmogul_mcp.mcp_server.FastMCP')
    @patch('chartmogul_mcp.api_client.chartmogul')
    def test_complete_initialization_workflow(self, mock_chartmogul, mock_fastmcp):
        """Test the complete initialization workflow from start to finish."""
        # Mock dependencies
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        mock_config = Mock()
        mock_chartmogul.Config.return_value = mock_config
        
        # Test full workflow
        from chartmogul_mcp.mcp_server import ChartMogulMcp
        
        # Initialize server
        server = ChartMogulMcp()
        
        # Verify initialization completed successfully
        assert server is not None
        assert server.config is not None
        assert server.mcp is not None
        
        # Verify tools were registered
        mock_mcp_instance.tool.assert_called()


if __name__ == "__main__":
    pytest.main([__file__])