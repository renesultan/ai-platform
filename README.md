# AI Platform Implementation

A progressive implementation of an AI platform based on Chip Huyen's architecture design blog post.

## Current State

### Project Structure

```
ai_platform/
├── src/
│   └── ai_platform/
│       ├── __init__.py
│       └── model.py  # ModelInterface with OpenAI integration
├── tests/
│   ├── __init__.py
│   └── test_model.py  # Unit tests for ModelInterface and ModelResponse
├── CONTRIBUTING.md    # Development guidelines and practices
├── requirements.txt   # Pinned dependencies
└── README.md
```

### Version Control

* Repository initialized with Git
* Branch structure:
  * `main`: Stable, production-ready code
  * `develop`: Integration branch for features
  * Feature branches: Component-specific development
* See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow and guidelines

### Implemented ComponentsDependencies

1. **Basic AI API Integration**

   - **ModelResponse class**: Holds text and/or error messages, with a custom `__str__` for easy debugging.
   - **ModelInterface class**: Uses the OpenAI `ChatCompletion.create` method, with environment-based or direct API key management.
   - **Robust Error Handling**:
     - Raises a `ValueError` if no API key is found.
     - Validates API responses (checks for an empty or missing `choices` field).
     - Catches and reports API errors.
   - **Unit Tests**:
     - Mocks OpenAI calls to avoid real API usage during testing.
     - Covers missing API keys, malformed responses, and general error cases.
2. **HTTP Request System (Legacy / Minimal)**

   - Initially set up for testing with `httpbin.org`.
   - Retained for reference but superseded by direct OpenAI integration in `ModelInterface`.

### Dependencies

Your dependencies are pinned in `requirements.txt` for reproducibility, including:

- `openai` (for AI API calls)
- `python-dotenv` (for managing `.env` environment variables)
- `pytest`, `pytest-asyncio`, and/or `unittest` (for testing)
- `httpx` or `urllib` (for any remaining HTTP requests, if needed)

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

### Current Implementation Details

#### ModelResponse Class

- Manages both successful outputs and error states
- Simple data structure with text and error fields
- Custom `__str__` method for clear debugging output

#### ModelInterface Class

- Integrates with OpenAI’s `ChatCompletion` endpoint
- Loads `OPENAI_API_KEY` from environment or constructor parameter
- Validates response structure (catches missing/empty `choices`)
- Handles errors robustly, returning a `ModelResponse` with error details

#### Testing

- **Comprehensive Unit Tests**:

  - **ModelResponse**: Ensures text/error fields and `__str__` behavior are correct
  - **ModelInterface**: Mocks OpenAI calls and tests success/error scenarios, including missing API keys and malformed responses
- Run with:

  ```bash
  python -m unittest discover tests
  ```

  or your preferred testing framework (eg., `pytest`).

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/renesultan/ai-platform.git
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

4. Run tests:

```bash
python -m unittest tests/test_model.py
```

-or-

```python
pytest
```

## Next Implementation Task

While the initial OpenAI integration is functional, there are still improvements to be made:

1. **Explore Additional Error Handling**
   * Catch specific OpenAI exceptions like `RateLimitError` or `AuthenticationError`
   * Provide user-friendly or automated-retry logic
2. **Experiment with Model Parameters**
   * Adjust temperature, max_tokens, etc.
   * Explore different models (e.g., GPT-4)
3. **Continue Progression**
   * Extend the platform with Retrieval Augmented Generation (RAG)
   * Implement guardrails for safer inputs/outputs
   * Build a model router/gateway for multiple AI providers

## Development

For guidelines on branch strategy, commit messages, and workflow, see [**CONTRIBUTING**.md](CONTRIBUTING.md).
