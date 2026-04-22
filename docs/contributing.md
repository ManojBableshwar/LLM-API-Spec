# Contributing

## How to Extend Capabilities

### Adding a New Capability Check

1. **Define the capability** in `llm_api_spec/models.py`:

```python
class Capability(str, Enum):
    # ... existing capabilities ...
    MY_NEW_CAPABILITY = "my_new_capability"
```

2. **Update applicability** if the capability is schema-specific:

```python
# In models.py
RESPONSES_ONLY: set[Capability] = {
    # ... add here if responses-only
    Capability.MY_NEW_CAPABILITY,
}
```

3. **Create the check function** in the appropriate file under `llm_api_spec/checks/`:

```python
async def check_my_new_capability(adapter: SchemaAdapter) -> CapabilityResult:
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.MY_NEW_CAPABILITY,
    )

    request_body = adapter.build_request(
        prompt="Your test prompt here",
        # ... any additional parameters
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        # Your verification logic here
        normalized = adapter.normalize(raw)
        if your_condition(normalized):
            result.passed = True
            result.details = "Capability works correctly"
        else:
            result.passed = False
            result.details = "Capability did not exhibit expected behavior"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Check failed: {exc}"

    return result
```

4. **Register it** in `llm_api_spec/checks/__init__.py`:

```python
from llm_api_spec.checks.your_module import check_my_new_capability

CAPABILITY_CHECK_MAP[Capability.MY_NEW_CAPABILITY] = check_my_new_capability
```

5. **Write tests** in `tests/`:

```python
@respx.mock
@pytest.mark.asyncio
async def test_my_new_capability_success(self, chat_target):
    respx.post("https://...").mock(return_value=httpx.Response(200, json={...}))
    adapter = ChatCompletionsAdapter(chat_target)
    result = await check_my_new_capability(adapter)
    assert result.passed is True
    await adapter.close()
```

### Guidelines for Capability Checks

- **One capability, one function** — each check tests exactly one behavior
- **No test logic in adapters** — adapters build/send/parse, checks verify
- **No backend assumptions** — never branch on backend identity
- **Handle errors gracefully** — HTTP errors → `unsupported`, not crashes
- **Record everything** — always populate `raw_request`, `raw_response`, `details`, `errors`

## How to Add New Schema Adapters

If a new API schema emerges (beyond Chat Completions and Responses):

1. **Add the schema type** to `SchemaType` enum in `models.py`:

```python
class SchemaType(str, Enum):
    CHAT_COMPLETIONS = "chat_completions"
    RESPONSES = "responses"
    NEW_SCHEMA = "new_schema"
```

2. **Create the adapter** in `llm_api_spec/adapters/new_schema.py`:

```python
class NewSchemaAdapter(SchemaAdapter):
    schema_type = SchemaType.NEW_SCHEMA

    def endpoint_path(self) -> str:
        return "/new-endpoint"

    def build_request(self, **kwargs) -> dict[str, Any]:
        # Schema-specific request construction
        ...

    def parse_response(self, response_data: dict[str, Any]) -> dict[str, Any]:
        # Schema-specific response parsing
        ...

    def normalize(self, response_data: dict[str, Any]) -> NormalizedResponse:
        # Convert to canonical NormalizedResponse
        ...

    async def stream_response(self, request_body: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        # Handle streaming for this schema
        ...
```

3. **Register it** in `llm_api_spec/runner.py`:

```python
def get_adapter(target, schema):
    if schema == SchemaType.NEW_SCHEMA:
        return NewSchemaAdapter(target)
    ...
```

4. **Update applicability** — define which capabilities apply to the new schema in `models.py`

5. **Write adapter tests** covering `build_request`, `parse_response`, and `normalize`

### Adapter Contract

Every adapter MUST:
- Implement all abstract methods from `SchemaAdapter`
- Use `self.target.model` in built requests
- Return `NormalizedResponse` from `normalize()` without raising (use defaults for missing fields)
- Handle streaming via async iterator yielding parsed chunks
- NOT contain any test/verification logic

## Development Setup

```bash
# Clone
git clone <repository-url>
cd llm-api-spec

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check llm_api_spec/ tests/
```

## Code Style

- Python 3.10+
- Type annotations everywhere
- `async/await` for all HTTP operations
- Pydantic for data models
- Click for CLI
- httpx for HTTP client
- pytest + respx for testing
