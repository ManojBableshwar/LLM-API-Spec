# llm-api-spec

**Black-box compatibility verification for LLM API endpoints.**

## What Is This?

`llm-api-spec` is a schema-aware verification framework that tests LLM API endpoints as black boxes. It answers one question:

> Given this endpoint, which capabilities work correctly, and which do not?

It sends real requests, inspects real responses, and reports observable behavior. It never assumes what's behind the endpoint.

## Why It Matters

Autonomous agents depend on LLM endpoints that claim to support certain features — tool calling, streaming, structured output, multimodal input. In practice, these features are inconsistently implemented across providers and runtimes.

**The problem:**
- Two endpoints exposing the same API shape may handle `tool_choice: "required"` differently
- An endpoint may accept `response_format: { type: "json_schema" }` but produce non-conformant output
- Streaming may partially work, or silently drop chunks
- There's no reliable way to know without testing

**The solution:**
`llm-api-spec` tests every capability independently, per schema, and reports exactly what works and what doesn't.

## How It's Different from Evals and Benchmarks

| | Evals/Benchmarks | llm-api-spec |
|---|---|---|
| **Tests** | Model reasoning quality | API surface compatibility |
| **Measures** | Accuracy, helpfulness | Supported vs unsupported features |
| **Assumes** | Known-good API behavior | Nothing about the backend |
| **Goal** | Rank model intelligence | Verify endpoint fidelity |

This project is **not** an eval framework, a benchmark, or a prompt testing tool.

## Quickstart

### Install

```bash
pip install -e ".[dev]"
```

### Run with inline target

```bash
llm-api-validate \
  --target https://api.openai.com/v1 \
  --model gpt-4o \
  --api-key $OPENAI_API_KEY \
  --schema chat_completions \
  --output markdown
```

### Run with config file

```bash
llm-api-validate --config configs/example_targets.yaml
```

### Run specific capabilities

```bash
llm-api-validate \
  --target https://api.example.com/v1 \
  --model my-model \
  --api-key $API_KEY \
  --capabilities text_input,text_output,tool_calling,streaming
```

### JSON output

```bash
llm-api-validate \
  --config configs/example_targets.yaml \
  --output json \
  --output-file results.json
```

### Debug mode (includes HTTP request/response payloads)

```bash
llm-api-validate \
  --config configs/example_targets.yaml \
  --debug \
  --output markdown \
  --output-file report_debug.md
```

### Filter a single target from a config file

```bash
llm-api-validate \
  --config configs/example_targets.yaml \
  --target my-target-name
```

When `--target` is used with `--config`, it filters by **target name** (not URL).

## CLI Usage

```
llm-api-validate [OPTIONS]

Options:
  --config PATH              YAML config file with target definitions
  --target TEXT               Inline target URL, or target name to filter from --config
  --model NAME               Model identifier (required with inline --target)
  --api-key KEY              API key (required with inline --target)
  --schema TYPE              chat_completions | responses | all (default: all)
  --capabilities LIST        Comma-separated list or 'all' (default: all)
  --output FORMAT            json | markdown (default: markdown)
  --output-file PATH         Write report to file
  --openapi-validation       Enable OpenAPI spec validation
  --timeout SECONDS          Request timeout (default: 60)
  --verbose                  Enable verbose logging
  --debug                    Log every HTTP request/response to stderr;
                             includes raw payloads in the report output
```

### Exit Codes

- `0` — all tests passed (or unsupported/not-applicable)
- `1` — one or more tests failed

## Sample Output

### Markdown Report

The default report includes a summary at the top and a results table per target/schema:

```markdown
# LLM API Compatibility Report

## Summary

my-endpoint — 17 passed, 1 failed, 5 unsupported, 7 n/a (out of 30)

---

## my-endpoint

### Chat Completions

| # | Capability | Result | Details |
|---|---|---|---|
| 1 | text_input | ✅ passed | Text input accepted and processed |
| 2 | text_output | ✅ passed | Response contains text content |
| 3 | tool_calling | ✅ passed | Tool call returned: get_weather |
| 4 | tool_choice_none | ❌ failed | tool_choice='none' did not suppress tool calls |
| 5 | streaming | ✅ passed | Streaming produced 15 chunks |
| 6 | image_input_url | ⚠️ unsupported | 400: model does not support image input |
| 7 | logprobs | ➖ n/a | Not applicable to this schema |
```

### Debug Markdown Report (`--debug`)

With `--debug`, the report adds a **Details** section with collapsible request/response payloads. Capability names in the table link to their detail anchors.

### Multi-Target Comparison

When multiple targets are tested in a single run, the report includes a side-by-side **Comparison** table:

```markdown
## Comparison

| # | Capability | openai-gpt54nano | azure-gpt54nano | azureml-gemma4 |
|---|-----------|:---:|:---:|:---:|
| 1 | text_input | ✅ | ✅ | ✅ |
| 2 | text_output | ✅ | ✅ | ✅ |
| 3 | json_output | ✅ | ✅ | ✅ |
| 4 | structured_output | ✅ | ✅ | ✅ |
| 5 | tool_calling | ✅ | ✅ | ✅ |
| 6 | streaming | ✅ | ✅ | ✅ |
| 7 | stop_sequences | ⚠️ | ⚠️ | ✅ |
| 8 | image_input_url | ✅ | ✅ | ✅ |
| 9 | image_output | ⚠️ | ⚠️ | ⚠️ |
| 10 | regex_constraints | ⚠️ | ⚠️ | ✅ |

✅ = passed · ❌ = failed · ⚠️ = unsupported · ➖ = n/a
```

This makes it easy to spot which capabilities differ across providers at a glance.

### Debug Markdown Report (`--debug`)

With `--debug`, the report adds a **Details** section with collapsible request/response payloads:

```markdown
## Details

### my-endpoint

#### <a id="my-endpoint-tool-calling">tool_calling</a>

✅ **passed**

> Tool call returned: get_weather

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-4o",
  "messages": [{"role": "user", "content": "What is the weather?"}],
  "tools": [...]
}
```

</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-abc123",
  "choices": [{"message": {"tool_calls": [...]}}]
}
```

</details>
```

Response payloads are automatically cleaned — `content_filter_results`, `usage`, `system_fingerprint`, and other noise fields are stripped for readability.

### JSON Report

```json
{
  "results": [
    {
      "target": "my-endpoint",
      "schema": "chat_completions",
      "capability": "text_input",
      "supported": true,
      "pass": true,
      "details": "Text input accepted and processed",
      "errors": []
    }
  ],
  "summary": {
    "total": 30,
    "passed": 22,
    "failed": 3,
    "unsupported": 5,
    "not_applicable": 0
  }
}
```

### Debug JSON Report (`--debug`)

With `--debug`, each result includes the raw HTTP payloads:

```json
{
  "target": "my-endpoint",
  "schema": "chat_completions",
  "capability": "tool_calling",
  "supported": true,
  "pass": true,
  "details": "Tool call returned: get_weather",
  "raw_request": { "model": "gpt-4o", "messages": [...], "tools": [...] },
  "raw_response": { "id": "chatcmpl-abc123", "choices": [...] },
  "normalized_response": { ... }
}
```

## Capability Matrix

Every capability is tested per-schema. Not all capabilities apply to all schemas:

| Capability | Chat Completions | Responses |
|---|:---:|:---:|
| text_input | ✓ | ✓ |
| text_output | ✓ | ✓ |
| json_output | ✓ | ✓ |
| structured_output | ✓ | ✓ |
| tool_calling | ✓ | ✓ |
| tool_choice variants | ✓ | ✓ |
| multiple_tool_calls | ✓ | ✓ |
| parallel_tool_calls | ✓ | ✓ |
| image_input (url/b64/multi) | ✓ | ✓ |
| image_output | ✓ | ✓ |
| file_input (inline/ref) | ✗ | ✓ |
| built_in_tools | ✗ | ✓ |
| streaming | ✓ | ✓ |
| stop_sequences | ✓ | ✓ |
| logprobs | ✓ | ✗ |
| seeded_determinism | ✓ | ✓ |
| long_prompt_acceptance | ✓ | ✓ |
| previous_response_id | ✗ | ✓ |
| background_mode | ✗ | ✓ |
| response_retrieval | ✗ | ✓ |
| regex/grammar/json_schema | ✓ | ✓ |

See [docs/spec.md](spec.md) for the complete specification.

## Architecture Overview

```
┌─────────────┐     ┌──────────────────┐     ┌────────────────┐
│     CLI      │────▶│     Runner       │────▶│  Capability    │
│              │     │                  │     │  Checks        │
└─────────────┘     └──────────────────┘     └────────────────┘
                           │                        │
                    ┌──────▼──────┐          ┌──────▼──────┐
                    │   Schema    │          │   OpenAPI   │
                    │   Adapters  │          │  Validator  │
                    ├─────────────┤          └─────────────┘
                    │ ChatComplet │
                    │ Responses   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Reporting  │
                    ├─────────────┤
                    │  JSON       │
                    │  Markdown   │
                    └─────────────┘
```

See [docs/architecture.md](architecture.md) for the full architecture document.
