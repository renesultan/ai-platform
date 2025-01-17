from urllib import request, error

class ModelResponse:
    """
    A simple class to hold model responses.
    """
    def __init__(self, text, error=None):
        self.text = text
        self.error = error

    def __str__(self):
        """
        Makes it easy to print responses
        """
        if self.error:
            return f"Error: {self.error}"
        return f"Response: {self.text}"
    
class ModelInterface:
    """
    Simple interface for AI model interactions.
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def generate(self, query):
        """
        Generate a response for the given query.
        Currently making a test HTTP GET request to httpbin.
        """
        try:
            # Make a simple GET request to httpbin
            url = "https://httpbin.org/get"

            # Create a Request object
            req = request.Request(url)

            # Open the URL and get the response
            with request.urlopen(req) as response:
                # Read the response and decode from bytes to string
                data = response.read().decode('utf-8')
                return ModelResponse(f"Got response: {data}")
            
        except error.URLError as e:
            # Handle network-related errors
            return ModelResponse(text="", error=f"Network error: {str(e)}")
        except Exception as e:
            # Handle any other errors
            return ModelResponse(text="", error=f"Unexpected error: {str(e)}")