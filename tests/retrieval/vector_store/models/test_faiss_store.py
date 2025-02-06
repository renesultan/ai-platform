"""
Tests for FAISS-based vector store implementation
"""
import unittest
import numpy as np
from typing import List

from src.ai_platform.retrieval.vector_store.models.faiss_store import FAISSVectorStore

class TestFAISSVectorStore(unittest.TestCase):
    """
    Test cases for FAISSVectorStore implementation.
    Tests both basic functionality and edge cases.
    """

    def setUp(self):
        """
        Set up test vectors and store for each test.
        """
        self.dimension = 3
        self.store = FAISSVectorStore(dimension=self.dimension)

        # Create some test vectors
        self.test_vector = [1.0, 2.0, 3.0]
        self.test_vectors = [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0]
        ]
        self.test_ids = ["vec1", "vec2", "vec3"]

    def test_initialization(self):
        """
        Test store initialization with different parameters.
        """
        # Test valid initialization
        store = FAISSVectorStore(dimension=5)
        self.assertEqual(store.dimension, 5)

        # Test invalid dimension
        with self.assertRaises(ValueError):
            FAISSVectorStore(dimension=0)
        with self.assertRaises(ValueError):
            FAISSVectorStore(dimension=-1)

    def test_add_get_single_vector(self):
        """
        Test adding and retrieving a single vector.
        """
        # Add vector
        self.store.add_vector("test1", self.test_vector)

        # Retrieve and verify
        retrieved = self.store.get_vector("test1")
        self.assertIsNotNone(retrieved)
        np.testing.assert_array_almost_equal(retrieved, self.test_vector)

    def test_add_vector_wrong_dimension(self):
        """
        Test adding vector with wrong dimension raises error.
        """
        wrong_dim_vector = [1.0, 2.0] # 2D instead of 3D
        with self.assertRaises(ValueError):
            self.store.add_vector("test", wrong_dim_vector)

    def test_add_duplicate_vector(self):
        """
        Test adding vector with duplicate ID raises error.
        """
        self.store.add_vector("test1", self.test_vector)
        with self.assertRaises(ValueError):
            self.store.add_vector("test1", self.test_vector)

    def test_add_vectors_mismatched_lengths(self):
        """
        Test adding vector with mismatched IDs and vectors raise error.
        """
        self.store.add_vectors(self.test_ids, self.test_vectors)

        # Verify all vectors were added correctly
        for id, vector in self.test_vectors:
            retrieved = self.store.get_vector(id)
            self.assertIsNotNone(retrieved)
            np.testing.assert_array_almost_equal(retrieved, vector)

    def test_add_vectors_mismatched_lengths(self):
        """
        Test adding vectors with mismatched IDs and vectors raises error.
        """
        ids = ["test1", "test2"]
        vectors = [[1.0, 2.0, 3.0]] # Only one vector
        with self.assertRaises(ValueError):
            self.store.add_vectors(ids, vectors)

    def test_add_vectors_wrong_dimension(self):
        """
        Test adding multiple vectors with wrong dimension raises error.
        """
        wrong_vectors = [[1.0, 2.0], [3.0, 4.0]] # 2D instead of 3D
        with self.assertRaises(ValueError):
            self.store.add_vectors(["test1", "test2"], wrong_vectors)

    def test_get_nonexistent_vector(self):
        """
        Test retrieving nonexistent vector returns None.
        """
        result = self.store.get_vector("nonexistent")
        self.assertIsNone(result)

    def test_find_similar_basic(self):
        """
        Test basic similarity search functionality.
        """
        # Add test vectors
        self.store.add_vectors(self.test_ids, self.test_vectors)

        # Search with first vector
        query = self.test_vectors[0]
        results = self.store.find_similar(query, k=2)

        # Verify results
        self.assertEqual(len(results), 2)
        # First result should be the same vector (distance = 0)
        self.assertEqual(results[0][0], self.test_ids[0])
        self.assertAlmostEqual(results[0][1], 0.0)

    def test_find_similar_empty_store(self):
        """
        Test similarity search on empty store returns empty list.
        """
        results = self.store.find_similar([1.0, 2.0, 3.0], k=5)
        self.assertEqual(results, [])

    def test_find_similar_with_threshold(self):
        """
        Test similarity search with distance threshold.
        """
        self.store.add_vectors(self.test_ids, self.test_vectors)

        # Search with threshold that should exclude some results
        threshold = 5.0
        results = self.store.find_similar(
            self.test_vectors[0],
            k=3,
            distance_threshold=threshold,
        )

        # Verify all returned distances are within threshold
        for _, distance in results:
            self.assertLessEqual(distance, threshold)

    def test_delete_vector(self):
        """
        Test vector deletion.
        """
        # Add and verify vector exists
        self.store.add_vector("test1", self.test_vector)
        self.assertIsNotNone(self.store.get_vector("test1"))

        # Delete and verify it's None
        result = self.store.delete_vector("test1")
        self.assertTrue(result)
        self.assertIsNone(self.store.get_vector("test1"))

    def test_delete_nonexistent_vector(self):
        """
        Test deleting nonexistent vector returns False.
        """
        result = self.store.delete_vector("nonexistent")
        self.assertFalse(result)

    def test_delete_multiple_vectors(self):
        """
        Test deleting multiple vectors.
        """
        # Add test vectors
        self.store.add_vectors(self.test_ids, self.test_vectors)

        # Delete some vectors
        self.store.delete_vectors(["vec1", "vec2", "nonexistent"])

        # Verify deletions
        self.assertIsNone(self.store.get_vector("vec1"))
        self.assertIsNone(self.store.get_vector("vec2"))
        self.assertIsNotNone(self.store.get_vector("vec3"))

    def test_find_similar_after_deletion(self):
        """
        Test similarity search stull works after deletions.
        """
        # Add vectors
        self.store.add_vectors(self.test_ids, self.test_vectors)

        # Delete one vector
        self.store.delete_vector("vec1")

        # Search
        results = self.store.find_similar(self.test_vectors[1], k=2)

        # Verify results don't include deleted vector
        result_ids = [id for id, _ in results]
        self.assertNotIn("vec1", result_ids)
        self.assertEqual(len(results), 2)

if __name__ == '__main__':
    unittest.main()                     