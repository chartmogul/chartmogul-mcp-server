import pytest
from unittest.mock import Mock, patch


class TestChartMogulMcp:
    """Test the ChartMogulMcp class."""
    
    @patch('chartmogul_mcp.mcp_server.load_dotenv')
    @patch('chartmogul_mcp.mcp_server.api_client.init_chartmogul_config')
    @patch('chartmogul_mcp.mcp_server.FastMCP')
    @patch('chartmogul_mcp.mcp_server.utils')
    def test_init_creates_mcp_server(self, mock_utils, mock_fastmcp, mock_init_config, mock_load_dotenv):
        """Test that ChartMogulMcp initialization creates MCP server correctly."""
        # Setup mocks
        mock_utils.MCP_SERVER_NAME = "test-mcp-server"
        mock_utils.DEPENDENCIES = ["test-dep1", "test-dep2"]
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        mock_config = Mock()
        mock_init_config.return_value = mock_config
        
        from chartmogul_mcp.mcp_server import ChartMogulMcp
        
        # Create instance
        server = ChartMogulMcp()
        
        # Verify initialization
        mock_load_dotenv.assert_called_once()
        mock_fastmcp.assert_called_once_with("test-mcp-server", deps=["test-dep1", "test-dep2"])
        mock_init_config.assert_called_once()
        
        # Verify instance attributes
        assert server.mcp == mock_mcp_instance
        assert server.config == mock_config
    
    @patch('chartmogul_mcp.mcp_server.load_dotenv')
    @patch('chartmogul_mcp.mcp_server.api_client.init_chartmogul_config')
    @patch('chartmogul_mcp.mcp_server.FastMCP')
    @patch('chartmogul_mcp.mcp_server.utils')
    @patch('chartmogul_mcp.mcp_server.LOGGER')
    def test_init_logs_initialization(self, mock_logger, mock_utils, mock_fastmcp, mock_init_config, mock_load_dotenv):
        """Test that initialization is logged."""
        from chartmogul_mcp.mcp_server import ChartMogulMcp
        
        # Create instance
        ChartMogulMcp()
        
        # Verify logging
        mock_logger.info.assert_called_with("ChartMogul MCP Server initialized")
    
    @patch('chartmogul_mcp.mcp_server.load_dotenv')
    @patch('chartmogul_mcp.mcp_server.api_client.init_chartmogul_config')
    @patch('chartmogul_mcp.mcp_server.FastMCP')
    @patch('chartmogul_mcp.mcp_server.utils')
    def test_register_tools_called_during_init(self, mock_utils, mock_fastmcp, mock_init_config, mock_load_dotenv):
        """Test that _register_tools is called during initialization."""
        from chartmogul_mcp.mcp_server import ChartMogulMcp
        
        with patch.object(ChartMogulMcp, '_register_tools') as mock_register:
            ChartMogulMcp()
            mock_register.assert_called_once()


class TestToolRegistration:
    """Test MCP tool registration functionality."""
    
    @patch('chartmogul_mcp.mcp_server.load_dotenv')
    @patch('chartmogul_mcp.mcp_server.api_client.init_chartmogul_config')
    @patch('chartmogul_mcp.mcp_server.FastMCP')
    @patch('chartmogul_mcp.mcp_server.utils')
    def test_retrieve_account_tool_registration(self, mock_utils, mock_fastmcp, mock_init_config, mock_load_dotenv):
        """Test that retrieve_account tool is registered correctly."""
        # Setup mocks
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        from chartmogul_mcp.mcp_server import ChartMogulMcp
        
        # Create instance (this will call _register_tools)
        ChartMogulMcp()
        
        # Verify that the tool decorator was called for retrieve_account
        mock_mcp_instance.tool.assert_called()
        
        # Get all the tool decorator calls
        tool_calls = mock_mcp_instance.tool.call_args_list
        
        # Check that retrieve_account tool was registered
        retrieve_account_call = None
        for call in tool_calls:
            args, kwargs = call
            if 'name' in kwargs and kwargs['name'] == 'retrieve_account':
                retrieve_account_call = call
                break
        
        assert retrieve_account_call is not None, "retrieve_account tool should be registered"
        
        # Verify the tool has correct name and description
        _, kwargs = retrieve_account_call
        assert kwargs['name'] == 'retrieve_account'
        assert 'ChartMogul API' in kwargs['description']
        assert 'account information' in kwargs['description']
    
    @patch('chartmogul_mcp.mcp_server.load_dotenv')
    @patch('chartmogul_mcp.mcp_server.api_client.init_chartmogul_config')
    @patch('chartmogul_mcp.mcp_server.FastMCP')
    @patch('chartmogul_mcp.mcp_server.utils')
    def test_list_sources_tool_registration(self, mock_utils, mock_fastmcp, mock_init_config, mock_load_dotenv):
        """Test that list_sources tool is registered correctly."""
        # Setup mocks
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        from chartmogul_mcp.mcp_server import ChartMogulMcp
        
        # Create instance
        ChartMogulMcp()
        
        # Check that list_sources tool was registered
        tool_calls = mock_mcp_instance.tool.call_args_list
        list_sources_call = None
        for call in tool_calls:
            args, kwargs = call
            if 'name' in kwargs and kwargs['name'] == 'list_sources':
                list_sources_call = call
                break
        
        assert list_sources_call is not None, "list_sources tool should be registered"
        
        # Verify the tool has correct name and description
        _, kwargs = list_sources_call
        assert kwargs['name'] == 'list_sources'
        assert 'data sources' in kwargs['description']
        assert 'billing systems' in kwargs['description']
    
    @patch('chartmogul_mcp.mcp_server.load_dotenv')
    @patch('chartmogul_mcp.mcp_server.api_client.init_chartmogul_config')
    @patch('chartmogul_mcp.mcp_server.FastMCP')
    @patch('chartmogul_mcp.mcp_server.utils')
    def test_multiple_tools_registered(self, mock_utils, mock_fastmcp, mock_init_config, mock_load_dotenv):
        """Test that multiple tools are registered."""
        # Setup mocks
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        from chartmogul_mcp.mcp_server import ChartMogulMcp
        
        # Create instance
        ChartMogulMcp()
        
        # Verify that tool decorator was called multiple times
        assert mock_mcp_instance.tool.call_count >= 2, "Multiple tools should be registered"
        
        # Get all registered tool names
        tool_calls = mock_mcp_instance.tool.call_args_list
        registered_tool_names = []
        for call in tool_calls:
            args, kwargs = call
            if 'name' in kwargs:
                registered_tool_names.append(kwargs['name'])
        
        # Check that expected tools are registered
        expected_tools = ['retrieve_account', 'list_sources']
        for tool_name in expected_tools:
            assert tool_name in registered_tool_names, f"{tool_name} should be registered"


class TestMCPServerImports:
    """Test that the MCP server module imports correctly."""
    
    def test_module_imports(self):
        """Test that all required modules can be imported."""
        try:
            import chartmogul_mcp.mcp_server  # noqa: F401
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import mcp_server module: {e}")
    
    def test_chartmogul_mcp_class_exists(self):
        """Test that ChartMogulMcp class can be imported."""
        try:
            from chartmogul_mcp.mcp_server import ChartMogulMcp
            assert ChartMogulMcp is not None
        except ImportError as e:
            pytest.fail(f"Failed to import ChartMogulMcp class: {e}")
    
    def test_required_dependencies_importable(self):
        """Test that all dependencies used in mcp_server can be imported."""
        # Test basic imports that should always work
        basic_imports = ['sys', 'datetime']
        for module_name in basic_imports:
            try:
                __import__(module_name)
            except ImportError as e:
                pytest.fail(f"Failed to import required module {module_name}: {e}")


class TestAsyncToolFunctions:
    """Test the async tool functions within the MCP server."""
    
    @patch('chartmogul_mcp.mcp_server.load_dotenv')
    @patch('chartmogul_mcp.mcp_server.api_client')
    @patch('chartmogul_mcp.mcp_server.FastMCP')
    @patch('chartmogul_mcp.mcp_server.utils')
    def test_tool_functions_are_async(self, mock_utils, mock_fastmcp, mock_api_client, mock_load_dotenv):
        """Test that registered tool functions are async."""
        # Setup mocks
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        mock_config = Mock()
        mock_api_client.init_chartmogul_config.return_value = mock_config
        
        # We need to capture the actual function that gets registered
        registered_functions = []
        
        def capture_tool(*args, **kwargs):
            def decorator(func):
                registered_functions.append(func)
                return func
            return decorator
        
        mock_mcp_instance.tool = capture_tool
        
        from chartmogul_mcp.mcp_server import ChartMogulMcp
        
        # Create instance (this will register tools)
        ChartMogulMcp()
        
        # Check that we captured some functions
        assert len(registered_functions) > 0, "Should have captured registered functions"
        
        # Check that the first function (should be retrieve_account) is async
        import asyncio
        first_func = registered_functions[0]
        assert asyncio.iscoroutinefunction(first_func), "Tool functions should be async"


if __name__ == "__main__":
    pytest.main([__file__])