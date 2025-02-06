"""
Tests for document store implementation
"""
import unittest
from src.ai_platform.retrieval.document_store import DocumentStore

class TestDocumentStore(unittest.TestCase):
    """
    Test cases for DocumentStore class
    """
    def setUp(self):
        """
        Create a fresh document store for each test
        """
        self.store = DocumentStore(default_chunk_size=100)

    def test_add_and_retrieve_document(self):
        """
        Test adding and retrieving a document
        """
        content = "This is a test document. With multiple sentences."
        metadata = {"souce": "test"}

        # Add document
        doc_id = self.store.add_document(content, metadata=metadata)
        
        # Retrieve and verify
        doc = self.store.get_document(doc_id)
        self.assertIsNotNone(doc)
        self.assertEqual(doc.content, content)
        self.assertEqual(doc.metadata, metadata)

        # Check chunks were created
        chunks = self.store.get_document_chunks(doc_id)
        self.assertTrue(len(chunks) > 0)

    def test_chunking_behavior(self):
        """
        Test document chunking with different sizes
        """
        # Create content with known sentence lengths
        sentences = ["Short sentences"] * 10
        content = ". ".join(sentences) + "."

        # Test with different chunk sizes
        store1 = DocumentStore(default_chunk_size=50)
        store2 = DocumentStore(default_chunk_size=200)

        doc1_id = store1.add_document(content)
        doc2_id = store2.add_document(content)

        chunks1 = store1.get_document_chunks(doc1_id)
        chunks2 = store2.get_document_chunks(doc2_id)

        # Smaller chunk size should create more chunks
        self.assertTrue(len(chunks1) > len(chunks2))

        # Verify chunk sizes
        for chunk in chunks1:
            self.assertLessEqual(len(chunk.text), 50)

        for chunk in chunks2:
            self.assertLessEqual(len(chunk.text), 200)

    def test_delete_document(self):
        """
        Test document deletion
        """
        # Add document
        doc_id = self.store.add_document("Test document")

        # Verify it exists
        self.assertIsNotNone(self.store.get_document(doc_id))

        # Get chunks before deletion
        chunks = self.store.get_document_chunks(doc_id)
        chunk_ids = [chunk.chunk_id for chunk in chunks]

        # Delete document
        result = self.store.delete_document(doc_id)
        self.assertTrue(result)

        # Verify document is gone
        self.assertIsNone(self.store.get_document(doc_id))

        # Verify chunks are gone
        for chunk_id in chunk_ids:
            self.assertIsNone(self.store.get_chunk(chunk_id))

    def test_custom_chunk_size(self):
        """
        Test using custom chunk size for specific document
        """
        content = "Sentence one. Sentence two. Sentence three. Sentence four."

        # Add same document with different chunk sizes
        doc1_id = self.store.add_document(content) # default size
        doc2_id = self.store.add_document(content, chunk_size=50) # smaller size

        chunks1 = self.store.get_document_chunks(doc1_id)
        chunks2 = self.store.get_document_chunks(doc2_id)

        # Smaller chunk size should result in more chunks
        self.assertTrue(len(chunks2) >= len(chunks1))

    def test_nonexistant_document(self):
        """
        Test handling of nonexistent document IDs
        """
        fake_id = "nonexistent"

        # Verify get_document returns None
        self.assertIsNone(self.store.get_document(fake_id))

        # Verify get_document_chunks return empty list
        self.assertEqual(len(self.store.get_document_chunks(fake_id)), 0)

        # Verify delete_document returns False
        self.assertFalse(self.store.delete_document(fake_id))

if __name__ == '__main__':
    unittest.main()
