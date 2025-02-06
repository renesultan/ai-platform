"""
Abstract interfaces for embedding functionality.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

class EmbeddingModel(ABC):
    """
    Abstract interface for embedding models.
    Defines how different embedding models should behave.
    """
    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for a single text.

        Args:
            text: The text to embed

        Returns:
            List of floats representing the embedding vector

        Raises:
            ValueError: If text is empty or invalid
        """
        pass

    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[float]:
        """
        Generate embeddings for multiple texts efficiently.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors (each a list of floats)

        Raises:
            ValueError: If any texts are empty or invalid
        """
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Get the dimension of embedding vectors produced by this model.
        """
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Get the name/identifier of this embedding model.
        """
        pass

class EmbeddingModelFactory:
    """
    Factory class for creating embedding models.
    Allows easy creation of different model types.
    """
    @staticmethod
    def create(
        model_type: str,
        api_key: Optional[str]= None,
        **kwargs
    ) -> EmbeddingModel:
        """
        Create an embedding model of the specified type.

        Args:
            model_type: Type of model to create(e.g., "openai")
            pi_key: Optional API key for hosted models
            **kwargs: Additional model-specific parameters

        Returns:
            An instance of EmbeddingModel

        Raises:
            ValueError: If model_type is unknown
        """
        # Import implementations here to avoid circular imports
        from .models.openai import OpenAIEmbedding

        if model_type.lower() == "openai":
            if not api_key:
                raise ValueError("OpenAI model requires an API key")
            return OpenAIEmbedding(api_key=api_key, **kwargs)
        
        raise ValueError(f"Unknown model type: {model_type}")
