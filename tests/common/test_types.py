"""
Tests for common data types
"""

import unittest
from src.ai_platform.common import ModelResponse

class TestModelResponse(unittest.TestCase):
    """
    Test cases for the ModelResponse class
    """

    def test_successful_response(self):
        """
        Test creating a successful response
        """
        response = ModelResponse("Hello")
        self.assertEqual(response.text, "Hello")
        self.assertIsNone(response.error)

    def test_error_response(self):
        """
        Test creating an error response
        """
        response = ModelResponse("", error="Something went wrong")
        self.assertEqual(response.text, "")
        self.assertEqual(response.error, "Something went wrong")

    def test_str_successful_response(self):
        """
        Test the string representation of a successful response
        """
        response = ModelResponse("Hello from GPT")
        self.assertEqual(str(response), "Response: Hello from GPT")

    def test_str_error_response(self):
        """
        Test the string representation of an error response
        """
        response = ModelResponse("", error="Something went really wrong")
        self.assertEqual(str(response), "Error: Something went really wrong")

if __name__ == '__main__':
    unittest.main()