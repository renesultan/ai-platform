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
│       └── retrieval/       # Future RAG implementation
│           └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   └── test_types.py   # Tests for shared types
│   ├── model/
│   │   ├── __init__.py
│   │   └── test_interface.py # Tests for model interface
│   └── retrieval/           # Future RAG tests
│       └── __init__.py
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
     - Custom string representation for easy debugging
   - **Model Interface**:
     - `ModelInterface` class for OpenAI API integration
     - Environment-based or direct API key management
     - Comprehensive error handling
   - **Testing Infrastructure**:
     - Modular test organization matching source structure
     - Mocked OpenAI calls for reliable testing
     - Support for both unittest and pytest frameworks

### Dependencies

Dependencies are pinned in `requirements.txt` for reproducibility:

- `openai`: AI API integration
- `python-dotenv`: Environment variable management
- `pytest`: Primary testing framework
- `pytest-asyncio`: Async test support
- `httpx`: HTTP client for API calls

## Testing

The project supports multiple testing approaches:

### Running All Tests

```bash
# Using pytest (recommended)
pytest

# Using unittest
python -m unittest
python -m unittest discover
```

### Running Specific Tests

```bash
# Run tests in a specific file
pytest tests/common/test_types.py
pytest tests/model/test_interface.py

# Run tests using unittest
python -m unittest tests/common/test_types.py
python -m unittest tests/model/test_interface.py

# Run specific test class
python -m unittest tests.common.test_types.TestModelResponse
python -m unittest tests.model.test_interface.TestModelInterface

# Run specific test method
pytest tests/common/test_types.py::TestModelResponse::test_successful_response
python -m unittest tests.common.test_types.TestModelResponse.test_successful_response
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

1. Context Enhancement with RAG

   - Implement retrieval system
   - Document storage and indexing
   - Context integration with queries
2. Input/Output Guardrails

   - Input validation and sanitization
   - Output verification
   - Safety checks and filters
3. Model Router and Gateway

   - Multiple model support
   - Request routing logic
   - API gateway implementation
4. Caching Mechanisms

   - Response caching
   - Cache invalidation
   - Performance optimization
5. Complex Logic and Write Actions

   - Multi-step operations
   - Write operation support
   - Transaction management

## Next Implementation Task

While the initial OpenAI integration is functional, there are still improvements to be made:

1. **Document Storage and Indexing**

   - Implement document store
   - Add vector embeddings support
   - Create index management
2. **Context Integration**

   - Implement retrieval system
   - Integrate retrieved context with queries
   - Add context management
3. **Testing Strategy**

   - Unit tests for document store
   - Integration tests for retrieval
   - End-to-end RAG tests

## Development

For guidelines on branch strategy, commit messages, and workflow, see [**CONTRIBUTING**.md](CONTRIBUTING.md).
