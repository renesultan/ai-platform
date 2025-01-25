"""
Tests for embedding interfaces and factory.
Tests the contract of the abstract interface and factory behavior,
not specific implementations.
"""
import unittest
from typing import List

from src.ai_platform.retrieval.embeddings.interfaces import (
    EmbeddingModel,
    EmbeddingModelFactory
)

class MockEmbeddingModel(EmbeddingModel):
    """
    Mock implementation of EmbeddingModel for testing interface contract.
    """

    def __init__(self, dimension: int = 3):
        self._dimension = dimension

    def generate_embedding(self, text:str) -> List[float]:
        if not text.strip():
            raise ValueError("Empty text")
        return [0.1] * self._dimension
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            raise ValueError("Empty text list")
        if any(not text.strip() for text in texts):
            raise ValueError("Empty text in list")
        return [[0.1] * self._dimension for _ in texts]
    
    @property
    def dimension(self) -> int:
        return self._dimension
    
    @property
    def model_name(self) -> str:
        return "mock_model"
    
class TestEmbeddingModelInterface(unittest.TestCase):
    """
    Test cases for EmbeddingModel interface contract.
    Uses MockEmbeddingModel to verify the interface behaves correctly.
    """

    def setUp(self):
        """
        Set up test cases.
        """
        self.model =MockEmbeddingModel()

    def test_generate_embedding_format(self):
        """
        Test generating a single embedding return correct format.
        """
        embedding = self.model.generate_embedding("test text")

        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), self.model.dimension)
        self.assertTrue(all(isinstance(x, float) for x in embedding))

    def test_generate_multiple_embeddings_format(self):
        """
        Test generating multiple embeddings returns correct format.
        """
        texts = ["text1", "text2"]
        embeddings =self.model.generate_embeddings(texts)

        self.assertIsInstance(embeddings, list)
        self.assertEqual(len(embeddings), len(texts))
        for embedding in embeddings:
            self.assertIsInstance(embedding, list)
            self.assertEqual(len(embedding), self.model.dimension)
            self.assertTrue(all(isinstance(x, float) for x in embedding))

    def test_dimension_property_type(self):
        """
        Test dimension property returns a positive integer.
        """ 
        dimension = self.model.dimension
        self.assertIsInstance(dimension, int)
        self.assertGreater(dimension, 0)

    def test_model_name_property(self):
        """
        Test model_name property returns a non-empty string.
        """
        name = self.model.model_name
        self.assertIsInstance(name, str)
        self.assertGreater(len(name), 0)

    def test_empty_input_handling(self):
        """
        Test interface handles empty inputs consistently.
        """
        with self.assertRaises(ValueError):
            self.model.generate_embedding("")

        with self.assertRaises(ValueError):
            self.model.generate_embeddings([])

        with self.assertRaises(ValueError):
            self.model.generate_embeddings(["valid", ""])

class TestEmbeddingModelFactory(unittest.TestCase):
    """
    Test cases for EmbeddingModelFactory.
    Only tests factory behavior, not specific implementations.
    """

    def test_factory_creates_model_instance(self):
        """
        Test factory creates an instance of EmbeddingModel.
        """
        # We only verify it creates a model instance
        # Specific implementation testing belongs in test_openai.py
        model = EmbeddingModelFactory.create(
            model_type="openai",
            api_key="test-key"
        )
        self.assertIsInstance(model, EmbeddingModel)

    def test_unknown_model_type(self):
        """
        Test factory handles unknown model types.
        """
        with self.assertRaises(ValueError) as context:
            EmbeddingModelFactory.create(
                model_type="unknown",
                api_key="test-key"
            )
        self.assertIn("Unknown model type", str(context.exception))

    def test_missing_required_parameters(self):
        """
        Test factory validates required parameters.
        """
        with self.assertRaises(ValueError) as context:
            EmbeddingModelFactory.create(model_type="openai")
        self.assertIn("requires an API key", str(context.exception))

if __name__ == '__main__':
    unittest.main()