"""
Document types and Document Store to simulate in-memory storage.
"""

from .types import Document, DocumentChunk
from .document_store import DocumentStore
from .embeddings import EmbeddingModel, EmbeddingModelFactory
from .vector_store import VectorStore

__all__ = [
    'Document',
    'DocumentChunk',
    'DocumentStore',
    'EmbeddingModel',
    'EmbeddingModelFactory',
    'VectorStore'
]