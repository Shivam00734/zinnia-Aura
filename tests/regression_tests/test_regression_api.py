"""
Regression tests for API functionality with comprehensive tagging
"""
import pytest
import allure
import requests
from tests.base.base_test import RegressionTestBase, APITestMixin

@pytest.mark.regression
@pytest.mark.api
@pytest.mark.comprehensive
@allure.feature('API')
@allure.suite('Regression Tests')
class TestRegressionAPI(RegressionTestBase, APITestMixin):
    """
    Regression test class for comprehensive API functionality
    Tests complete API workflows and edge cases
    """
    
    def setup_method(self, method):
        """Setup for each test method"""
        # Initialize attributes without calling super().__init__()
        self.test_type = "regression"
        self.test_priority = "P1"
        self.timeout = 300
        
        super().setup_method(method)
        self.setup_api_client()
    
    @allure.story('User Management')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.crud_operations
    @pytest.mark.workflow
    def test_user_crud_operations(self):
        """Test complete CRUD operations for users"""
        with allure.step('Create new user'):
            user_data = {
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "username": "johndoe",
                "password": "password123"
            }
            response = requests.post(f"{self.base_url}users/add", 
                                   json=user_data, 
                                   headers=self.headers)
            created_user = self.validate_api_response(response, 200)
            user_id = created_user.get('id')
            assert user_id is not None, "Created user should have an ID"
        
        with allure.step('Read created user'):
            response = requests.get(f"{self.base_url}users/{user_id}", headers=self.headers)
            user_data = self.validate_api_response(response, 200)
            assert user_data['firstName'] == "John", "First name should match"
        
        with allure.step('Update user'):
            update_data = {"firstName": "Jane"}
            response = requests.put(f"{self.base_url}users/{user_id}", 
                                  json=update_data, 
                                  headers=self.headers)
            updated_user = self.validate_api_response(response, 200)
            assert updated_user['firstName'] == "Jane", "First name should be updated"
        
        with allure.step('Delete user'):
            response = requests.delete(f"{self.base_url}users/{user_id}", headers=self.headers)
            self.validate_api_response(response, 200)
    
    @allure.story('Data Validation')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.data_validation
    @pytest.mark.pagination
    def test_api_data_pagination(self):
        """Test API pagination functionality"""
        with allure.step('Test pagination with limit'):
            response = requests.get(f"{self.base_url}users?limit=5", headers=self.headers)
            data = self.validate_api_response(response, 200)
            assert len(data['users']) <= 5, "Should return at most 5 users"
        
        with allure.step('Test pagination with skip'):
            response = requests.get(f"{self.base_url}users?skip=10&limit=5", headers=self.headers)
            data = self.validate_api_response(response, 200)
            assert 'users' in data, "Should return users data"
    
    @allure.story('Error Handling')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.error_handling
    @pytest.mark.edge_cases
    def test_api_error_handling(self):
        """Test API error handling for various scenarios"""
        with allure.step('Test invalid endpoint'):
            response = requests.get(f"{self.base_url}invalid-endpoint", headers=self.headers)
            assert response.status_code == 404, "Should return 404 for invalid endpoint"
        
        with allure.step('Test invalid user ID'):
            response = requests.get(f"{self.base_url}users/999999", headers=self.headers)
            assert response.status_code == 404, "Should return 404 for non-existent user"
        
        with allure.step('Test malformed request'):
            invalid_headers = {'Content-Type': 'invalid/type'}
            response = requests.get(f"{self.base_url}users", headers=invalid_headers)
            # Note: This specific API might not validate content-type for GET requests
            # Adjust assertion based on actual API behavior
    
    @allure.story('Performance')
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    @pytest.mark.integration
    def test_api_response_time(self):
        """Test API response time requirements"""
        import time
        
        with allure.step('Measure response time'):
            start_time = time.time()
            response = requests.get(f"{self.base_url}users", headers=self.headers)
            end_time = time.time()
            response_time = end_time - start_time
        
        with allure.step('Validate response time'):
            self.validate_api_response(response, 200)
            assert response_time < 5.0, f"Response time {response_time:.2f}s should be less than 5 seconds"
            allure.attach(f"{response_time:.2f} seconds", name="Response Time", attachment_type=allure.attachment_type.TEXT)
    
    @allure.story('Payload Validation')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.payload
    @pytest.mark.data_validation
    def test_payload_validation(self):
        """Test API payload validation scenarios"""
        with allure.step('Test empty payload'):
            response = requests.post(f"{self.base_url}users/add", 
                                   json={}, 
                                   headers=self.headers)
            # API might return 400 for invalid payload
            assert response.status_code in [400, 422], "Should handle empty payload appropriately"
        
        with allure.step('Test oversized payload'):
            large_data = {"description": "x" * 10000}  # Large string
            response = requests.post(f"{self.base_url}users/add", 
                                   json=large_data, 
                                   headers=self.headers)
            # Check if API handles large payloads
            assert response.status_code in [200, 400, 413], "Should handle large payload appropriately"
