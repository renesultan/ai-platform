"""
Abstract interface for vector storage functionality.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

class VectorStore(ABC):
    """
    Abstract interface for storing and retrieving vectors.
    Implementations must handle:
    - Vector storage and retrieval
    - Similarity search
    - Vector updates and deletions
    """

    @abstractmethod
    def add_vector(self, id: str, vector: List[float]) -> None:
        """
        Store a single vector with its ID.

        Args:
            id: unique identifier for the vector
            vector: The vector to store

        Raises:
            ValueError: If vector dimensions don't match or ID already exists
        """
        pass

    @abstractmethod
    def add_vectors(self, ids: List[str], vectors: List[List[float]]) -> None:
        """
        Store multiple vectors with their IDs.

        Args:
            ids: List of unique identifiers
            vectors: List of vectors to store

        Raises:
            ValueError: If dimensions don't match or any ID already exists
        """
        pass

    @abstractmethod
    def get_vector(self, id: str) -> Optional[List[float]]:
        """
        Retrieve a vector by its ID.

        Args:
            id: The identifier of the vector to retrieve

        Returns:
            The vector if found, None otherwise
        """
        pass

    @abstractmethod
    def find_similar(
        self,
        query_vector: List[float],
        k: int = 5,
        distance_threshold: Optional[float] = None
    ) -> List[Tuple[str, float]]:
        """
        Find k most similar vectors to query_vector.

        Args:
            query_vector: Vector to compare against
            k: Number of similar vectors to return
            distance_threshold: Optional maximum distance threshold

        Returns:
            List of tuples (id, distance) ordered by similarity (closest first)

        Raises:
            ValueError: If query_vector dimensions don't match stored vectors
        """
        pass

    @abstractmethod
    def delete_vector(self, id: str) -> bool:
        """
        Delete a vector by its ID.

        Args:
            id: The identifier of the vector to delete
        
        Returns:
            True if vector was found and deleted, False otherwise
        """
        pass

    @abstractmethod
    def delete_vectors(self, ids: List[str]) -> None:
        """
        Delete multiple vectors by their IDs.
        Silently skips IDs that don't exist.

        Args:
            ids: List of identifiers to delete
        """
        pass