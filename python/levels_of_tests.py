"""
This module demonstrates different levels of testing in software development
through practical examples.
"""

import unittest
from unittest.mock import Mock, patch
import requests
import json

# 1. Unit Test Example
# Tests a single function/unit in isolation
class CalculatorTest(unittest.TestCase):
    def test_add_numbers(self):
        """Unit test: Testing a single function in isolation"""
        def add_numbers(a, b):
            return a + b
            
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)

# 2. Integration Test Example 
# Tests interaction between multiple components
class UserServiceIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.db = Mock()  # Mock database
        self.email_service = Mock()  # Mock email service
        
    def test_user_registration(self):
        """Integration test: Testing interaction between user service, DB and email service"""
        class UserService:
            def __init__(self, db, email_service):
                self.db = db
                self.email_service = email_service
                
            def register_user(self, username, email):
                # Save to DB
                self.db.save_user(username, email)
                # Send welcome email
                self.email_service.send_welcome_email(email)
                return True
        
        # Test the integration
        user_service = UserService(self.db, self.email_service)
        result = user_service.register_user("john_doe", "john@example.com")
        
        # Verify all components interacted correctly
        self.assertTrue(result)
        self.db.save_user.assert_called_once_with("john_doe", "john@example.com")
        self.email_service.send_welcome_email.assert_called_once_with("john@example.com")

# 3. End-to-End Test Example
# Tests entire system flow from start to finish
class EcommerceE2ETest(unittest.TestCase):
    @patch('requests.post')
    @patch('requests.get')
    def test_complete_purchase_flow(self, mock_get, mock_post):
        """End-to-end test: Testing complete purchase flow in an e-commerce system"""
        # Mock API responses
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "product": {"id": 1, "name": "Laptop", "price": 999.99}
        }
        
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"order_id": "12345"}
        
        # 1. User logs in
        login_response = requests.post(
            'https://api.example.com/login',
            json={"username": "user", "password": "pass"}
        )
        self.assertEqual(login_response.status_code, 200)
        
        # 2. User browses product
        product_response = requests.get('https://api.example.com/products/1')
        self.assertEqual(product_response.status_code, 200)
        product = product_response.json()['product']
        
        # 3. User adds to cart and checks out
        order_response = requests.post(
            'https://api.example.com/orders',
            json={
                "product_id": product['id'],
                "quantity": 1,
                "shipping_address": "123 Main St"
            }
        )
        self.assertEqual(order_response.status_code, 200)
        self.assertIn('order_id', order_response.json())

if __name__ == '__main__':
    unittest.main()

"""
Key Differences:

1. Unit Tests:
   - Test individual components in isolation
   - Fast execution
   - No external dependencies
   - Easiest to write and maintain

2. Integration Tests:
   - Test interaction between components
   - May use mock objects for external services
   - More complex setup
   - Slower than unit tests

3. End-to-End Tests:
   - Test complete business flows
   - Test real system integration
   - Most complex setup
   - Slowest to execute
   - Most similar to real user behavior
"""
