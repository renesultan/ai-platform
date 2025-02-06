# AI Platform Implementation

A progressive implementation of an AI platform based on Chip Huyen's architecture design blog post.

## Current State

### Project Structure

```
ai_platform/
├── src/
│   └── ai_platform/
│       ├── __init__.py
│       ├── common/           # Shared components
│       │   ├── __init__.py
│       │   └── types.py     # Shared data types (ModelResponse)
│       ├── model/           # Model interface components
│       │   ├── __init__.py
│       │   └── interface.py # ModelInterface implementation
│       └── retrieval/       # RAG system implementation
│           ├── __init__.py
│           ├── types.py     # Document and DocumentChunk classes
│           ├── document_store.py  # DocumentStore implementation
│           ├── chunk_embedder.py  # Chunk embedding management
│           ├── rag_store.py      # Complete RAG integration
│           ├── embeddings/   # Embedding functionality
│           │   ├── __init__.py
│           │   ├── interfaces.py  # Abstract embedding interfaces
│           │   └── models/        # Model implementations
│           │       ├── __init__.py
│           │       └── openai.py  # OpenAI embedding model
│           └── vector_store/  # Vector storage functionality
│               ├── __init__.py
│               ├── interfaces.py  # VectorStore interface
│               └── models/        # Concrete implementations
│                   ├── __init__.py
│                   └── faiss_store.py  # FAISS-based store
├── tests/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   └── test_types.py   # Tests for shared types
│   ├── model/
│   │   ├── __init__.py
│   │   └── test_interface.py # Tests for model interface
│   └── retrieval/           # RAG system tests
│       ├── __init__.py
│       ├── test_types.py    # Tests for Document/DocumentChunk
│       ├── test_document_store.py # Tests for DocumentStore
│       ├── test_chunk_embedder.py # Tests for ChunkEmbedder
│       ├── test_rag_store.py     # Tests for RAGStore
│       ├── embeddings/
│       │   ├── __init__.py
│       │   ├── test_interfaces.py # Tests for embedding interfaces
│       │   └── models/
│       │       ├── __init__.py
│       │       └── test_openai.py # Tests for OpenAI implementation
│       └── vector_store/
│           ├── __init__.py
│           ├── test_interfaces.py # Tests for VectorStore interface
│           └── test_faiss_store.py # Tests for FAISS store
├── CONTRIBUTING.md         # Development guidelines
├── requirements.txt       # Pinned dependencies
└── README.md
```

### Version Control

* Repository initialized with Git
* Branch structure:
  * `main`: Stable, production-ready code
  * `develop`: Integration branch for features
  * Feature branches: Component-specific development
* See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow and guidelines

### Implemented Components

1. **Basic AI API Integration**

   - **Common Types**:
     - `ModelResponse` class for consistent response handling
     - Supports both successful and error responses
     - Custom string representation for debugging
   - **Model Interface**:
     - `ModelInterface` class for OpenAI API integration
     - Environment-based or direct API key management
     - Comprehensive error handling
2. **Complete RAG System**

   - **Document Types**:
     - `Document` class for storing complete documents
     - `DocumentChunk` class for managing document segments
     - Support for metadata and unique identifiers
   - **Document Store**:
     - In-memory storage for documents and chunks
     - Configurable chunking strategy
     - Efficient document and chunk retrieval
     - Support for custom chunk sizes
   - **Embedding System**:
     - Abstract `EmbeddingModel` interface
     - Factory pattern for model creation
     - OpenAI embedding model implementation
     - Efficient embedding caching with `ChunkEmbedder`
   - **Vector Store**:
     - Abstract `VectorStore` interface
     - FAISS-based implementation for efficient similarity search
     - Support for dynamic updates and deletions
   - **Integrated RAG Store**:
     - Complete integration of all RAG components
     - Clean interface for document management
     - Efficient similarity search functionality
     - Comprehensive error handling and cleanup
     - Built-in caching through ChunkEmbedder

### Dependencies

Dependencies are pinned in `requirements.txt` for reproducibility:

- `openai`: AI API integration
- `python-dotenv`: Environment variable management
- `pytest`: Primary testing framework
- `pytest-asyncio`: Async test support
- `httpx`: HTTP client for API calls
- `faiss-cpu`: Vector similarity search
- `numpy`: Array operations for FAISS

## Testing

### Running All Tests

```bash
# Using pytest (recommended)
pytest

# Using unittest
python -m unittest discover
```

### Running Specific Tests

```bash
# Run tests for specific components
pytest tests/common/
pytest tests/model/
pytest tests/retrieval/

# Run specific test files
pytest tests/retrieval/test_types.py
pytest tests/retrieval/test_document_store.py
pytest tests/retrieval/test_chunk_embedder.py
pytest tests/retrieval/test_rag_store.py
pytest tests/retrieval/embeddings/test_interfaces.py
pytest tests/retrieval/embeddings/models/test_openai.py
pytest tests/retrieval/vector_store/test_faiss_store.py
```

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ai-platform.git
cd ai-platform
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run tests to verify setup:

```bash
pytest
```

## Usage Example

Here's a basic example of using the RAG system:

```python
from ai_platform.retrieval import (
    DocumentStore,
    RAGStore,
    EmbeddingModelFactory
)
from ai_platform.retrieval.vector_store.models.faiss_store import FAISSVectorStore

# Initialize components
document_store = DocumentStore(default_chunk_size=500)
vector_store = FAISSVectorStore(dimension=1536)  # OpenAI's embedding dimension
embedding_model = EmbeddingModelFactory.create(
    model_type="openai",
    api_key="your-api-key"
)

# Create RAG store
rag_store = RAGStore(
    document_store=document_store,
    vector_store=vector_store,
    embedding_model=embedding_model
)

# Add a document
doc_id = rag_store.add_document(
    content="Your document content here",
    metadata={"source": "example"}
)

# Find relevant chunks
results = rag_store.find_relevant_chunks(
    query="Your search query",
    k=3  # Number of results to return
)

# Process results
for chunk, score in results:
    print(f"Relevance score: {score}")
    print(f"Content: {chunk.text}")
```

## Roadmap

1. ✅ Basic OpenAI Integration

   - Model interface
   - Response handling
   - Error management
2. ✅ RAG System Implementation

   - Document representation
   - Chunking strategy
   - Document store implementation
   - Embedding system
   - Vector store
   - Complete RAG integration
3. 🔄 Input/Output Guardrails

   - Input validation
   - Output verification
   - Safety checks
4. Model Router and Gateway

   - Multiple model support
   - Request routing
   - API gateway
5. Caching Mechanisms

   - Response caching
   - Cache invalidation
   - Performance optimization

## Next Implementation Task

Current focus is on implementing input/output guardrails:

1. Input Validation

   - Content filtering
   - Safety checks
   - Rate limiting
2. Output Verification

   - Response validation
   - Quality checks
   - Safety filtering

## Development

For guidelines on branch strategy, commit messages, and workflow, see [CONTRIBUTING.md](CONTRIBUTING.md).
