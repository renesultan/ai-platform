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
│           ├── embeddings/   # Embedding functionality
│           │   ├── __init__.py
│           │   ├── interfaces.py  # Abstract embedding interfaces
│           │   └── models/        # Model implementations
│           │       ├── __init__.py
│           │       └── openai.py  # OpenAI embedding model
│           └── vector_store/  # Vector storage functionality
│               ├── __init__.py
│               ├── interfaces.py  # VectorStore interface
│               └── implementations/ # Concrete implementations
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
│       ├── embeddings/
│       │   ├── __init__.py
│       │   ├── test_interfaces.py # Tests for embedding interfaces
│       │   └── models/
│       │       ├── __init__.py
│       │       └── test_openai.py # Tests for OpenAI implementation
│       └── vector_store/
│           ├── __init__.py
│           ├── test_interfaces.py # Tests for VectorStore interface
│           └── implementations/
│               ├── __init__.py
│               └── test_faiss_store.py # Tests for FAISS store
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
2. **RAG System Foundation**

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
     - Comprehensive testing suite
   - **Vector Store**:
     - Abstract `VectorStore` interface
     - FAISS-based implementation for efficient similarity search
     - Support for dynamic updates and deletions
     - Comprehensive testing suite

### Dependencies

Dependencies are pinned in `requirements.txt` for reproducibility:

- `openai`: AI API integration
- `python-dotenv`: Environment variable management
- `pytest`: Primary testing framework
- `pytest-asyncio`: Async test support
- `httpx`: HTTP client for API calls
- `faiss-cpu`: Vector similarity search

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
pytest tests/retrieval/embeddings/test_interfaces.py
pytest tests/retrieval/embeddings/models/test_openai.py
pytest tests/retrieval/vector_store/implementations/test_faiss_store.py
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

## Roadmap

1. ✅ Basic OpenAI Integration

   - Model interface
   - Response handling
   - Error management
2. ✅ RAG System Foundation

   - Document representation
   - Basic chunking strategy
   - Document store implementation
3. 🔄 RAG System Enhancement

   - ✅ Initial embedding interfaces
   - ✅ OpenAI embedding implementation
   - ✅ Vector storage interface
   - ✅ FAISS vector store implementation
   - ⏳ Context integration
4. Input/Output Guardrails

   - Input validation
   - Output verification
   - Safety checks
5. Model Router and Gateway

   - Multiple model support
   - Request routing
   - API gateway
6. Caching Mechanisms

   - Response caching
   - Cache invalidation
   - Performance optimization

## Next Implementation Task

Current focus is on completing the RAG system enhancement with:

1. Context Integration

   - Integration of DocumentStore with VectorStore
   - Relevance-based document retrieval
   - Context window management
   - Query enhancement with context
2. Testing Strategy

   - Integration tests for RAG system
   - End-to-end RAG tests
   - Performance benchmarks

## Development

For guidelines on branch strategy, commit messages, and workflow, see [CONTRIBUTING.md](CONTRIBUTING.md).
