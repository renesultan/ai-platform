"""
Tests for chunk embedder functionality
"""
import unittest
from unittest.mock import Mock

from src.ai_platform.retrieval.chunk_embedder import ChunkEmbedder
from src.ai_platform.retrieval.types import DocumentChunk

class TestChunkEmbedder(unittest.TestCase):
    """
    Test cases for ChunkEmbedder class
    """
    def setUp(self):
        """
        Set up test fixtures
        """
        self.mock_model = Mock()
        self.embedder = ChunkEmbedder(self.mock_model)
        self.test_chunk = DocumentChunk(
            chunk_id="test1",
            text="Test content",
            document_id="doc1"
        )

    def test_generate_single_embedding(self):
        """
        Test generating embedding for a single chunk
        """
        expected_embedding = [0.1, 0.2, 0.3]
        self.mock_model.generate_embedding.return_value = expected_embedding

        # Generate embedding
        result = self.embedder.generate_embedding(self.test_chunk)
        
        # Verify result and model call
        self.assertEqual(result, expected_embedding)
        self.mock_model.generate_embedding.assert_called_once_with(self.test_chunk.text)

    def test_empty_chunk_raises_error(self):
        """
        Test that empty chunk raises ValueError
        """
        empty_chunk = DocumentChunk(
            chunk_id="empty",
            text="    ", # Only whitespace
            document_id="doc1"
        )
        with self.assertRaises(ValueError):
            self.embedder.generate_embedding(empty_chunk)

    def test_generate_multiple_embeddings(self):
        """
        Test generating embeddings for multiple chunks
        """
        chunks = [
            self.test_chunk,
            DocumentChunk(chunk_id="test2", text="More content", document_id="doc1")
        ]
        expected_embeddings = [[0.1, 0.2], [0.3, 0.4]]
        self.mock_model.generate_embeddings.return_value = expected_embeddings

        # Generate embeddings
        results = self.embedder.generate_embeddings(chunks)

        # Verify results and model call
        self.assertEqual(results, expected_embeddings)
        self.mock_model.generate_embeddings.assert_called_once_with([c.text for c in chunks])

    def test_embedding_caching(self):
        """
        Test that embeddings are properly cached
        """
        embedding = [0.1, 0.2, 0.3]
        self.mock_model.generate_embedding.return_value = embedding

        # First call should use model
        self.embedder.generate_embedding(self.test_chunk)
        self.mock_model.generate_embedding.assert_called_once()

        # Second call should use cache
        self.mock_model.generate_embedding.reset_mock()
        cached_result = self.embedder.generate_embedding(self.test_chunk)
        self.assertEqual(cached_result, embedding)
        self.mock_model.generate_embedding.assert_not_called()

    def test_clear_cache(self):
        """
        Test cache clearing functionality
        """
        # Add something to cache
        embedding = [0.1, 0.2, 0.3]
        self.mock_model.generate_embedding.return_value = embedding
        self.embedder.generate_embedding(self.test_chunk)

        # Clear cache
        self.embedder.clear_cache()

        # Verify cache is empty by checking that is model is called again
        self.mock_model.generate_embedding.reset_mock()
        self.embedder.generate_embedding(self.test_chunk)
        self.mock_model.generate_embedding.assert_called_once()

    def test_get_cached_embedding(self):
        """
        Test retrieving cached embedding
        """
        # Initally should return None
        self.assertIsNone(self.embedder.get_cached_embedding("test1"))

        # Add embedding and verify it can be retrieved
        embedding = [0.1, 0.2, 0.3]
        self.mock_model.generate_embedding.return_value = embedding
        self.embedder.generate_embedding(self.test_chunk)

        cached = self.embedder.get_cached_embedding("test1")
        self.assertEqual(cached, embedding)

if __name__ == '__main__':
    unittest.main()