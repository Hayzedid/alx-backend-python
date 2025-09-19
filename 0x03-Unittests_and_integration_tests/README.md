# Unittests and Integration Tests

This project demonstrates unit testing and integration testing in Python using the `unittest` framework, `parameterized` for test parameterization, and `unittest.mock` for mocking external dependencies.

## Project Structure

```
0x03-Unittests_and_integration_tests/
├── utils.py              # Utility functions for GitHub org client
├── client.py             # GitHub organization client implementation
├── fixtures.py           # Test fixtures and sample data
├── test_utils.py         # Unit tests for utils module
├── test_client.py        # Unit and integration tests for client module
└── README.md            # This file
```

## Files Description

### utils.py
Contains utility functions:
- `access_nested_map()`: Access nested dictionary values using a path
- `get_json()`: Fetch JSON data from a URL
- `memoize()`: Decorator for memoizing method results

### client.py
Contains the `GithubOrgClient` class:
- `org()`: Get organization information
- `_public_repos_url()`: Get public repositories URL
- `repos_payload()`: Get repositories payload
- `public_repos()`: Get list of public repositories
- `has_license()`: Check if a repository has a specific license

### test_utils.py
Unit tests for the utils module:
- `TestAccessNestedMap`: Tests for nested map access with valid and invalid inputs
- `TestGetJson`: Tests for JSON fetching with mocked HTTP requests
- `TestMemoize`: Tests for memoization decorator functionality

### test_client.py
Unit and integration tests for the client module:
- `TestGithubOrgClient`: Unit tests for individual methods
- `TestIntegrationGithubOrgClient`: Integration tests with mocked external calls

## Testing Concepts Demonstrated

### Unit Testing
- Testing individual functions and methods in isolation
- Using mocks to isolate code under test from external dependencies
- Testing both success and failure scenarios
- Parameterized testing for multiple input scenarios

### Integration Testing
- Testing complete workflows end-to-end
- Mocking only external dependencies (HTTP requests)
- Testing interactions between different components
- Using fixtures for consistent test data

### Mocking Techniques
- `@patch` decorator for method-level mocking
- `patch` context manager for scoped mocking
- `PropertyMock` for mocking properties
- `side_effect` for complex mocking scenarios

## Running Tests

To run all tests:
```bash
python -m unittest discover
```

To run specific test files:
```bash
python -m unittest test_utils.py
python -m unittest test_client.py
```

To run with verbose output:
```bash
python -m unittest -v
```

## Dependencies

- Python 3.7+
- unittest (built-in)
- parameterized
- requests
- unittest.mock (built-in)

## Key Learning Objectives

1. **Unit vs Integration Tests**: Understanding when to use each type of test
2. **Mocking**: How to mock external dependencies and internal methods
3. **Parameterization**: Using parameterized tests for multiple scenarios
4. **Fixtures**: Managing test data and setup/teardown
5. **Test Organization**: Structuring tests for maintainability and clarity
