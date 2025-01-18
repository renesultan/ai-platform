import unittest
from unittest.mock import patch
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

class TestModelInterface(unittest.TestCase):
    """
    Test cases for the ModelInterface class

    We'll patch openai.ChatCompletion.create
    so we never hit the real OpenAI API in these tests.
    """

    @patch("src.ai_platform.model.openai.ChatCompletion.create")
    def test_basic_request(self, mock_create):
        """
        Test a basic request to the ChatCompletion endpoint, but mocked.
        """
        # Setup the mock's return value
        mock_create.return_value = {
            "choices": [
                {"message": {"content": "Mocked OpenAI response"}}
            ]
        }

        # Create the model 
        model = ModelInterface(api_key="test-key")

        # Call generate, which we expect to call the mock
        response = model.generate("test query")

        # Verify results
        self.assertEqual(response.text, "Mocked OpenAI response")
        self.assertIsNone(response.error)

        # Confirm ChatCompletion.create was called exactly once 
        # and that it was called with the correct arguments
        mock_create.assert_called_once()
        args, kwargs = mock_create.call_args
        self.assertIn("messages", kwargs)
        self.assertIn("model", kwargs)

    @patch("src.ai_platform.model.openai.ChatCompletion.create")
    def test_error_handling(self, mock_create):
        """
        If the OpenAI call fails, ensure we properly catch the error
        and return a ModelResponse with an error.
        """

        # Setup the mock to raise an Exception
        mock_create.side_effect = Exception("Network failure")

        # Create a model
        model = ModelInterface(api_key="test-key")

        # Call generate, we we expect to raise inside but be caught
        response = model.generate("some query")

        # Verify that we get an error, and no text
        self.assertEqual(response.text, "")
        self.assertIn("Network failure", response.error)

        # Confirm ChatCompletion.create was called once
        mock_create.assert_called_once()

    @patch("src.ai_platform.model.load_dotenv", return_value=None)
    @patch.dict("os.environ", {}, clear=True)
    def test_missing_api_key_raises_value_error(self, mock_load_dotenv):
        """
        Ensure ModelInterface raises ValueError if no API key is provided
        and OPENAI_API_KEY is not set in the environment
        """
        with self.assertRaises(ValueError):
            ModelInterface(api_key=None)

    @patch("src.ai_platform.model.openai.ChatCompletion.create")
    def test_empty_choices_handling(self, mock_create):
        """
        If OpenAI returns an empty or missing choices array,
        ensure we return an appropriate error ModelResponse.
        """
        # Mock a response with empty choices
        mock_create.return_value = {
            "choices": []
        }

        # Create ModelInterface with a test key
        model = ModelInterface(api_key="test-key")

        #  Generate
        response = model.generate("test query")

        # Verify the response text is empty and error contains our message
        self.assertEqual(response.text, "")
        self.assertIn("Empty or malformed response", response.error)

if __name__ == '__main__':
    unittest.main()