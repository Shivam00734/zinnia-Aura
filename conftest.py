"""
Global pytest configuration and fixtures with tag integration
"""
import pytest
import allure
import yaml
import os
import sys
import platform
from pathlib import Path
from typing import Dict, Any

def pytest_configure(config):
    """Configure pytest with custom settings"""
    # Set up allure environment properties
    if not os.path.exists("allure-results"):
        os.makedirs("allure-results")
    
    # Create environment properties for allure
    with open("allure-results/environment.properties", "w") as f:
        f.write(f"Environment={os.getenv('TEST_ENV', 'dev')}\n")
        f.write(f"Python.Version={sys.version}\n")
        f.write(f"Platform={platform.system()}\n")

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add custom behavior"""
    # Add markers based on test file location
    for item in items:
        # Add suite markers based on file path
        if "smoke_tests" in str(item.fspath):
            item.add_marker(pytest.mark.smoke)
        elif "regression_tests" in str(item.fspath):
            item.add_marker(pytest.mark.regression)
        
        # Add API/UI markers based on file name
        if "api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        elif "ui" in str(item.fspath):
            item.add_marker(pytest.mark.ui)

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--env", 
        action="store", 
        default="dev",
        help="Test environment: dev, staging, prod"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser for UI tests: chrome, firefox"
    )
    parser.addoption(
        "--suite",
        action="store",
        help="Test suite to run: smoke, regression"
    )
    parser.addoption(
        "--tags",
        action="store",
        help="Comma-separated list of tags to include"
    )

@pytest.fixture(scope="session")
def test_config(request):
    """Load test configuration"""
    env = request.config.getoption("--env")
    
    # Default configuration
    config = {
        'environments': {
            'dev': {
                'api_base_url': 'https://dummyjson.com/',
                'ui_base_url': 'https://dev.example.com',
                'timeout': 30
            },
            'staging': {
                'api_base_url': 'https://staging-api.example.com',
                'ui_base_url': 'https://staging.example.com', 
                'timeout': 60
            },
            'prod': {
                'api_base_url': 'https://api.example.com',
                'ui_base_url': 'https://example.com',
                'timeout': 120
            }
        }
    }
    
    # Set environment-specific configuration
    config['current_env'] = env
    config['env_config'] = config['environments'][env]
    
    return config

@pytest.fixture(scope="session")
def api_config(test_config):
    """API configuration fixture"""
    return {
        'base_url': test_config['env_config']['api_base_url'],
        'timeout': test_config['env_config']['timeout'],
        'headers': {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    }

@pytest.fixture(scope="session")
def ui_config(test_config, request):
    """UI configuration fixture"""
    browser = request.config.getoption("--browser")
    return {
        'base_url': test_config['env_config']['ui_base_url'],
        'browser': browser,
        'timeout': test_config['env_config']['timeout']
    }

@pytest.fixture(scope="function")
def allure_environment():
    """Set up allure test environment information"""
    allure.environment(
        Environment=os.getenv('TEST_ENV', 'dev'),
        Browser=os.getenv('BROWSER', 'chrome'),
        Platform=os.getenv('PLATFORM', 'Windows')
    )

@pytest.fixture(autouse=True)
def test_setup_teardown(request):
    """Automatic setup and teardown for all tests"""
    # Setup
    test_name = request.node.name
    allure.dynamic.description(f"Test: {test_name}")
    
    yield
    
    # Teardown
    # Clean up any test artifacts if needed
    pass

@pytest.fixture(scope="function")
def api_client(api_config):
    """HTTP client fixture for API tests"""
    import requests
    
    class APIClient:
        def __init__(self, config):
            self.base_url = config['base_url']
            self.timeout = config['timeout']
            self.headers = config['headers']
        
        def get(self, endpoint, **kwargs):
            return requests.get(f"{self.base_url}{endpoint}", 
                              headers=self.headers, 
                              timeout=self.timeout, 
                              **kwargs)
        
        def post(self, endpoint, **kwargs):
            return requests.post(f"{self.base_url}{endpoint}", 
                               headers=self.headers, 
                               timeout=self.timeout, 
                               **kwargs)
        
        def put(self, endpoint, **kwargs):
            return requests.put(f"{self.base_url}{endpoint}", 
                              headers=self.headers, 
                              timeout=self.timeout, 
                              **kwargs)
        
        def delete(self, endpoint, **kwargs):
            return requests.delete(f"{self.base_url}{endpoint}", 
                                 headers=self.headers, 
                                 timeout=self.timeout, 
                                 **kwargs)
    
    return APIClient(api_config)

# Pytest hooks for test result handling
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for allure reporting"""
    if call.when == 'call':
        if call.excinfo is not None:
            # Test failed
            allure.attach(
                str(call.excinfo.value), 
                name="Error Details", 
                attachment_type=allure.attachment_type.TEXT
            )

def pytest_sessionstart(session):
    """Called after the Session object has been created"""
    print("\n" + "="*50)
    print("Starting Test Execution")
    print("="*50)

def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished"""
    print("\n" + "="*50)
    print("Test Execution Completed")
    print(f"Exit Status: {exitstatus}")
    print("="*50)
