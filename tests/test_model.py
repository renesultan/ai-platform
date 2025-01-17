import unittest
from src.ai_platform.model import ModelInterface, ModelResponse

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

class TestModelInterface(unittest.TestCase):
    """
    Test cases for the ModelInterface class
    """

    def test_basic_request(self):
        """
        Test that we can make a basic HTTP request
        """
        model = ModelInterface(api_key="test-key")
        response = model.generate("test query")
        self.assertIsNotNone(response.text)
        self.assertIsNone(response.error)

    def test_response_contains_data(self):
        """
        Test that our response contains actual data
        """
        model = ModelInterface(api_key="test-key")
        response = model.generate("test query")
        self.assertIn('httpbin', response.text)

if __name__ == '__main__':
    unittest.main()