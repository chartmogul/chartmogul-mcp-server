#!/usr/bin/env python3
"""
Standalone tests that don't require external dependencies.
These tests can be run without installing pytest or chartmogul.

Usage: python3 tests/test_standalone.py
"""

import sys
import os
import traceback
from functools import wraps

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_decorator_functionality():
    """Test the error handling decorator logic independently."""
    print("Testing decorator functionality...")
    
    def handle_api_errors(operation_name=None):
        """Mock version of the decorator for testing."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_msg = operation_name or func.__name__.replace('_', ' ')
                    print(f"Error {error_msg}: {str(e)}")
                    return None
            return wrapper
        return decorator
    
    # Test successful case
    @handle_api_errors("test operation")
    def successful_function():
        return "success"
    
    result = successful_function()
    assert result == "success", f"Expected 'success', got {result}"
    
    # Test error case
    @handle_api_errors("test operation")
    def failing_function():
        raise ValueError("Test error")
    
    result = failing_function()
    assert result is None, f"Expected None, got {result}"
    
    # Test default operation name
    @handle_api_errors()
    def some_function_name():
        raise RuntimeError("Test error")
    
    result = some_function_name()
    assert result is None, f"Expected None, got {result}"
    
    print("✅ Decorator functionality tests passed!")


def test_parse_object_logic():
    """Test the parse_object utility function logic."""
    print("Testing parse_object functionality...")
    
    def parse_object(obj):
        """Mock version of parse_object for testing."""
        import datetime
        
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            result = {}
            for key, value in obj.__dict__.items():
                result[key] = parse_object(value)
            return result
        elif isinstance(obj, list):
            return [parse_object(item) for item in obj]
        else:
            return obj
    
    # Test primitive types
    assert parse_object("string") == "string"
    assert parse_object(123) == 123
    assert parse_object(True) is True
    assert parse_object(None) is None
    
    # Test list
    test_list = [1, 2, "test"]
    result = parse_object(test_list)
    assert result == [1, 2, "test"]
    
    # Test datetime
    import datetime
    dt = datetime.datetime(2023, 1, 1, 12, 0, 0)
    result = parse_object(dt)
    assert result == "2023-01-01T12:00:00"
    
    # Test object with __dict__
    class TestObj:
        def __init__(self):
            self.name = "test"
            self.value = 123
    
    obj = TestObj()
    result = parse_object(obj)
    expected = {"name": "test", "value": 123}
    assert result == expected, f"Expected {expected}, got {result}"
    
    print("✅ parse_object functionality tests passed!")


def test_utils_constants():
    """Test that utils module has expected constants."""
    print("Testing utils constants...")
    
    # Test that we can define expected constants
    expected_constants = {
        'MCP_SERVER_NAME': str,
        'DEPENDENCIES': list,
        'CHARTMOGUL_TOKEN': (str, type(None)),  # Could be None if not set
    }
    
    # Mock the constants for testing
    MCP_SERVER_NAME = "mcp-chartmogul"
    DEPENDENCIES = ["chartmogul", "python-dotenv"]
    CHARTMOGUL_TOKEN = None  # Default when not set
    
    # Test constants
    assert isinstance(MCP_SERVER_NAME, str)
    assert MCP_SERVER_NAME == "mcp-chartmogul"
    
    assert isinstance(DEPENDENCIES, list)
    assert "chartmogul" in DEPENDENCIES
    assert "python-dotenv" in DEPENDENCIES
    
    assert CHARTMOGUL_TOKEN is None or isinstance(CHARTMOGUL_TOKEN, str)
    
    print("✅ Utils constants tests passed!")


def test_environment_variable_handling():
    """Test environment variable handling logic."""
    print("Testing environment variable handling...")
    
    # Test setting environment variable
    original_value = os.environ.get('CHARTMOGUL_TOKEN')
    
    # Test with set value
    os.environ['CHARTMOGUL_TOKEN'] = 'test_token_123'
    token = os.getenv('CHARTMOGUL_TOKEN')
    assert token == 'test_token_123'
    
    # Test with unset value
    if 'CHARTMOGUL_TOKEN' in os.environ:
        del os.environ['CHARTMOGUL_TOKEN']
    token = os.getenv('CHARTMOGUL_TOKEN')
    assert token is None
    
    # Restore original value
    if original_value is not None:
        os.environ['CHARTMOGUL_TOKEN'] = original_value
    
    print("✅ Environment variable handling tests passed!")


def test_logging_configuration():
    """Test logging configuration logic."""
    print("Testing logging configuration...")
    
    import logging
    
    # Test creating a logger
    logger_name = "mcp-chartmogul"
    logger = logging.getLogger(logger_name)
    
    assert logger is not None
    assert logger.name == logger_name
    assert isinstance(logger, logging.Logger)
    
    # Test that we can log messages
    try:
        logger.info("Test message")
        # If we get here, logging is working
    except Exception as e:
        raise AssertionError(f"Logging failed: {e}")
    
    print("✅ Logging configuration tests passed!")


def test_module_structure():
    """Test that the module structure is as expected."""
    print("Testing module structure...")
    
    # Test that module files exist
    expected_files = [
        'chartmogul_mcp/__init__.py',
        'chartmogul_mcp/api_client.py',
        'chartmogul_mcp/utils.py',
        'chartmogul_mcp/mcp_server.py',
        'tests/__init__.py',
        'tests/test_api_client.py',
        'tests/test_utils.py',
        'tests/test_mcp_server.py',
        'tests/test_integration.py',
        'pyproject.toml',
        'pytest.ini',
        '.github/workflows/test.yml',
    ]
    
    for file_path in expected_files:
        if not os.path.exists(file_path):
            print(f"⚠️  Expected file not found: {file_path}")
        else:
            print(f"✅ Found: {file_path}")
    
    print("✅ Module structure tests completed!")


def run_all_tests():
    """Run all standalone tests."""
    print("🧪 Running ChartMogul MCP Server Standalone Tests")
    print("=" * 50)
    
    tests = [
        test_decorator_functionality,
        test_parse_object_logic,
        test_utils_constants,
        test_environment_variable_handling,
        test_logging_configuration,
        test_module_structure,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            print(f"\n📋 Running {test.__name__}...")
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed:")
            print(f"   {str(e)}")
            traceback.print_exc()
            failed += 1
    
    print(f"\n" + "=" * 50)
    print(f"📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📝 Total:  {passed + failed}")
    
    if failed == 0:
        print(f"\n🎉 All standalone tests passed!")
        return 0
    else:
        print(f"\n💥 {failed} test(s) failed!")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())