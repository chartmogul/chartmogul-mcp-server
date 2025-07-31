# ChartMogul MCP Server Tests

This directory contains comprehensive tests for the ChartMogul MCP Server project.

## Test Structure

```
tests/
├── __init__.py                 # Test package marker
├── test_api_client.py         # Tests for API client functions and decorator
├── test_utils.py              # Tests for utility functions
├── test_mcp_server.py         # Tests for MCP server functionality
├── test_integration.py        # Integration tests
├── test_standalone.py         # Standalone tests (no external deps)
└── README.md                  # This file
```

## Test Categories

### 1. Unit Tests (`test_*.py`)
- **`test_api_client.py`**: Tests all API client functions and the error handling decorator
- **`test_utils.py`**: Tests utility functions, configuration, and logging
- **`test_mcp_server.py`**: Tests MCP server initialization and tool registration

### 2. Integration Tests (`test_integration.py`)
- End-to-end workflow testing
- Module interaction testing
- Configuration and environment variable testing
- Error propagation testing

### 3. Standalone Tests (`test_standalone.py`)
- Tests that don't require external dependencies
- Can be run without pytest or chartmogul package
- Useful for basic functionality verification

## Running Tests

### Option 1: Using uv (recommended)
```bash
# Install dependencies
uv sync --dev

# Run all tests with coverage
uv run pytest tests/ --cov=chartmogul_mcp --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_api_client.py -v

# Run specific test
uv run pytest tests/test_api_client.py::TestHandleApiErrorsDecorator::test_decorator_success_case -v

# Run linting
uv run ruff check chartmogul_mcp/ tests/

# Run code formatting
uv run black chartmogul_mcp/ tests/

# Run type checking
uv run mypy chartmogul_mcp/ --ignore-missing-imports
```

### Option 2: Using pytest directly (requires dependencies)
```bash
# Install test dependencies first
pip install -e ".[test]"

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=chartmogul_mcp --cov-report=term-missing
```

### Option 3: Using standalone tests (no dependencies required)
```bash
# Run standalone tests only
python3 tests/test_standalone.py
```

## Test Dependencies

The tests require the following packages:
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `pytest-mock>=3.10.0` - Mocking utilities
- `pytest-asyncio>=0.21.0` - Async test support

Install with uv (recommended):
```bash
uv sync --dev
```

Or using pip with optional dependencies:
```bash
pip install -e ".[test]"
```

## Test Configuration

Tests are configured via:
- **`pytest.ini`**: Basic pytest configuration
- **`pyproject.toml`**: Advanced configuration with coverage settings
- **Environment variables**: For testing different configurations

### Key Configuration Options
- Coverage threshold: 70% minimum
- Test discovery: Automatic for `test_*.py` files
- Markers: `unit`, `integration`, `slow`
- Coverage exclusions: Test files, `__pycache__`, pragma comments

## What's Tested

### API Client (`test_api_client.py`)
✅ **Error Handling Decorator**
- Success case handling
- Exception catching and logging
- Return value of None on errors
- Function metadata preservation
- Custom vs default operation names

✅ **Core API Functions**
- `retrieve_account()` - Account information retrieval
- `list_sources()` - Data source listing
- `retrieve_source()` - Single data source retrieval
- `list_customers()` - Customer listing with pagination
- `create_customer()` - Customer creation
- `retrieve_customer()` - Single customer retrieval
- `update_customer()` - Customer updates
- `search_customers()` - Customer search

✅ **Utility Functions**
- `parse_object()` - Object serialization
- `init_chartmogul_config()` - Configuration initialization

### Utils Module (`test_utils.py`)
✅ **Configuration**
- Environment variable loading
- Constants accessibility
- Missing environment variable handling

✅ **Logging**
- Logger configuration
- Log level settings
- Format verification

### MCP Server (`test_mcp_server.py`)
✅ **Initialization**
- Server creation
- Configuration setup
- Tool registration
- Dependency injection

✅ **Tool Registration**
- Multiple tool registration
- Correct tool names and descriptions
- Async function handling

### Integration Tests (`test_integration.py`)
✅ **End-to-End Workflows**
- Complete server initialization
- API call workflows
- Error handling integration

✅ **System Integration**
- Module imports and dependencies
- Configuration propagation
- Logging system integration

## Coverage Goals

The test suite aims for:
- **Minimum 70% code coverage** (enforced)
- **90%+ coverage** for critical paths (api_client decorator)
- **100% coverage** for utility functions

Current coverage areas:
- ✅ Error handling decorator: ~95%
- ✅ API client functions: ~85%
- ✅ Utility functions: ~90%
- ✅ Configuration handling: ~80%

## Test Features

### Mocking Strategy
- **ChartMogul API**: Fully mocked to avoid external dependencies
- **FastMCP**: Mocked for server testing
- **Environment variables**: Patched for configuration testing
- **Logging**: Captured and verified

### Error Simulation
- Network errors
- API errors
- Configuration errors
- Missing dependencies

### Async Testing
- Async tool functions
- MCP server async patterns
- Error handling in async context

## Adding New Tests

When adding new functionality, ensure you:

1. **Add unit tests** for new functions
2. **Update integration tests** if needed
3. **Mock external dependencies**
4. **Test both success and error cases** 
5. **Update coverage expectations**

### Test Template
```python
class TestNewFeature:
    """Test the new feature functionality."""
    
    def test_success_case(self):
        """Test successful operation."""
        # Setup
        # Execute
        # Assert
        pass
    
    def test_error_case(self):
        """Test error handling."""
        # Setup error condition
        # Execute
        # Assert error handling
        pass
```

## Troubleshooting

### Common Issues

**Import Errors**
- Ensure `chartmogul` package is available or properly mocked
- Check Python path includes project root

**Coverage Too Low**  
- Add tests for uncovered code paths
- Check coverage report: `pytest --cov-report=html`

**Async Test Issues**
- Use `@pytest.mark.asyncio` for async tests
- Ensure `pytest-asyncio` is installed

**Mock Issues**
- Use `patch` decorators correctly
- Verify mock call assertions
- Check mock return values

### Getting Help

1. Run standalone tests first: `python3 tests/test_standalone.py`
2. Check syntax: `python3 run_tests.py --syntax-only`
3. Review test output for specific error messages
4. Check coverage report for missed areas

## Contributing

When contributing:
1. Write tests for new functionality
2. Ensure existing tests pass
3. Maintain or improve coverage
4. Update this README if needed