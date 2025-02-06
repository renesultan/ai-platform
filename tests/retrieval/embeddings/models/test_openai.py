"""
Tests for OpenAI embedding model implementation.
"""
import unittest
from unittest.mock import Mock, patch

from src.ai_platform.retrieval.embeddings.models.openai import OpenAIEmbedding

class TestOpenAIEmbedding(unittest.TestCase):
    """
    Test cases for OpenAI embedding implementation.
    """

    def setUp(self):
        """
        Set up test cases.
        """
        self.api_key="test-key"
        self.model_name="text-embedding-ada-002"

    @patch('src.ai_platform.retrieval.embeddings.models.openai.OpenAI')
    def test_initialization(self, mock_openai):
        """
         Test model initialization with different parameters.
        """
        # Test default initialization
        model = OpenAIEmbedding(api_key=self.api_key)
        self.assertEqual(model.model_name, self.model_name)
        self.assertEqual(model.dimension, 1536)

        # Test custom model name
        custom_model = OpenAIEmbedding(
            api_key=self.api_key,
            model_name="custom-model"
        )
        self.assertEqual(custom_model.model_name, "custom-model")

    @patch('src.ai_platform.retrieval.embeddings.models.openai.OpenAI')
    def test_generate_single_embedding(self, mock_openai):
        """
        Test generating a single embedding vector.
        """
        # Setup mock response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [Mock(embedding=[0.1, 0.2, 0.3])]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client

        # Create model and generate embedding
        model = OpenAIEmbedding(api_key=self.api_key)
        embedding = model.generate_embedding("test text")

        # Verify embedding
        self.assertEqual(embedding, [0.1, 0.2, 0.3])

        # Verify API call
        mock_client.embeddings.create.assert_called_once_with(
            model=self.model_name,
            input="test text"
        )

    @patch('src.ai_platform.retrieval.embeddings.models.openai.OpenAI')
    def test_generate_multiple_embeddings(self, mock_openai):
        """
        Test generating embeddings for multiple texts.
        """
        # Setup mock response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [
            Mock(embedding=[0.1, 0.2]),
            Mock(embedding=[0.3,0.4])
        ]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client

        # Create model and generate embeddings
        model = OpenAIEmbedding(api_key=self.api_key)
        texts = ["text1", "text2"]
        embeddings = model.generate_embeddings(texts)

        # Verify embeddings
        self.assertEqual(len(embeddings), 2)
        self.assertEqual(embeddings[0], [0.1, 0.2])
        self.assertEqual(embeddings[1], [0.3, 0.4])

        # Verify API call
        mock_client.embeddings.create.assert_called_once_with(
            model=self.model_name,
            input=texts
        )

    def test_input_validation(self):
        """
        Test input validation for embedding generation
        """
        model = OpenAIEmbedding(api_key=self.api_key)

        with self.assertRaises(ValueError) as context:
            model.generate_embedding("")
        self.assertIn("cannot be empty", str(context.exception))

        # Test empty text in batch
        with self.assertRaises(ValueError) as context:
            model.generate_embeddings(["valid", ""])
        self.assertIn("must be non-empty", str(context.exception))

        # Test empty list
        with self.assertRaises(ValueError) as context:
            model.generate_embeddings([])
        self.assertIn("cannot be empty", str(context.exception))

    @patch('src.ai_platform.retrieval.embeddings.models.openai.OpenAI')
    def test_api_error_handling(self, mock_openai):
        """
        Test handling of API errors.
        """
        # Setup mock to raise an exception 
        mock_client = Mock()
        mock_client.embeddings.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client

        model = OpenAIEmbedding(api_key=self.api_key)

        # Test single embedding error
        with self.assertRaises(Exception) as context:
            model.generate_embedding("test")
        self.assertIn("API Error", str(context.exception))

        # Test batch embedding error
        with self.assertRaises(Exception) as context:
            model.generate_embeddings(["test1", "test2"])
        self.assertIn("API Error", str(context.exception))

if __name__ == '__main__':
    unittest.main()
