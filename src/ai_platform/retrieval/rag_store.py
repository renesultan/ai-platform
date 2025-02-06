"""
Integrated RAG store combining document storage, embedding, and vector search.
"""
from typing import Dict, List, Optional, Tuple

from .document_store import DocumentStore
from .vector_store import VectorStore
from .embeddings import EmbeddingModel
from .types import Document, DocumentChunk
from .chunk_embedder import ChunkEmbedder

class RAGStoreError(Exception):
    """
    Custom exception for RAG store errors
    """
    pass

class RAGStore:
    """
    Complete RAG storage system integrating document storage,
    embedding generation, and vector similarity search.
    """
    def __init__(
            self,
            document_store: DocumentStore,
            vector_store: VectorStore,
            embedding_model: EmbeddingModel,
            chunk_size: Optional[int] = None
    ):
        """
        Initialize a RAG store with required components.

        Args:
            document_store: Store for documents and chunks
            vector_store: Store for vector embeddings
            embedding_model: Model for generating embeddings
            chunk_size: Optional custom chunk size

        Raises:
            ValueError: If any required component is None
        """
        if not document_store:
            raise ValueError("document_store cannot be None")
        if not vector_store:
            raise ValueError("vector_store cannot be None")
        if not embedding_model:
            raise ValueError("embedding_model cannot be None")
        
        self._document_store = document_store
        self._vector_store = vector_store
        self._chunk_embedder = ChunkEmbedder(embedding_model)
        self._chunk_size = chunk_size

    def add_document(
            self,
            content: str,
            metadata: Optional[Dict] = None
    ) -> str:
        """
        Add document to the RAG store.
        Handles chunking, embedding generation, and storage.

        Args:
            content: Document content
            metadata: Optional document metadata

        Returns:
            Document ID

        Raises:
            RAGStoreError: If document processing fails
        """
        try:
            # Add to document store first
            doc_id = self._document_store.add_document(
                content=content,
                metadata=metadata,
                chunk_size=self._chunk_size
            )

            # Get chunks for the document
            chunks = self._document_store.get_document_chunks(doc_id)

            # Generate embeddings
            try:
                embeddings = self._chunk_embedder.generate_embeddings(chunks)
            except Exception as e:
                # If embedding fails, clean up document and re-raise
                self._document_store.delete_document(doc_id)
                raise RAGStoreError(f"Failed to generate embeddings: {str(e)}")
            
            # Store embeddings
            try:
                chunk_ids = [chunk.chunk_id for chunk in chunks]
                self._vector_store.add_vectors(chunk_ids, embeddings)
            except Exception as e:
                # If vector storage fails, clean up and re-raise
                self._document_store.delete_document(doc_id)
                raise RAGStoreError(f"Failed to store vectors: {str(e)}")
            
            return doc_id
        
        except Exception as e:
            if not isinstance(e, RAGStoreError):
                raise RAGStoreError(f"Failed to add document: {str(e)}")
            raise

    def get_document(self, document_id: str) -> Optional[Document]:
        """
        Retrieve a document by ID.

        Args:
            document_id: ID of document to retrieve

        Returns:
            Document if found, None otherwise
        """
        return self._document_store.get_document(document_id)
    
    def find_relevant_chunks(
            self,
            query: str,
            k: int = 5,
            distance_threshold: Optional[float] = None
    ) -> List[Tuple[DocumentChunk, float]]:
        """
        Find chunks relevant to a query using similarity search.

        Args:
            query: Search query
            k: Number of results to return
            distance_threshold: Optional similarity threshold

        Returns:
            List of (chunk, similarity_score) tuples ordered by relevance

        Raises:
            RAGStoreError: If retrieval fails
        """
        try:
            # Create temporary chunk for query
            query_chunk = DocumentChunk(
                chunk_id="query",
                text=query,
                document_id="query"
            )

            # Generate query embedding
            try:
                query_embedding = self._chunk_embedder.generate_embedding(query_chunk)
            except Exception as e:
                raise RAGStoreError(f"Failed to generate query embedding: {str(e)}")
            
            # Find similar vectors
            try:
                similar_chunks = self._vector_store.find_similar(
                    query_embedding,
                    k=k,
                    distance_threshold=distance_threshold
                )
            except Exception as e:
                raise RAGStoreError(f"Failed to find similar vectors: {str(e)}")
            
            # Get actual chunks
            results = []
            for chunk_id, score in similar_chunks:
                chunk = self._document_store.get_chunk(chunk_id)
                if chunk: # Only include if chunk exists
                    results.append((chunk, score))

            return results
        
        except Exception as e:
            if not isinstance(e, RAGStoreError):
                raise RAGStoreError(f"Failed to find relevant chunks: {str(e)}")
            raise

    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document and all its associated data.

        Args:
            document_id: ID of document to delete

        Returns:
            True if document was found and deleted

        Raises:
            RAGStoreError: If deletion fails
        """
        try:
            # Get chunks before deletion
            chunks = self._document_store.get_document_chunks(document_id)
            chunk_ids = [chunk.chunk_id for chunk in chunks]

            # Delete from vector store
            if chunk_ids:
                try:
                    self._vector_store.delete_vectors(chunk_ids)
                except Exception as e:
                    raise RAGStoreError(f"Failed to delete vectors: {str(e)}")
                
            # Delete from document store
            deleted = self._document_store.delete_document(document_id)

            # Clear embeddings from cache
            for chunk_id in chunk_ids:
                self._chunk_embedder._embedding_cache.pop(chunk_id, None)

            return deleted
        
        except Exception as e:
            if not isinstance(e, RAGStoreError):
                raise RAGStoreError(f"Failed to delete document: {str(e)}")
            raise
