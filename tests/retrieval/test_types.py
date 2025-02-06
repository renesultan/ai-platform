"""
Test for manually implemented document type classes
"""
import unittest
from src.ai_platform.retrieval.types import Document, DocumentChunk

class TestDocumentChunk(unittest.TestCase):
    """
    Test cases for DocumentChunk class
    """

    def setUp(self):
        """
        Create a sample chunk for use in tests
        """
        self.chunk = DocumentChunk(
            chunk_id="chunk1",
            text="Test chunk content",
            document_id="doc1",
            metadata={"position": 1}
        )

    def test_properties(self):
        """
        Test that properties return correct values
        """
        self.assertEqual(self.chunk.chunk_id, "chunk1")
        self.assertEqual(self.chunk.text, "Test chunk content")
        self.assertEqual(self.chunk.document_id, "doc1")
        self.assertEqual(self.chunk.metadata["position"], 1)

    def test_metadata_immutability(self):
        """
        Test that metadata cannot be modified through the property
        """
        original_metadata = self.chunk.metadata
        original_metadata["new_key"] = "new_value"
        self.assertNotIn("new_key", self.chunk.metadata)

    def test_equality(self):
        """
        Test equality comparison
        """
        same_chunk = DocumentChunk(
            chunk_id="chunk1",
            text="Test chunk content",
            document_id="doc1"
        )
        different_chunk = DocumentChunk(
            chunk_id="chunk2",
            text="Different content",
            document_id="doc1"
        )

        self.assertEqual(self.chunk, same_chunk)
        self.assertNotEqual(self.chunk, different_chunk)
        self.assertNotEqual(self.chunk, "not a chunk")

    def test_representation(self):
        """
        Test string representation
        """
        repr_str = repr(self.chunk)
        self.assertIn("chunk1", repr_str)
        self.assertIn("Test chunk content", repr_str)
        self.assertIn("doc1", repr_str)

class TestDocument(unittest.TestCase):
    """
    Test cases for Document class
    """

    def setUp(self):
        """
        Create a sample document for use in tests
        """
        self.doc = Document(
            document_id="doc1",
            content="Test document content",
            metadata={"author": "test"}
        )

    def test_properties(self):
        """
        Test that properties return correct values
        """
        self.assertEqual(self.doc.document_id, "doc1")
        self.assertEqual(self.doc.content, "Test document content")
        self.assertEqual(self.doc.metadata["author"], "test")

    def test_metadata_immutability(self):
        """
        Test that metadata cannot be modified through the property
        """
        original_metadata = self.doc.metadata
        original_metadata["new_key"] = "new_value"
        self.assertNotIn("new_key", self.doc.metadata)

    def test_equality(self):
        """
        Test equality comparison
        """
        same_doc = Document(
            document_id="doc1",
            content="Test document content"
        )
        different_doc = Document(
            document_id="doc2",
            content="Different content"
        )

        self.assertEqual(self.doc, same_doc)
        self.assertNotEqual(self.doc, different_doc)
        self.assertNotEqual(self.doc, "not a document")

    def test_representation(self):
        """
        Test string representation
        """
        repr_str = repr(self.doc)
        self.assertIn("doc1", repr_str)
        self.assertIn("Test document content", repr_str)

if __name__ == '__main__':
    unittest.main()