"""
Tests for vector interface contract
"""
import unittest
from typing import List, Optional, Tuple

from src.ai_platform.retrieval.vector_store.interfaces import VectorStore

class MockVectorStore(VectorStore):
    """
    Simple in-memory implementation of VectorStore for testing interface contract
    """
    def __init__(self):
        self.vectors = {} # id -> vector mapping

    def add_vector(self, id: str, vector: List[float]) -> None:
        if id in self.vectors:
            raise ValueError(f"Vector with id {id} already exists")
        self.vectors[id] = vector

    def add_vectors(self, ids: List[str], vectors: List[List[float]]) -> None:
        if len(ids) != len(vectors):
            raise ValueError(f"Number of ids must match number of vectors")
        for id, vector in zip(ids, vectors):
            self.add_vector(id, vector)

    def get_vector(self, id: str) -> Optional[List[float]]:
        return self.vectors.get(id)
    
    def find_similar(
            self,
            query_vector: List[float],
            k: int = 5,
            distance_threshold: Optional[float] =  None
    ) -> List[Tuple[str, float]]:
        # Simple mock implementation using fixed instances
        results = [(id, 0.5) for id in list(self.vectors.keys())[:k]]
        return results
    
    def delete_vector(self, id: str) -> bool:
        if id in self.vectors:
            del self.vectors[id]
            return True
        return False
    
    def delete_vectors(self, ids: List[str]) -> None:
        for id in ids:
            self.delete_vector(id)

class TestVectorStoreInterface(unittest.TestCase):
    """
    Test cases to verify the VectorStore interface contract
    """

    def setUp(self):
        """
        Set up a mock vector store for testing
        """
        self.store = MockVectorStore()
        self.test_vector = [0.1, 0.2, 0.3]

    def test_add_and_get_vector(self):
        """
        Test basic vector addition and retrieval
        """
        self.store.add_vector("test1", self.test_vector)
        retrieved = self.store.get_vector("test1")
        self.assertEqual(retrieved, self.test_vector)

    def test_add_duplicate_vector(self):
        """
        Test adding vector with duplicate ID raises error
        """
        self.store.add_vector("test1", self.test_vector)
        with self.assertRaises(ValueError):
            self.store.add_vector("test1", self.test_vector)

    def add_multiple_vectors(self):
        """
        Test adding multiple vectors at once
        """
        ids = ["test1", "test2"]
        vectors = [[0.1, 0.2], [0.3, 0.4]]
        self.store.add_vectors(ids, vectors)

        for id, vector in zip(ids, vectors):
            self.assertEqual(self.store.get_vector(id), vector)

    def test_find_similar_vectors(self):
        """
        Test finding similar vectors
        """
        # Add some test vectors
        self.store.add_vector("test1", [0.1, 0.2])
        self.store.add_vector("test2", [0.3, 0.4])

        # Search
        results = self.store.find_similar([0.1, 0.2], k=2)

        # Verify results format
        self.assertEqual(len(results), 2)
        for id, distance in results:
            self.assertIsInstance(id, str)
            self.assertIsInstance(distance, float)

    def test_delete_vector(self):
        """
        Test vector deletion
        """
        # Add and verify vector exists
        self.store.add_vector("test1", self.test_vector)
        self.assertIsNotNone(self.store.get_vector("test1"))

        # Delete and verify it's gone
        result = self.store.delete_vector("test1")
        self.assertTrue(result)
        self.assertIsNone(self.store.get_vector("test1"))

    def test_delete_nonexistent_vector(self):
        """
        Test deleting vector that doesn't exist
        """
        result = self.store.delete_vector("nonexistent")
        self.assertFalse(result)

    def test_delete_multiple_vectors(self):
        """
        Test deleting multiple vectors
        """
        # Add test vectors
        ids = ["test1", "test2", "test3"]
        vectors = [[0.1], [0.2], [0.3]]
        self.store.add_vectors(ids, vectors)

        # Delete some vectors
        self.store.delete_vectors(["test1", "test2", "nonexistent"])

        # verify deletions
        self.assertIsNone(self.store.get_vector("test1"))
        self.assertIsNone(self.store.get_vector("test2"))
        self.assertIsNotNone(self.store.get_vector("test3"))

if __name__ == '__main__':
    unittest.main()


