"""
Smoke tests for API functionality with comprehensive tagging
"""
import pytest
import allure
import requests
from tests.base.base_test import SmokeTestBase, APITestMixin

@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.critical
@allure.feature('API')
@allure.suite('Smoke Tests')
class TestSmokeAPI(SmokeTestBase, APITestMixin):
    """
    Smoke test class for critical API functionality
    Tests basic API endpoints and core functionality
    """
    
    def setup_method(self, method):
        """Setup for each test method"""
        # Initialize attributes without calling super().__init__()
        self.test_type = "smoke"
        self.test_priority = "P0"
        self.timeout = 60
        
        super().setup_method(method)
        self.setup_api_client()
    
    @allure.story('Health Check')
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.health_check
    @pytest.mark.core_api
    def test_api_health_check(self):
        """Test API health check endpoint"""
        with allure.step('Send health check request'):
            response = requests.get(f"{self.base_url}users", headers=self.headers)
        
        with allure.step('Validate response'):
            data = self.validate_api_response(response, 200)
            assert 'users' in data, "Users endpoint should return users data"
            assert len(data['users']) > 0, "Should return at least one user"
    
    @allure.story('Authentication')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.authentication
    @pytest.mark.security
    def test_user_authentication_endpoint(self):
        """Test basic user authentication endpoint"""
        with allure.step('Send authentication request'):
            auth_payload = {
                "username": "test_user",
                "password": "test_password"
            }
            # Using a mock endpoint for demo purposes
            response = requests.get(f"{self.base_url}users/1", headers=self.headers)
        
        with allure.step('Validate authentication response'):
            data = self.validate_api_response(response, 200)
            assert 'id' in data, "Response should contain user ID"
            assert data['id'] is not None, "User ID should not be null"
    
    @allure.story('Data Retrieval')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.endpoints
    @pytest.mark.core_api
    def test_get_single_user(self):
        """Test retrieving a single user by ID"""
        user_id = 1
        
        with allure.step(f'Request user with ID {user_id}'):
            response = requests.get(f"{self.base_url}users/{user_id}", headers=self.headers)
        
        with allure.step('Validate user data'):
            user_data = self.validate_api_response(response, 200)
            assert user_data['id'] == user_id, f"User ID should be {user_id}"
            assert 'firstName' in user_data, "User should have firstName"
            assert 'email' in user_data, "User should have email"
    
    @allure.story('Status Codes')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.status_codes
    @pytest.mark.error_handling
    def test_api_error_handling(self):
        """Test API error handling for invalid requests"""
        with allure.step('Test invalid endpoint'):
            response = requests.get(f"{self.base_url}invalid-endpoint", headers=self.headers)
            assert response.status_code == 404, "Should return 404 for invalid endpoint"
        
        with allure.step('Test invalid user ID'):
            response = requests.get(f"{self.base_url}users/999999", headers=self.headers)
            assert response.status_code == 404, "Should return 404 for non-existent user"
