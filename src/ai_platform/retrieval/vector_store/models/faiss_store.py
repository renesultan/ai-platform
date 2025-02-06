"""
FAISS-based implementation of the VectorStore interface.
Provides efficient similarity search for high-dimensional
"""
from typing import List, Optional, Tuple, Dict
import numpy as np
import faiss
from ..interfaces import VectorStore

class FAISSVectorStore(VectorStore):
    """
    Vector store implementation using FAISS for efficient similarity search.

    This implementation:
    - Uses L2 distance for similarity
    - Maintains an in-memory mapping of IDs to indices
    - Supports dynamic addition and deletion of vectors
    """
    def __init__(self, dimension: int):
        """
        Initializes FAISS vector store.

        Args:
            dimension: Dimensionality of vectors to be stored

        Raises:
            ValueError: If dimension is not positive
        """
        if dimension <= 0:
            raise ValueError("Dimension must be positive")
        
        self.dimension = dimension
        # Initialize FAISS index for L2 distance
        self.index = faiss.IndexFlatL2(dimension)
        # Map IDs to their positions in the index
        self._id_to_index: Dict[str, int] = {}
        # Map positions to IDs
        self._index_to_id: Dict[int, str] = {}
        # Track the next available index
        self._next_index = 0

    def add_vector(self, id: str, vector: List[float]) -> None:
        """
        Add a single vector to the store

        Args:
            id: Unique identifier for the vector
            vector: Vector to store, must match initialized dimension

        Raises:
            ValueError: If vector dimension doesn't match or ID exists 
        """
        if id in self._id_to_index:
            raise ValueError(f"Vector with id {id} already exists")
        
        vector_array = np.array(vector, dtype=np.float32)
        if vector_array.shape != (self.dimension,):
            raise ValueError(
                f"Vector dimension {vector_array.shape[0]} "
                f"doesn't match index dimension {self.dimension}"
            )
        
        # Add to FAISS index
        self.index.add(vector_array.reshape(1, -1))

        # Update mappings
        self._id_to_index[id] = self._next_index
        self._index_to_id[self._next_index] = id
        self._next_index += 1

    def add_vectors(self, ids: List[str], vectors: List[List[float]]) -> None:
        """
        Add multiple vectors to the store.

        Args:
            ids: List of unique identifiers
            vectors: List of vectors to store

        Raises:
            ValueError: If dimensions don't match or any ID exists
        """
        if len(ids) != len(vectors):
            raise ValueError("Number of ids must match number of vectors")
        
        # Check for duplicate IDs
        if any(id in self._id_to_index for id in ids):
            raise ValueError("One or more IDs already exist")
        
        # Convert to numpy array for FAISS
        vectors_array = np.array(vectors, dtype=np.float32)
        if vectors_array.shape[1] != self.dimension:
            raise ValueError(
                f"Vector dimension {vectors_array.shape[1]} "
                f"doesn't match index dimension {self.dimension}"
            )
        
        # Add to FAISS index
        self.index.add(vectors_array)

        # Update mappings
        for id in ids:
            self._id_to_index[id] = self._next_index
            self._index_to_id[self._next_index] = id
            self._next_index += 1

    def get_vector(self, id: str) -> Optional[List[float]]:
        """
        Retrieve a vector by its ID.

        Args:
            id: The identifier of the vector to retrieve

        Returns:
            The vector if found, None otherwise
        """
        if id not in self._id_to_index:
            return None
        
        # FAISS doesn't provide direct vector access
        # We need to reconstruct from index
        index = self._id_to_index[id]
        # Search with high k to ensure we fnd the exact vector
        D, I = self.index.search(
            self.index.reconstruct(index).reshape(1, -1),
            1
        )
        return self.index.reconstruct(int(I[0][0])).tolist()
    
    def find_similar(
            self,
            query_vector: List[float],
            k: int = 5,
            distance_threshold: Optional[float] = None
    ) -> List[Tuple[str, float]]:
        """
        Find k most similar vectors ot query_vector.

        Args:
            query_vector: Vector to compare against
            k: Number of similar vectors to return
            distance_threshold: Optional maximum distance threshold

        Returns:
            List of tuples (id, distance) ordered by similarity
        
        Raises:
            ValueError: If query_vector dimensions don't match
        """
        query_array = np.array(query_vector, dtype=np.float32)
        if query_array.shape != (self.dimension,):
            raise ValueError("Query vector dimension doesn't match index dimension")
        
        # Ensure k doesn't exceed number of stored vectors
        k = min(k, self.index.ntotal)
        if k == 0:
            return []
        
        # Perform similarity search
        distances, indices = self.index.search(query_array.reshape(1, -1), k)

        # COnvert results to list of (id, distance) tuples
        results = []
        for idx, (distance, index) in enumerate(zip(distances[0], indices[0])):
            # Stop if we hut the distance threshold
            if distance_threshold and distance > distance_threshold:
                break
            # Skip invalid indices (can happen if vectors were deleted)
            if index in self._index_to_id:
                results.append((self._index_to_id[index], float(distance)))

        return results
    
    def delete_vector(self, id: str) -> bool:
        """
        Delete a vector by its ID.

        Args:
            id: The identifier of the vector to delete

        Returns:
            True if vector was found and deleted, False otherwise
        """
        if id not in self._id_to_index:
            return False
        
        # FAISS doesn't support direct deletion
        # We need to rebuild the index without the deleted vector
        index_to_remove = self._id_to_index[id]

        # Get all vectors except the one to delete
        vectors = []
        ids = []
        for i in range(self.index.ntotal):
            if i != index_to_remove:
                vectors.append(self.index.reconstruct(i))
                ids.append(self._index_to_id[i])

        # Clear existing index and mappings
        self.index = faiss.IndexFlatL2(self.dimension)
        self._id_to_index.clear()
        self._index_to_id.clear()
        self._next_index = 0

        # Re-add remaining vectors
        if vectors:
            vectors_array = np.array(vectors, dtype=np.float32)
            self.index.add(vectors_array)
            for id in ids:
                self._id_to_index[id] = self._next_index
                self._index_to_id[self._next_index] = id
                self._next_index += 1

        return True
    
    def delete_vectors(self, ids: List[str]) -> None:
        """
        Delete multiple vectors by their IDs.

        Args:
            ids: List of identifiers to delete
        """
        # Filter to existing IDs
        ids_to_delete = set(id for id in ids if id in self._id_to_index)
        if not ids_to_delete:
            return False
        
        # Get indices to remove
        indices_to_remove = {self._id_to_index[id] for id in ids_to_delete}

        # Get all vectors except those to delete
        vectors = []
        remaining_ids = []
        for i in range(self.index.ntotal):
            if i not in indices_to_remove:
                vectors.append(self.index.reconstruct(i))
                remaining_ids.append(self._index_to_id[i])

        # Clear and rebuild index
        self.index = faiss.IndexFlatL2(self.dimension)
        self._id_to_index.clear()
        self._index_to_id.clear()
        self._next_index = 0

        # Re-add remaining vectors
        if vectors:
            vectors_array = np.array(vectors, dtype=np.float32)
            self.index.add(vectors_array)
            for id in remaining_ids:
                self._id_to_index[id] = self._next_index
                self._index_to_id[self._next_index] = id
                self._next_index += 1
