import unittest
from unittest.mock import Mock, patch
import pytest

# Let's demonstrate with a real-world example
# Suppose we have a class that processes user data and makes API calls

class UserProcessor:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def get_user_data(self, user_id):
        return self.api_client.fetch_user(user_id)
    
    def process_user(self, user_id):
        user_data = self.get_user_data(user_id)
        return f"Processed user: {user_data['name']}"

# Example using unittest with Mock
class TestUserProcessorWithMock(unittest.TestCase):
    def test_process_user_with_mock(self):
        # Mock approach: We create a mock object to simulate the API client
        mock_api_client = Mock()
        mock_api_client.fetch_user.return_value = {"name": "John Doe"}
        
        processor = UserProcessor(mock_api_client)
        result = processor.process_user(1)
        
        self.assertEqual(result, "Processed user: John Doe")
        mock_api_client.fetch_user.assert_called_once_with(1)

# Example using pytest with Fixture
@pytest.fixture
def api_client():
    # Fixture approach: We create a reusable test double
    class TestApiClient:
        def fetch_user(self, user_id):
            return {"name": "John Doe"}
    
    return TestApiClient()

def test_process_user_with_fixture(api_client):
    processor = UserProcessor(api_client)
    result = processor.process_user(1)
    assert result == "Processed user: John Doe"

"""
Key differences between Mocks and Fixtures:

1. Purpose:
   - Mocks are specifically for simulating behavior and verifying interactions
   - Fixtures are for setting up reusable test dependencies/data

2. Verification:
   - Mocks can verify if and how methods were called (assert_called_with)
   - Fixtures focus on providing consistent test data/state

3. Reusability:
   - Fixtures are easily shared across multiple tests
   - Mocks are typically created within individual tests

4. Complexity:
   - Mocks are more powerful for behavior verification but can be complex
   - Fixtures are simpler but mainly focused on data/dependency provision

5. Scope:
   - Fixtures can have different scopes (function, class, module, session)
   - Mocks are typically scoped to individual tests
"""
