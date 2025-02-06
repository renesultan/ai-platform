"""
Common data types used across the AI platform
"""

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