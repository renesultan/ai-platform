"""
Basic document store implementation for RAG system.
Handles storage and basic operations for documents and chunks.
"""
import uuid
from typing import Dict, List, Optional
from .types import Document, DocumentChunk

class DocumentStore:
    """
    Simple in-memory document store that manages documents and their chunks.
    """
    def __init__(self, default_chunk_size: int = 500):
        """
        Initialize document store.

        Args:
            default_chunk_size: Default maximum size for document chunks
        """
        self._documents: Dict[str, Document] = {}
        self._chunks: Dict[str, DocumentChunk] = {}
        self._default_chunk_size = default_chunk_size

    def add_document(
            self,
            content: str,
            metadata: Optional[Dict] = None,
            chunk_size: Optional[int] = None
    ) -> str:
        """
        Add a document to the store and create its chunks.

        Args:
            content: The document text content
            metadata: Optional document metadata
            chunk_size: Optional custom chunk size for this document

        Returns:
            str: The generated document ID
        """
        # Generate unique ID
        doc_id = str(uuid.uuid4())

        # Create document
        document = Document(
            document_id=doc_id,
            content=content,
            metadata=metadata
        )

        # Create and store chunks
        chunks = self._create_chunks(
            content=content,
            doc_id=doc_id,
            chunk_size=chunk_size or self._default_chunk_size
        )

        # Store everything
        self._documents[doc_id] = document
        for chunk in chunks:
            self._chunks[chunk.chunk_id] = chunk

        return doc_id
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """
        Retrieve a document by ID.

        Args:
            document_id: The ID of the document to retrieve

        Returns:
            Document if found, None otherwise
        """
        return self._documents.get(document_id)

    def get_document_chunks(self, document_id: str) -> List[DocumentChunk]:
        """
        Get all chunks for a specific document.

        Args:
            document_id: The ID of the document

        Returns:
            List of chunks belonging to the document
        """
        return [
            chunk for chunk in self._chunks.values()
            if chunk.document_id == document_id
        ]
    
    def get_chunk(self, chunk_id: str) -> Optional[DocumentChunk]:
        """
        Retrieve a specific chunk by ID.

        Args:
            chunk_id: The ID of the chunk to retrieve

        Returns:
            DocumentChunk if found, None otherwise
        """
        return self._chunks.get(chunk_id)
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document and all its chunks.

        Args:
            document_id: The ID of the document to delete

        Returns:
            bool: True if document was found and deleted, False otherwise
        """
        if document_id not in self._documents:
            return False

        # Delete document
        del self._documents[document_id]

        # Find and delete all chunks for this document
        chunk_ids_to_delete = [
            chunk_id for chunk_id, chunk in self._chunks.items()
            if chunk.document_id == document_id
        ]

        for chunk_id in chunk_ids_to_delete:
            del self._chunks[chunk_id]

        return True
    
    def _create_chunks(
            self,
            content: str,
            doc_id: str,
            chunk_size: int
    ) -> List[DocumentChunk]:
        """
        Split document comment into chunks

        Args:
            content: The document text to split
            doc_id: The ID of the document these chunks belong to
            chunk_size: Maximum size for each chunk

        Returns:
            List of created DocumentChunk objects
        """
        chunks = []
        # Simple sentence-based splitting
        sentences = content.split('. ')
        current_chunk =[]
        current_length = 0

        for sentence in sentences:
            # Add period back to sentences unless ut's the last one
            if sentence != sentences[-1]:
                sentence = sentence + '.'

            sentence_length = len(sentence)

            if current_length + sentence_length > chunk_size and current_chunk:
                # Create chunk from accumulated sentences
                chunk_text = ' '.join(current_chunk)
                chunk = DocumentChunk(
                    chunk_id=str(uuid.uuid4()),
                    text=chunk_text,
                    document_id=doc_id
                )
                chunks.append(chunk)

                # Start new chunk
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        # Handle any remaining text
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunk = DocumentChunk(
                chunk_id=str(uuid.uuid4()),
                text=chunk_text,
                document_id=doc_id
            )
            chunks.append(chunk)

        return chunks