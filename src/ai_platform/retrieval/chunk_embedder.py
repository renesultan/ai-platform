"""
Handles embedding generation and management for document chunks.
"""
from typing import Dict, List, Optional

from .types import DocumentChunk
from .embeddings import EmbeddingModel

class ChunkEmbedder:
    """
    Manages embedding generation and storage for document chunks.
    Acts as a coordinator between chunks and their embeddings.
    """
    def __init__(self, embedding_model: EmbeddingModel):
        """
        Initialize chunk embedder with specified model.

        Args:
            embedding_model: Model to use for generating embeddings
        """
        self._embedding_model = embedding_model
        # Cache of chunk_id to embedding mapping
        self._embedding_cache: Dict[str, List[float]] = {}

    def generate_embedding(self, chunk: DocumentChunk) -> List[float]:
        """
        Generate embedding for a single chunk.
        Caches the result for future use.

        Args:
            chunk: The document chunk to embed

        Raises:
            ValueError: If chunk is invalid or embedding fails
        """
        if not chunk.text.strip():
            raise ValueError("Cannot be empty chunk")
        
        if chunk.chunk_id in self._embedding_cache:
            return self._embedding_cache[chunk.chunk_id]
        
        embedding = self._embedding_model.generate_embedding(chunk.text)
        self._embedding_cache[chunk.chunk_id] = embedding
        return embedding

    def generate_embeddings(self, chunks: List[DocumentChunk]) -> List[List[float]]:
        """
        Generate embeddings for multiple chunks efficiently.
        Caches results for future use.

        Args:
            chunks: The document chunks to embed

        Returns:
            List of embedding vectors

        Raises:
            ValueError: If chunks are invalid or embedding fails
        """
        if not chunks:
            return []
        
        # Filter out chunks we already have embeddings for 
        new_chunks = [
            chunk for chunk in chunks
            if chunk.chunk_id not in self._embedding_cache
        ]

        if new_chunks:
            # Generate embedding for new chunks
            new_texts = [chunk.text for chunk in new_chunks]
            new_embeddings = self._embedding_model.generate_embeddings(new_texts)

            # Cache new embeddings
            for chunk, embedding in zip(new_chunks, new_embeddings):
                self._embedding_cache[chunk.chunk_id] = embedding

        # Return all embeddings in original order
        return [self._embedding_cache[chunk.chunk_id] for chunk in chunks]
    
    def get_cached_embedding(self, chunk_id: str) -> Optional[List[float]]:
        """
        Retrieve cached embedding for a chunk if available.

        Args:
            chunk_id: ID of the chunk to get embedding for

        Returns:
            Cached embedding if available, None otherwise
        """
        return self._embedding_cache.get(chunk_id)

    def clear_cache(self) -> None:
        """
        Clear the embedding cache.
        Useful for memory management.
        """
        self._embedding_cache.clear()