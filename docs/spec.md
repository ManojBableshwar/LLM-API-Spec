# LLM API Specification — Black-Box Compatibility Verification

**Version:** 1.0.0
**Status:** Normative
**Date:** 2026-04-19

---

## 1. Problem Definition

### 1.1 What This Project Solves

Autonomous agents depend on LLM endpoints that expose HTTP APIs. These endpoints vary widely in their implementation: some are hosted by frontier providers, others are self-hosted via open-source inference engines, and still others are proxy layers or custom gateways.

Despite converging on similar API shapes (notably the Chat Completions and Responses schemas), these endpoints differ in which capabilities they actually support, how faithfully they conform to the schema, and whether their outputs are normalized consistently.

**llm-api-spec** provides a schema-aware, black-box verification framework that tests what an endpoint actually does — not what it claims to do. It answers a single question:

> *Given this endpoint, which capabilities work correctly, and which do not?*

### 1.2 Why Black-Box Verification Is Needed

1. **No reliable self-reporting.** Endpoints do not consistently advertise which features they support. A `/models` endpoint may list a model, but that tells you nothing about whether `tool_choice: "required"` actually works.

2. **Behavioral divergence is the norm.** Two endpoints exposing the same API shape may handle structured output, streaming, or tool calling in incompatible ways. Agents cannot discover this without testing.

3. **Backend opacity.** The system behind the endpoint may be vLLM, SGLang, TGI, llama.cpp, OpenAI, Anthropic, a custom proxy, or anything else. The caller has no way to know, and must not need to know. Verification must be purely observational.

4. **Agent reliability depends on endpoint fidelity.** An agent that relies on `parallel_tool_calls` will fail silently if the endpoint accepts the parameter but ignores it. Black-box testing catches this.

---

## 2. Core Abstractions

### 2.1 Endpoint Target

An **Endpoint Target** is a concrete HTTP endpoint to be verified. It is defined by:

| Field | Type | Description |
|---|---|---|
| `name` | `string` | Human-readable identifier |
| `base_url` | `string` | Base URL of the API (e.g., `https://api.example.com/v1`) |
| `api_key` | `string?` | Authentication token, if required |
| `model` | `string` | Model identifier to use in requests |
| `schemas` | `list[string]` | Which schemas to test (`chat_completions`, `responses`) |
| `headers` | `dict?` | Additional HTTP headers |
| `timeout` | `float?` | Request timeout in seconds |

A single verification run may include multiple targets.

### 2.2 Schema

A **Schema** defines a request/response contract. This project supports two schemas:

- **Chat Completions** (`chat_completions`): The `/v1/chat/completions` API shape.
- **Responses** (`responses`): The `/v1/responses` API shape.

Each schema has its own adapter that knows how to construct requests, parse responses, and normalize outputs for that schema.

### 2.3 Capability

A **Capability** is an observable behavior that an endpoint may or may not support. Capabilities are atomic and independently testable. Each capability is evaluated per-schema.

### 2.4 Validation Layers

Verification is performed through four distinct validation layers, applied in order:

1. **OpenAPI request validation** — does the outgoing request conform to the schema spec?
2. **OpenAPI response validation** — does the incoming response conform to the schema spec?
3. **Semantic capability validation** — does the endpoint actually exhibit the expected behavior?
4. **Normalization validation** — can the response be normalized to the canonical internal form?

---

## 3. Schema Definitions

### 3.1 Chat Completions Schema

The Chat Completions schema corresponds to the `/v1/chat/completions` endpoint. Its conceptual structure:

**Request:**
- `model`: string — model identifier
- `messages`: array — ordered list of message objects (`role`, `content`, optionally `tool_calls`, `tool_call_id`)
- `tools`: array? — tool/function definitions
- `tool_choice`: string | object? — tool selection strategy
- `parallel_tool_calls`: boolean? — whether multiple tools can be called simultaneously
- `response_format`: object? — constrains output format (e.g., `json_object`, `json_schema`)
- `stream`: boolean? — enable streaming
- `stop`: string | array? — stop sequences
- `logprobs`: boolean? — return log probabilities
- `top_logprobs`: integer? — number of top logprobs per token
- `seed`: integer? — deterministic seed
- `max_tokens`: integer? — maximum output tokens

**Response:**
- `id`: string — unique response identifier
- `object`: string — always `"chat.completion"`
- `model`: string — model used
- `choices`: array — list of completions, each with `message`, `finish_reason`, `index`
- `usage`: object — token counts (`prompt_tokens`, `completion_tokens`, `total_tokens`)

### 3.2 Responses Schema

The Responses schema corresponds to the `/v1/responses` endpoint. Its conceptual structure:

**Request:**
- `model`: string — model identifier
- `input`: string | array — input content (text or structured items)
- `tools`: array? — tool definitions (function, built-in)
- `tool_choice`: string | object? — tool selection strategy
- `parallel_tool_calls`: boolean? — whether multiple tools can be called simultaneously
- `text`: object? — text output configuration (format constraints)
- `stream`: boolean? — enable streaming
- `stop`: array? — stop sequences
- `previous_response_id`: string? — chain to a previous response
- `background`: boolean? — run in background mode
- `include`: array? — additional data to include in the response

**Response:**
- `id`: string — unique response identifier
- `object`: string — always `"response"`
- `model`: string — model used
- `output`: array — list of output items (messages, tool calls, etc.)
- `usage`: object — token counts
- `status`: string — response status (`completed`, `in_progress`, `failed`)

### 3.3 Key Differences Between Schemas

| Dimension | Chat Completions | Responses |
|---|---|---|
| Input shape | `messages` array (role/content pairs) | `input` (string or item array) |
| Output shape | `choices[].message` | `output[]` items |
| Streaming unit | `delta` chunks | Server-sent events with typed events |
| Tool definitions | `functions` in `tools` array | `function` and built-in tools |
| Response chaining | Not supported | `previous_response_id` |
| Background execution | Not supported | `background: true` |
| Built-in tools | Not supported | `web_search`, `file_search`, `code_interpreter` |
| Format constraints | `response_format` | `text.format` |
| Status tracking | Implicit via `finish_reason` | Explicit `status` field |

---

## 4. Capability Taxonomy

Each capability listed below is an independently verifiable behavior. Capabilities are tested per-schema.

### 4.1 text_input

The endpoint accepts plain text input and processes it without error.

- **Chat Completions:** A `messages` array with a single `user` message containing text content.
- **Responses:** An `input` field containing a plain string.
- **Verified by:** Sending a simple text prompt and receiving a non-error response.

### 4.2 text_output

The endpoint returns coherent text content in its response.

- **Chat Completions:** `choices[0].message.content` is a non-empty string.
- **Responses:** `output` contains a message item with text content.
- **Verified by:** Checking that the response contains extractable text content.

### 4.3 json_output

The endpoint can produce output that is valid JSON when instructed to do so.

- **Chat Completions:** Setting `response_format: { type: "json_object" }` and prompting for JSON.
- **Responses:** Setting `text.format: { type: "json_object" }` and prompting for JSON.
- **Verified by:** Parsing the output as JSON without error.

### 4.4 structured_output

The endpoint can produce output conforming to a provided JSON schema.

- **Chat Completions:** Setting `response_format: { type: "json_schema", json_schema: { ... } }`.
- **Responses:** Setting `text.format: { type: "json_schema", json_schema: { ... } }`.
- **Verified by:** Validating the output against the provided JSON schema.

### 4.5 tool_calling

The endpoint can invoke tool/function calls when tools are defined.

- **Chat Completions:** `tools` array with function definitions; response contains `tool_calls` in the message.
- **Responses:** `tools` array with function definitions; `output` contains `function_call` items.
- **Verified by:** Providing a tool definition and a prompt that should trigger it, then checking for a well-formed tool call in the response.

### 4.6 tool_choice Variants

The endpoint respects the `tool_choice` parameter across its valid values:

- `"auto"` — model decides whether to call a tool
- `"none"` — model must not call any tool
- `"required"` — model must call at least one tool
- `{ "type": "function", "function": { "name": "..." } }` — model must call a specific tool

**Verified by:** Sending requests with each `tool_choice` variant and confirming the response behavior matches the constraint.

### 4.7 multiple_tool_calls

The endpoint can return more than one tool call in a single response.

- **Verified by:** Providing multiple tools and a prompt that requires calling more than one, then confirming multiple tool calls appear in the response.

### 4.8 parallel_tool_calls

The endpoint respects the `parallel_tool_calls` parameter.

- When `true`: multiple tool calls may be returned simultaneously.
- When `false`: only one tool call should be returned per response.

**Verified by:** Sending requests with `parallel_tool_calls` set to both values and checking the response.

### 4.9 image_input

The endpoint can accept image data as input. Three sub-capabilities:

- **url**: Image provided as a URL reference.
- **base64**: Image provided as a base64-encoded data URI.
- **multi**: Multiple images in a single request.

**Verified by:** Sending requests with image content and confirming the response acknowledges the image content.

### 4.10 image_output

The endpoint can generate images as part of its output.

- **Verified by:** Requesting image generation and confirming the response contains image data or a URL.

### 4.11 file_input

The endpoint can accept file data as input. Two sub-capabilities:

- **inline**: File content provided directly in the request body.
- **reference**: File referenced by ID or URL.

**Verified by:** Sending requests with file content and confirming the response processes the file.

### 4.12 built_in_tools

The endpoint supports built-in tools (e.g., `web_search`, `file_search`, `code_interpreter`).

- **Applicable primarily to the Responses schema.**
- **Verified by:** Including a built-in tool definition and confirming the endpoint processes it.

### 4.13 streaming

The endpoint supports streaming responses via server-sent events (SSE).

- **Chat Completions:** `stream: true` returns `data:` lines with `delta` objects.
- **Responses:** `stream: true` returns typed SSE events.
- **Verified by:** Sending a streaming request and successfully consuming chunks until completion.

### 4.14 stop_sequences

The endpoint respects custom stop sequences.

- **Verified by:** Providing a stop sequence and confirming the output terminates at that sequence.

### 4.15 logprobs

The endpoint can return log probabilities for output tokens.

- **Chat Completions:** `logprobs: true` with optional `top_logprobs`.
- **Verified by:** Confirming the response contains logprob data with valid probability values.

### 4.16 seeded_determinism

The endpoint produces deterministic output when a `seed` parameter is provided.

- **Verified by:** Sending the same request with the same seed twice and comparing outputs.

### 4.17 long_prompt_acceptance

The endpoint can accept and process long input prompts without errors.

- **Verified by:** Sending a prompt of substantial length (e.g., 8,000+ tokens) and receiving a valid response.

### 4.18 previous_response_id

The endpoint supports response chaining via `previous_response_id`.

- **Applicable primarily to the Responses schema.**
- **Verified by:** Creating a response, then sending a follow-up request referencing its ID, and confirming contextual continuity.

### 4.19 background_mode

The endpoint supports background execution via `background: true`.

- **Applicable primarily to the Responses schema.**
- **Verified by:** Sending a background request and receiving a response with `status: "in_progress"` or retrievable later.

### 4.20 response_retrieval

The endpoint supports retrieving a previously created response by ID.

- **Applicable primarily to the Responses schema.**
- **Verified by:** Creating a response and then retrieving it via `GET /v1/responses/{id}`.

### 4.21 normalization

The endpoint's output can be normalized to a canonical internal representation.

- **Verified by:** Running the normalization layer and confirming it produces a valid normalized response without errors.

### 4.22 regex_constraints

The endpoint can constrain output to match a regular expression pattern.

- **Verified by:** Providing a regex constraint and validating the output matches the pattern.

### 4.23 grammar_constraints

The endpoint can constrain output to conform to a formal grammar (e.g., GBNF, EBNF).

- **Verified by:** Providing a grammar constraint and validating the output conforms.

### 4.24 json_schema_constraints

The endpoint can enforce a JSON schema on its output (overlaps with `structured_output` but may be tested via different mechanisms such as `text.format`).

- **Verified by:** Providing a JSON schema constraint and validating the output against it.

---

## 5. Capability × Schema Matrix

Every capability must be evaluated independently for each supported schema. The combination of `(target, schema, capability)` forms the primary key for all results.

Not every capability applies to every schema. The following matrix defines applicability:

| Capability | Chat Completions | Responses |
|---|:---:|:---:|
| text_input | ✓ | ✓ |
| text_output | ✓ | ✓ |
| json_output | ✓ | ✓ |
| structured_output | ✓ | ✓ |
| tool_calling | ✓ | ✓ |
| tool_choice_auto | ✓ | ✓ |
| tool_choice_none | ✓ | ✓ |
| tool_choice_required | ✓ | ✓ |
| tool_choice_function | ✓ | ✓ |
| multiple_tool_calls | ✓ | ✓ |
| parallel_tool_calls | ✓ | ✓ |
| image_input_url | ✓ | ✓ |
| image_input_base64 | ✓ | ✓ |
| image_input_multi | ✓ | ✓ |
| image_output | ✓ | ✓ |
| file_input_inline | ✗ | ✓ |
| file_input_reference | ✗ | ✓ |
| built_in_tools | ✗ | ✓ |
| streaming | ✓ | ✓ |
| stop_sequences | ✓ | ✓ |
| logprobs | ✓ | ✗ |
| seeded_determinism | ✓ | ✓ |
| long_prompt_acceptance | ✓ | ✓ |
| previous_response_id | ✗ | ✓ |
| background_mode | ✗ | ✓ |
| response_retrieval | ✗ | ✓ |
| normalization | ✓ | ✓ |
| regex_constraints | ✓ | ✓ |
| grammar_constraints | ✓ | ✓ |
| json_schema_constraints | ✓ | ✓ |

When a capability is not applicable to a schema, it is reported as `not_applicable` (distinct from `unsupported`).

---

## 6. Validation Layers

Verification proceeds through four ordered validation layers. Each layer produces independent results.

### 6.1 OpenAPI Request Validation

Before sending a request, it may optionally be validated against the official OpenAPI specification for the target schema.

- **Input:** Constructed request body.
- **Output:** `request_schema_valid: true | false` with a list of validation errors.
- **Behavior:** This layer is advisory. A request that fails OpenAPI validation is still sent (the endpoint may accept non-conformant requests). The validation result is recorded independently.

### 6.2 OpenAPI Response Validation

After receiving a response, it may optionally be validated against the official OpenAPI specification.

- **Input:** Raw response body.
- **Output:** `response_schema_valid: true | false` with a list of validation errors.
- **Behavior:** This layer is advisory. A response that fails OpenAPI validation may still pass semantic validation.

### 6.3 Semantic Capability Validation

The core validation layer. Each capability check sends a request designed to exercise a specific behavior, then inspects the response to determine whether the behavior is correctly exhibited.

- **Input:** Constructed request (via the schema adapter) and raw response.
- **Output:** `supported: true | false`, `pass: true | false`, and `details` describing what was observed.
- **Behavior:**
  - If the endpoint returns an error indicating the feature is not supported, the capability is marked `supported: false`.
  - If the endpoint returns a response but the expected behavior is not observed, the capability is marked `supported: true, pass: false`.
  - If the expected behavior is correctly observed, the capability is marked `supported: true, pass: true`.

### 6.4 Normalization Validation

After semantic validation, the response is passed through the normalization layer.

- **Input:** Raw response.
- **Output:** `normalized_response` and `normalization_valid: true | false`.
- **Behavior:** Normalization converts schema-specific responses into a canonical form. If normalization fails or produces an invalid result, this is recorded.

---

## 7. Result Model

Every capability check produces a `CapabilityResult` keyed by `(target, schema, capability)`.

### 7.1 Result Fields

| Field | Type | Description |
|---|---|---|
| `target` | `string` | Endpoint target name |
| `schema` | `string` | Schema tested (`chat_completions` or `responses`) |
| `capability` | `string` | Capability identifier |
| `supported` | `bool?` | Whether the endpoint supports this capability (`null` if not tested) |
| `pass` | `bool?` | Whether the capability check passed (`null` if not supported or not tested) |
| `request_schema_valid` | `bool?` | Whether the request conformed to the OpenAPI spec |
| `response_schema_valid` | `bool?` | Whether the response conformed to the OpenAPI spec |
| `normalized` | `bool?` | Whether the response was successfully normalized |
| `details` | `string?` | Human-readable description of the result |
| `raw_request` | `object?` | The request that was sent |
| `raw_response` | `object?` | The response that was received |
| `normalized_response` | `object?` | The normalized response, if normalization succeeded |
| `errors` | `list[string]` | List of errors encountered during verification |

### 7.2 Result States

A capability check resolves to one of four terminal states:

| State | `supported` | `pass` | Meaning |
|---|---|---|---|
| **passed** | `true` | `true` | Capability works correctly |
| **failed** | `true` | `false` | Capability is supported but behaves incorrectly |
| **unsupported** | `false` | `null` | Endpoint does not support this capability |
| **not_applicable** | `null` | `null` | Capability does not apply to this schema |

Additionally, schema validation results are orthogonal:

| Schema State | Meaning |
|---|---|
| **schema-valid** | Request or response conforms to the OpenAPI spec |
| **schema-invalid** | Request or response does not conform to the OpenAPI spec |

And normalization results:

| Normalization State | Meaning |
|---|---|
| **normalized** | Response was successfully converted to canonical form |
| **non-normalized** | Normalization failed or produced invalid output |

---

## 8. Black-Box Guarantees

This specification enforces strict black-box semantics. The following guarantees are normative:

### 8.1 No Runtime Inference

The system MUST NOT attempt to detect, infer, or identify the runtime, inference engine, or software stack behind an endpoint. It does not matter whether the backend is vLLM, SGLang, TGI, llama.cpp, OpenAI, Anthropic, Mistral, or any other system.

### 8.2 No Backend Assumptions

The system MUST NOT include any code paths, branching logic, or special behavior conditioned on the identity of the backend. There are no backend-specific adapters, quirks tables, or compatibility shims.

### 8.3 No Special Casing

All endpoints are tested identically. The same request is sent, the same response parsing is applied, and the same validation criteria are used, regardless of the target. The only configuration that varies between targets is what is specified in the `EndpointTarget` definition (URL, model, authentication, schemas).

### 8.4 Observable Behavior Only

All verification is based exclusively on:

- HTTP status codes
- Response headers
- Response bodies
- SSE event streams
- Timing characteristics (for timeout detection only)

No out-of-band information is used.

---

## 9. Non-Goals

The following are explicitly out of scope for this project:

### 9.1 Not a Benchmark

This project does not measure latency, throughput, tokens-per-second, time-to-first-token, or any performance metric. It does not rank endpoints.

### 9.2 Not an Eval Framework

This project does not evaluate the quality, accuracy, helpfulness, or reasoning ability of model outputs. It does not score responses against ground truth. It does not measure MMLU, HumanEval, or any evaluation benchmark.

### 9.3 Not a Prompt Testing Tool

This project does not test whether specific prompts produce desired outputs. It does not support prompt engineering, prompt regression testing, or A/B testing of prompt variants.

### 9.4 Not an Agent Framework

This project does not execute multi-step agent loops, manage tool-call round trips, or orchestrate LLM-driven workflows. It verifies that the endpoint primitives that agents depend on actually work.

---

## 10. CLI Behavior

### 10.1 Invocation

The primary interface is the `llm-api-validate` CLI command.

```
llm-api-validate [OPTIONS]
```

### 10.2 Options

| Option | Type | Default | Description |
|---|---|---|---|
| `--config` | `path` | — | Path to a YAML configuration file defining targets |
| `--target` | `string` | — | Inline target specification (URL) |
| `--model` | `string` | — | Model identifier (required with `--target`) |
| `--api-key` | `string` | — | API key (required with `--target`) |
| `--schema` | `string` | `all` | Schemas to test: `chat_completions`, `responses`, `all` |
| `--capabilities` | `string` | `all` | Comma-separated list of capabilities to test, or `all` |
| `--output` | `string` | `markdown` | Output format: `json` or `markdown` |
| `--output-file` | `path` | — | Write output to file instead of stdout |
| `--openapi-validation` | `bool` | `false` | Enable OpenAPI request/response validation |
| `--timeout` | `float` | `60.0` | Request timeout in seconds |
| `--verbose` | `bool` | `false` | Enable verbose output |

### 10.3 Configuration File

A YAML configuration file may define one or more targets:

```yaml
targets:
  - name: my-endpoint
    base_url: https://api.example.com/v1
    api_key: ${MY_API_KEY}
    model: gpt-4o
    schemas:
      - chat_completions
      - responses
    timeout: 120
    headers:
      X-Custom-Header: value
```

Environment variable substitution is supported via `${VAR_NAME}` syntax.

### 10.4 Output

**Markdown output** (default) produces a human-readable report:

```
# LLM API Compatibility Report

## Target: my-endpoint
**Base URL:** https://api.example.com/v1
**Model:** gpt-4o

### Chat Completions Schema

| Capability | Supported | Pass | Schema Valid |
|---|---|---|---|
| text_input | ✓ | ✓ | ✓ |
| text_output | ✓ | ✓ | ✓ |
| tool_calling | ✓ | ✗ | ✓ |
| streaming | ✗ | — | — |

### Summary
Passed: 15 / 20
Unsupported: 3
Failed: 2
```

**JSON output** produces a machine-readable report with full result details:

```json
{
  "results": [
    {
      "target": "my-endpoint",
      "schema": "chat_completions",
      "capability": "text_input",
      "supported": true,
      "pass": true,
      "request_schema_valid": true,
      "response_schema_valid": true,
      "normalized": true,
      "details": "Text input accepted and processed",
      "errors": []
    }
  ],
  "summary": {
    "total": 20,
    "passed": 15,
    "failed": 2,
    "unsupported": 3,
    "not_applicable": 0
  }
}
```

### 10.5 Exit Codes

| Code | Meaning |
|---|---|
| `0` | All applicable capability checks passed |
| `1` | One or more capability checks failed |
| `2` | Configuration or invocation error |

---

## Appendix A: Glossary

| Term | Definition |
|---|---|
| **Adapter** | A schema-specific module that constructs requests and parses responses |
| **Capability** | An independently verifiable endpoint behavior |
| **Capability Check** | A test that exercises a single capability and produces a result |
| **Normalization** | Converting a schema-specific response into a canonical internal form |
| **Schema** | A request/response contract (Chat Completions or Responses) |
| **Target** | A specific HTTP endpoint to be verified |
| **Validation Layer** | One of four ordered stages of verification |

---

## Appendix B: Capability Identifiers

The canonical identifiers for all capabilities:

```
text_input
text_output
json_output
structured_output
tool_calling
tool_choice_auto
tool_choice_none
tool_choice_required
tool_choice_function
multiple_tool_calls
parallel_tool_calls
image_input_url
image_input_base64
image_input_multi
image_output
file_input_inline
file_input_reference
built_in_tools
streaming
stop_sequences
logprobs
seeded_determinism
long_prompt_acceptance
previous_response_id
background_mode
response_retrieval
normalization
regex_constraints
grammar_constraints
json_schema_constraints
```
