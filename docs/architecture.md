# Architecture

## System Design

`llm-api-spec` is organized around four primary components:

1. **CLI** — parses user input, loads configuration, invokes the runner
2. **Runner** — orchestrates capability checks across targets and schemas
3. **Schema Adapters** — build requests, send them, parse and normalize responses
4. **Capability Checks** — individual verification functions for each capability

Supporting components:

5. **OpenAPI Validator** — optional request/response validation against OpenAPI specs
6. **Reporting** — transforms results into JSON or Markdown output

## Data Flow

```
User Input (CLI args or config file)
         │
         ▼
    ┌─────────┐
    │   CLI   │  Parse args, load YAML config, resolve env vars
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │ Runner  │  For each (target, schema):
    └────┬────┘    For each capability:
         │           1. Check applicability
         │           2. Get adapter
         │           3. Run check
         │           4. Apply OpenAPI validation (if enabled)
         ▼
    ┌──────────────────┐
    │ Schema Adapter   │  Build request → Send HTTP → Parse response → Normalize
    │ (Chat/Responses) │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ Capability Check │  Send constructed request, inspect response,
    │                  │  determine supported/pass/fail
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ CapabilityResult │  target + schema + capability + supported + pass + details
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │    Reporter      │  Aggregate results → JSON or Markdown
    └──────────────────┘
```

## Adapter Model

### Base Adapter (`SchemaAdapter`)

Abstract base class providing:

- `get_client()` — returns a configured `httpx.AsyncClient`
- `send_request(body)` — sends a POST to the schema endpoint
- `send_and_parse(body)` — sends request, parses response
- `close()` — closes the HTTP client

Subclasses MUST implement:

| Method | Purpose |
|---|---|
| `endpoint_path()` | Returns the API path (e.g., `/chat/completions`) |
| `build_request(**kwargs)` | Constructs a request body from keyword arguments |
| `parse_response(data)` | Parses raw response into structured form |
| `normalize(data)` | Converts response to `NormalizedResponse` |
| `stream_response(body)` | Sends streaming request, yields parsed chunks |

### ChatCompletionsAdapter

- Endpoint: `/chat/completions`
- Builds messages-based requests
- Parses `choices[0].message` for content and tool calls
- Normalizes usage from `prompt_tokens`/`completion_tokens`/`total_tokens`
- Streams via `data:` SSE lines with `delta` objects

### ResponsesAdapter

- Endpoint: `/responses`
- Builds input-based requests (string or item array)
- Parses `output[]` items for messages and function calls
- Normalizes usage from `input_tokens`/`output_tokens`
- Streams via typed SSE events
- Supports `retrieve_response(id)` via GET

## Normalization Design

All schema-specific responses are normalized to `NormalizedResponse`:

```
NormalizedResponse
├── text: str | None           # Extracted text content
├── tool_calls: list           # Normalized tool call objects
│   ├── id: str | None
│   ├── name: str
│   └── arguments: str (JSON)
├── finish_reason: str | None  # Why the response ended
├── model: str | None          # Model identifier
├── usage: NormalizedUsage     # Token counts
│   ├── prompt_tokens
│   ├── completion_tokens
│   └── total_tokens
└── response_id: str | None    # Response identifier
```

Normalization goals:
- **Uniform access** — downstream code works with one structure regardless of schema
- **Lossless mapping** — all semantically meaningful fields are preserved
- **Fail-safe** — missing fields default to `None` or empty lists, no exceptions

## Capability Check Design

Each capability check is an async function with signature:

```python
async def check_<capability>(adapter: SchemaAdapter) -> CapabilityResult
```

Checks follow this pattern:
1. Build a request using the adapter
2. Send it and get the response
3. Inspect the response for expected behavior
4. Return a `CapabilityResult` with `supported`, `pass`, and `details`

Error handling:
- HTTP errors (4xx, 5xx) → `supported=False`
- Correct response but wrong behavior → `supported=True, pass=False`
- Correct behavior → `supported=True, pass=True`

## Result Model

Results are keyed by `(target, schema, capability)` and resolve to one of:

| State | supported | pass | Meaning |
|---|---|---|---|
| passed | true | true | Works correctly |
| failed | true | false | Supported but incorrect |
| unsupported | false | null | Not supported |
| not_applicable | null | null | Doesn't apply to this schema |

## Module Layout

```
llm_api_spec/
├── __init__.py
├── models.py               # Pydantic data models
├── cli.py                  # Click CLI entry point
├── runner.py               # Orchestration logic
├── openapi_validation.py   # OpenAPI spec validation
├── adapters/
│   ├── base.py             # SchemaAdapter ABC
│   ├── chat_completions.py # Chat Completions adapter
│   └── responses.py        # Responses adapter
├── checks/
│   ├── basic_text.py       # text_input, text_output, stop_sequences
│   ├── tool_calling.py     # All tool-related checks
│   ├── structured_output.py # JSON, schema, regex, grammar
│   ├── multimodal.py       # Image input/output
│   ├── file_input.py       # File input (inline, reference)
│   ├── lifecycle.py        # Chaining, background, retrieval, built-in tools
│   ├── streaming.py        # Streaming check
│   ├── logprobs.py         # Log probabilities
│   ├── determinism.py      # Seeded determinism
│   ├── long_context.py     # Long prompt acceptance
│   └── normalization.py    # Normalization verification
├── reporting/
│   ├── json_report.py      # JSON output
│   └── markdown_report.py  # Markdown output
└── schemas/
    └── fixtures/            # OpenAPI spec fixtures (optional)
```
