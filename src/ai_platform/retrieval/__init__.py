"""
Document types and Document Store to simulate in-memory storage.
"""

from .types import Document, DocumentChunk
from .document_store import DocumentStore

__all__ = ['Document', 'DocumentChunk', 'DocumentStore']