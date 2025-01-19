"""
Basic document types for RAG system
"""

from typing import Dict, Optional

class DocumentChunk:
    """
    Represents a chunk/segment of a document
    """
    def __init__(
            self,
            chunk_id: str,
            text: str,
            document_id: str,
            metadata: Optional[Dict] = None
    ):
        """
        Initializes a document chunk.

        Args:
            chunk_id: Unique identifier for this chunk
            text: The actual text content of this chunk
            document_id: Reference document
            metadata: Optional metadata about this chunk
        """
        self._chunk_id = chunk_id
        self._text = text
        self._document_id = document_id
        self._metadata = metadata if metadata is not None else {}

    @property
    def chunk_id(self) -> str:
        """
        Get the chunk's unique identifier
        """
        return self._chunk_id
    
    @property
    def text(self) -> str:
        """
        Get the chunk's text content
        """
        return self._text
    
    @property
    def document_id(self) -> str:
        """
        Get the chunk's document identifier
        """
        return self._document_id
    
    @property
    def metadata(self) -> Dict:
        """
        Get the chunk's metadata
        """
        return self._metadata.copy() # Return a copy to prevent modification
    
    def __eq__(self, other: object) -> bool:
        """
        Compare this chunk with another for equality.
        Two chunks are equal if they have the same ID and content.
        """
        if not isinstance(other, DocumentChunk):
            return False
        
        return (
            self.chunk_id == other.chunk_id and
            self.text == other.text and
            self.document_id == other.document_id
        )
    
    def __repr__(self) -> str:
        """
        Return a string representation of the chunk.
        Useful for debugging.
        """
        return(
            f"DocumentChunk(chunk_id='{self.chunk_id}', "
            f"text='{self.text[:50]}{'...' if len(self.text) > 50 else ''}', "
            f"document_id='{self.document_id}', "
            f"metadata={self.metadata})"
        )
    
class Document:
    """
    Represents a full document.
    """
    def __init__(
            self,
            document_id: str,
            content: str,
            metadata: Optional[Dict] = None
    ):
        """
        Initialize a document.

        Args:
            document_id: Unique identifier for the document
            content: Full text content of the document
            metadata: Optional metadata about the document
        """
        self._document_id = document_id
        self._content = content
        self._metadata = metadata if metadata is not None else {}

    @property
    def document_id(self) -> str:
        """
        Get the document's unique identifier
        """
        return self._document_id
    
    @property
    def content(self) -> str:
        """
        Get the document's full content
        """
        return self._content
    
    @property
    def metadata(self) -> Dict:
        """
        Get the document's metadata
        """
        return self._metadata.copy() # Return a copy to prevent modification
    
    def __eq__(self, other: object) -> bool:
        """
        Compare this document with another for equality.
        Two documents are equal if the have the same ID and content.
        """
        if not isinstance(other, Document):
            return False
        
        return (
            self.document_id == other.document_id and
            self.content == other.content
        )
    
    def __repr__(self) -> str:
        """
        Return a string representation of the document.
        Useful for debugging.
        """
        return (
            f"Document(document_id='{self.document_id}', "
            f"content='{self.content[:50]}{'...' if len(self.content) > 50 else ''}', "
            f"metadata={self.metadata})"
        )