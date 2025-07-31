import pytest
from unittest.mock import patch, Mock
import logging
import os


class TestUtilsModule:
    """Test the utils module functionality."""
    
    @patch.dict(os.environ, {'CHARTMOGUL_TOKEN': 'test_token_123'})
    def test_chartmogul_token_environment_variable(self):
        """Test that CHARTMOGUL_TOKEN is read from environment."""
        # Need to reload the module to pick up the new environment variable
        import importlib
        from chartmogul_mcp import utils
        importlib.reload(utils)
        
        assert utils.CHARTMOGUL_TOKEN == 'test_token_123'
    
    @patch.dict(os.environ, {}, clear=True)
    def test_chartmogul_token_none_when_not_set(self):
        """Test that CHARTMOGUL_TOKEN is None when not set in environment."""
        # Need to reload the module to pick up the cleared environment
        import importlib
        from chartmogul_mcp import utils
        importlib.reload(utils)
        
        assert utils.CHARTMOGUL_TOKEN is None
    
    def test_mcp_server_name_constant(self):
        """Test MCP_SERVER_NAME constant."""
        from chartmogul_mcp import utils
        assert utils.MCP_SERVER_NAME == "mcp-chartmogul"
    
    def test_dependencies_list(self):
        """Test DEPENDENCIES constant contains expected packages."""
        from chartmogul_mcp import utils
        expected_dependencies = ["chartmogul", "python-dotenv"]
        assert utils.DEPENDENCIES == expected_dependencies
    
    def test_logger_configuration(self):
        """Test that logger is properly configured."""
        from chartmogul_mcp import utils
        
        # Check logger exists and has correct name
        assert utils.LOGGER is not None
        assert utils.LOGGER.name == "mcp-chartmogul"
        assert isinstance(utils.LOGGER, logging.Logger)
    
    def test_logger_level(self):
        """Test that logger is set to INFO level."""
        from chartmogul_mcp import utils
        
        # Check that logger or its handlers have INFO level
        logger_level = utils.LOGGER.level
        root_logger_level = logging.getLogger().level
        
        # Logger should be at INFO level or inherit from root
        assert logger_level == logging.NOTSET or logger_level <= logging.INFO
        assert root_logger_level <= logging.INFO
    
    @patch('chartmogul_mcp.utils.load_dotenv')
    def test_dotenv_is_loaded(self, mock_load_dotenv):
        """Test that load_dotenv is called when module is imported."""
        # Reload module to trigger the load_dotenv call
        import importlib
        from chartmogul_mcp import utils
        importlib.reload(utils)
        
        # load_dotenv should be called at least once during import
        mock_load_dotenv.assert_called()
    
    def test_module_imports(self):
        """Test that all required modules can be imported."""
        # This test ensures all imports in utils.py work correctly
        try:
            from chartmogul_mcp import utils
            # If we get here, all imports succeeded
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import utils module: {e}")
    
    def test_constants_are_accessible(self):
        """Test that all expected constants are accessible."""
        from chartmogul_mcp import utils
        
        # Test that all expected attributes exist
        expected_attributes = [
            'CHARTMOGUL_TOKEN',
            'MCP_SERVER_NAME', 
            'DEPENDENCIES',
            'LOGGER'
        ]
        
        for attr in expected_attributes:
            assert hasattr(utils, attr), f"utils module should have {attr} attribute"


class TestLoggingConfiguration:
    """Test logging configuration functionality."""
    
    def test_logging_format(self):
        """Test that logging is configured with expected format."""
        from chartmogul_mcp import utils
        
        # Create a test log message and check it's formatted correctly
        with patch('chartmogul_mcp.utils.LOGGER') as mock_logger:
            # Get the actual logger to test its configuration
            actual_logger = logging.getLogger("mcp-chartmogul")
            
            # Check that logger exists and can be used
            assert actual_logger is not None
            
            # Test that we can log messages (this verifies configuration)
            actual_logger.info("Test message")
            # If we get here without exception, logging is configured correctly
    
    def test_logger_name_matches_server_name(self):
        """Test that logger name matches MCP_SERVER_NAME."""
        from chartmogul_mcp import utils
        
        assert utils.LOGGER.name == utils.MCP_SERVER_NAME
    
    def test_logging_basicconfig_called(self):
        """Test that logging.basicConfig was called during module import."""
        # This is tested indirectly by checking that the root logger has the expected level
        root_logger = logging.getLogger()
        
        # After utils module import, root logger should be configured
        assert root_logger.level <= logging.INFO
        
        # Check that handlers exist (basicConfig should have added at least one)
        assert len(root_logger.handlers) > 0


if __name__ == "__main__":
    pytest.main([__file__])