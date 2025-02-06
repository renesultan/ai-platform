"""
OpenAI embedding model implementation.
"""
from typing import List
from openai import OpenAI
from ..interfaces import EmbeddingModel

class OpenAIEmbedding(EmbeddingModel):
    """
    Implementation of embedding model using OpenAI's API.
    """
    def __init__(
            self,
            api_key: str,
            model_name: str = "text-embedding-ada-002"
    ):
        """
        Initialize OpenAI embedding model.

        Args:
            api_key: OpenAI API key
            model_name: Name of OpenAI embedding model to use
        """
        self._client = OpenAI(api_key=api_key)
        self._model_name = model_name
        # Ada-002 always produces 1536-dimensional embeddings
        self._dimension = 1536

    def generate_embedding(self, text:str) ->List[float]:
        """
        Generate embedding for a single text using OpenAI API.
        """
        if not text.strip():
            raise ValueError("Text cannot be empty")
        
        response = self._client.embeddings.create(
            model=self._model_name,
            input=text
        )

        return response.data[0].embedding
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in one API call.
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")
        
        if any(not text.strip() for text in texts):
            raise ValueError("All texts must be non-empty")
        
        response = self._client.embeddings.create(
            model=self._model_name,
            input=texts
        )

        return [data.embedding for data in response.data]
    
    @property
    def dimension(self) -> int:
        """
        Get embedding dimension.
        """
        return self._dimension
    
    @property
    def model_name(self) -> str:
        """
        Get model name.
        """
        return self._model_name