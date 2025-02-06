"""
Tests for integrated RAG store functionality
"""
import unittest
from unittest.mock import Mock

from src.ai_platform.retrieval.rag_store import RAGStore, RAGStoreError
from src.ai_platform.retrieval.document_store import DocumentStore
from src.ai_platform.retrieval.vector_store.models.faiss_store import FAISSVectorStore
from src.ai_platform.retrieval.types import Document, DocumentChunk

class TestRAGStore(unittest.TestCase):
    """
    Test cases for RAGStore class
    """
    def setUp(self):
        """
        Set up test fixtures
        """
        self.document_store = DocumentStore(default_chunk_size=100)
        self.vector_store = FAISSVectorStore(dimension=3) # Small dimension for testing
        self.mock_embedding_model = Mock()
        self.mock_embedding_model.dimension = 3

        # Setup mock embeddings
        self.mock_embedding_model.generate_embedding.return_value = [0.1, 0.2, 0.3]
        # Setup mock embeddings for batch embedding generation with a dynamic side_effect
        self.mock_embedding_model.generate_embeddings.side_effect = lambda texts: [
            [0.1 * (i + 1), 0.2 * (i + 1), 0.3 * (i + 1)] for i in range(len(texts))
        ]

        self.rag_store = RAGStore(
            document_store=self.document_store,
            vector_store=self.vector_store,
            embedding_model=self.mock_embedding_model
        )

    def test_initialization_validation(self):
        """
        Test that initialization validates required components
        """
        with self.assertRaises(ValueError):
            RAGStore(None, self.vector_store, self.mock_embedding_model)

        with self.assertRaises(ValueError):
            RAGStore(self.document_store, None, self.mock_embedding_model)

        with self.assertRaises(ValueError):
            RAGStore(self.document_store, self.vector_store, None)

    def test_add_and_retrieve_document(self):
        """
        Test adding document and retrieving it
        """
        content = "Test document content. Multiple sentences for chunking."
        doc_id = self.rag_store.add_document(content)

        # Verify document was stored
        doc = self.rag_store.get_document(doc_id)
        self.assertIsNotNone(doc)
        self.assertEqual(doc.content, content)

        # Verify chunks were created
        chunks = self.document_store.get_document_chunks(doc_id)
        self.assertTrue(len(chunks) > 0)

        # Verify embeddings were generated
        self.mock_embedding_model.generate_embeddings.assert_called_once()

    def test_find_relevant_chunks(self):
        """
        Test finding relevant chunks for a query
        """
        # Add test document
        doc_id = self.rag_store.add_document(
            "This is the very first chunk content from this very own test document. This is the second chunk content from this very own test document. This is the third chunk content from this very own test document."
        )

        # Search for relevant chunks
        query = "chunk content"
        results = self.rag_store.find_relevant_chunks(query, k=2)

        # Verify results structure
        self.assertEqual(len(results), 2)  # Asked for k=2
        for chunk, score in results:
            self.assertIsInstance(chunk, DocumentChunk)
            self.assertIsInstance(score, float)

        # Verify query was embedded
        self.mock_embedding_model.generate_embedding.assert_called()

    def test_delete_document(self):
        """
        Test document deletion removes all associated data
        """
        # Add document
        doc_id = self.rag_store.add_document("Test content")

        # Verify document exists
        self.assertIsNotNone(self.rag_store.get_document(doc_id))

        # Delete document
        result = self.rag_store.delete_document(doc_id)
        self.assertTrue(result)

        # Verify document is gone
        self.assertIsNone(self.rag_store.get_document(doc_id))

    def test_error_handling_in_add_document(self):
        """
        Test error handling during document addition
        """
        # Mock embedding failure
        self.mock_embedding_model.generate_embeddings.side_effect = Exception("Embedding failed")

        with self.assertRaises(RAGStoreError) as context:
            self.rag_store.add_document("Test content")

        self.assertIn("Failed to generate embeddings", str(context.exception))

    def test_error_handling_in_find_relevant(self):
        """
        Test error handling during relevance search
        """
        # Mock embedding failure
        self.mock_embedding_model.generate_embedding.side_effect = Exception("Embedding failed")

        with self.assertRaises(RAGStoreError) as context:
            self.rag_store.find_relevant_chunks("test query")

        self.assertIn("Failed to generate query embedding", str(context.exception))

    def test_document_cleanup_on_failure(self):
        """
        Test that document is cleaned up if processing fails
        """
        # Mock vector store to fail
        original_add_vectors = self.vector_store.add_vectors
        self.vector_store.add_vectors = Mock(side_effect=Exception("Vector store failed"))

        # Attempt to add document
        with self.assertRaises(RAGStoreError):
            doc_id = self.rag_store.add_document("Test content")

        # Verify no documents were left in store
        self.assertEqual(len(self.document_store._documents), 0)

        # Restore original method
        self.vector_store.add_vectors = original_add_vectors

