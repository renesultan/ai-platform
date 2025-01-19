"""
Interface for AI model interactions.
"""

from dotenv import load_dotenv
import openai
import os

from ..common.types import ModelResponse
    
class ModelInterface:
    """
    Simple interface for AI model interactions.
    """
    def __init__(self, api_key=None):
        """
        Initialize the model interface with API keys.
        If no key is provided, attempts to load from environment.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')

        if not self.api_key:
            raise ValueError("API key must be provided or set in OPENAI_API_KEY environment variable")
        
        # Assign api_key to openai.api_key
        openai.api_key = self.api_key

    def generate(self, query):
        """
        Generate a response for the given query.
        Currently using OpenAI's ChatCompletion API.
        """
        try:
            # Call openai's ChatCompletion endpoint
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}]
            )

            # Validate the response structure
            if "choices" not in response or not response["choices"]:
                # Return an error ModelResponse if no choices are provided
                return ModelResponse(
                    text="",
                    error="Empty or malformed response from OpenAI"
                )

            # Extract the text from the response
            response_text = response['choices'][0]['message']['content']
            return ModelResponse(text=response_text)

        except Exception as e:
            # Handle errors and return an error response
            return ModelResponse(text="", error=f"API error: {str(e)}")