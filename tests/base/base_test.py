"""
Base test classes for smoke and regression test suites with tag integration
"""
import pytest
import allure
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class TestTags:
    """
    Centralized test tag definitions for dashboard integration
    """
    
    # Smoke test tags
    SMOKE_TAGS = {
        'critical': 'Critical functionality that must work',
        'health_check': 'Basic system health verification',
        'authentication': 'User authentication flows',
        'core_api': 'Core API endpoints',
        'main_ui': 'Main UI components',
        'login': 'Login functionality',
        'navigation': 'Basic navigation'
    }
    
    # Regression test tags
    REGRESSION_TAGS = {
        'comprehensive': 'Complete feature testing',
        'crud_operations': 'Create, Read, Update, Delete operations',
        'data_validation': 'Data integrity and validation',
        'edge_cases': 'Edge case scenarios',
        'performance': 'Performance related tests',
        'integration': 'Integration between components',
        'workflow': 'Complete user workflows',
        'error_handling': 'Error handling scenarios',
        'cross_browser': 'Cross-browser compatibility',
        'responsive': 'Responsive design testing'
    }
    
    # API specific tags
    API_TAGS = {
        'endpoints': 'API endpoint testing',
        'security': 'API security testing',
        'payload': 'Request/Response payload validation',
        'status_codes': 'HTTP status code validation',
        'rate_limiting': 'API rate limiting tests',
        'versioning': 'API versioning tests'
    }
    
    # UI specific tags
    UI_TAGS = {
        'forms': 'Form functionality',
        'tables': 'Data table operations',
        'modals': 'Modal dialog testing',
        'navigation': 'UI navigation testing',
        'accessibility': 'Accessibility compliance',
        'visual': 'Visual regression testing'
    }
    
    @classmethod
    def get_tags_for_test_type(cls, test_type: str) -> Dict[str, str]:
        """Get tags available for a specific test type"""
        tag_mapping = {
            'smoke': cls.SMOKE_TAGS,
            'regression': cls.REGRESSION_TAGS,
            'api': {**cls.API_TAGS, **cls.SMOKE_TAGS, **cls.REGRESSION_TAGS},
            'ui': {**cls.UI_TAGS, **cls.SMOKE_TAGS, **cls.REGRESSION_TAGS}
        }
        return tag_mapping.get(test_type, {})
    
    @classmethod
    def get_all_tags(cls) -> Dict[str, Dict[str, str]]:
        """Get all tags organized by category"""
        return {
            'smoke': cls.SMOKE_TAGS,
            'regression': cls.REGRESSION_TAGS,
            'api': cls.API_TAGS,
            'ui': cls.UI_TAGS
        }

class BaseTest(ABC):
    """
    Abstract base class for all test types
    """
    
    def setup_method(self, method):
        """Setup method called before each test method"""
        self.test_name = method.__name__
        self.setup_test_environment()
    
    def teardown_method(self, method):
        """Teardown method called after each test method"""
        self.cleanup_test_environment()
    
    def setup_test_environment(self):
        """Setup test environment - override in subclasses if needed"""
        pass
    
    def cleanup_test_environment(self):
        """Cleanup test environment - override in subclasses if needed"""
        pass
    
    @abstractmethod
    def get_test_data(self) -> Dict[str, Any]:
        """Get test data specific to the test type"""
        pass

class SmokeTestBase(BaseTest):
    """
    Base class for smoke tests - quick, critical functionality tests
    """
    
    def setup_test_environment(self):
        """Setup for smoke tests - minimal setup"""
        super().setup_test_environment()
        allure.dynamic.label("suite", "Smoke Tests")
        allure.dynamic.label("priority", "P0")
        allure.dynamic.label("test_type", "smoke")
    
    def get_test_data(self) -> Dict[str, Any]:
        """Get minimal test data for smoke tests"""
        return {
            "test_type": "smoke",
            "timeout": 60,
            "priority": "P0",
            "tags": TestTags.SMOKE_TAGS
        }

class RegressionTestBase(BaseTest):
    """
    Base class for regression tests - comprehensive functionality tests
    """
    
    def setup_test_environment(self):
        """Setup for regression tests - comprehensive setup"""
        super().setup_test_environment()
        allure.dynamic.label("suite", "Regression Tests")
        allure.dynamic.label("priority", "P1")
        allure.dynamic.label("test_type", "regression")
    
    def get_test_data(self) -> Dict[str, Any]:
        """Get comprehensive test data for regression tests"""
        return {
            "test_type": "regression",
            "timeout": 300,
            "priority": "P1",
            "tags": TestTags.REGRESSION_TAGS
        }

class APITestMixin:
    """
    Mixin class for API-specific test functionality
    """
    
    def setup_api_client(self):
        """Setup API client configuration"""
        self.base_url = os.getenv('API_BASE_URL', 'https://dummyjson.com/')
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def validate_api_response(self, response, expected_status=200):
        """Validate basic API response"""
        assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
        return response.json() if response.content else {}

class UITestMixin:
    """
    Mixin class for UI-specific test functionality
    """
    
    def setup_webdriver(self):
        """Setup WebDriver configuration"""
        # WebDriver setup will be implemented based on existing selenium setup
        pass
    
    def cleanup_webdriver(self):
        """Cleanup WebDriver"""
        pass

class DatabaseTestMixin:
    """
    Mixin class for database-specific test functionality
    """
    
    def setup_database_connection(self):
        """Setup database connection"""
        # Database setup will be implemented based on existing DB configuration
        pass
    
    def cleanup_database_connection(self):
        """Cleanup database connection"""
        pass
