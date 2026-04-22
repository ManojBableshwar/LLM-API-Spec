# LLM API Compatibility Report

## Summary

**openai-gpt54nano** — 20 passed, 0 failed, 4 unsupported, 6 n/a (out of 30)

**azure-gpt54nano** — 20 passed, 0 failed, 4 unsupported, 6 n/a (out of 30)

**azureml-gemma4** — 22 passed, 0 failed, 2 unsupported, 6 n/a (out of 30)

---

## Comparison

| # | Capability | openai-gpt54nano | azure-gpt54nano | azureml-gemma4 |
|---|-----------|:---:|:---:|:---:|
| 1 | text_input | ✅ | ✅ | ✅ |
| 2 | text_output | ✅ | ✅ | ✅ |
| 3 | json_output | ✅ | ✅ | ✅ |
| 4 | structured_output | ✅ | ✅ | ✅ |
| 5 | tool_calling | ✅ | ✅ | ✅ |
| 6 | tool_choice_auto | ✅ | ✅ | ✅ |
| 7 | tool_choice_none | ✅ | ✅ | ✅ |
| 8 | tool_choice_required | ✅ | ✅ | ✅ |
| 9 | tool_choice_function | ✅ | ✅ | ✅ |
| 10 | multiple_tool_calls | ✅ | ✅ | ✅ |
| 11 | parallel_tool_calls | ✅ | ✅ | ✅ |
| 12 | image_input_url | ✅ | ✅ | ✅ |
| 13 | image_input_base64 | ✅ | ✅ | ✅ |
| 14 | image_input_multi | ✅ | ✅ | ✅ |
| 15 | image_output | ⚠️ | ⚠️ | ⚠️ |
| 16 | file_input_inline | ➖ | ➖ | ➖ |
| 17 | file_input_reference | ➖ | ➖ | ➖ |
| 18 | built_in_tools | ➖ | ➖ | ➖ |
| 19 | streaming | ✅ | ✅ | ✅ |
| 20 | stop_sequences | ⚠️ | ⚠️ | ✅ |
| 21 | logprobs | ✅ | ✅ | ✅ |
| 22 | seeded_determinism | ✅ | ✅ | ✅ |
| 23 | long_prompt_acceptance | ✅ | ✅ | ✅ |
| 24 | previous_response_id | ➖ | ➖ | ➖ |
| 25 | background_mode | ➖ | ➖ | ➖ |
| 26 | response_retrieval | ➖ | ➖ | ➖ |
| 27 | normalization | ✅ | ✅ | ✅ |
| 28 | regex_constraints | ⚠️ | ⚠️ | ✅ |
| 29 | grammar_constraints | ⚠️ | ⚠️ | ⚠️ |
| 30 | json_schema_constraints | ✅ | ✅ | ✅ |

✅ = passed · ❌ = failed · ⚠️ = unsupported · ➖ = n/a

---

## openai-gpt54nano

### Chat Completions

| # | Capability | Result | Details |
|---|-----------|--------|---------|
| 1 | [text_input](#openai-gpt54nano-text-input) | ✅ passed | Text input accepted and processed |
| 2 | [text_output](#openai-gpt54nano-text-output) | ✅ passed | Response contains text content |
| 3 | [json_output](#openai-gpt54nano-json-output) | ✅ passed | Response is valid JSON |
| 4 | [structured_output](#openai-gpt54nano-structured-output) | ✅ passed | Output conforms to JSON schema |
| 5 | [tool_calling](#openai-gpt54nano-tool-calling) | ✅ passed | Tool call returned: get_weather |
| 6 | [tool_choice_auto](#openai-gpt54nano-tool-choice-auto) | ✅ passed | tool_choice='auto' accepted |
| 7 | [tool_choice_none](#openai-gpt54nano-tool-choice-none) | ✅ passed | tool_choice='none' correctly suppressed tool calls |
| 8 | [tool_choice_required](#openai-gpt54nano-tool-choice-required) | ✅ passed | tool_choice='required' forced a tool call |
| 9 | [tool_choice_function](#openai-gpt54nano-tool-choice-function) | ✅ passed | tool_choice forced specific function 'get_weather' |
| 10 | [multiple_tool_calls](#openai-gpt54nano-multiple-tool-calls) | ✅ passed | Multiple tool calls returned: 2 |
| 11 | [parallel_tool_calls](#openai-gpt54nano-parallel-tool-calls) | ✅ passed | parallel_tool_calls parameter accepted |
| 12 | [image_input_url](#openai-gpt54nano-image-input-url) | ✅ passed | Image URL accepted and processed |
| 13 | [image_input_base64](#openai-gpt54nano-image-input-base64) | ✅ passed | Base64 image accepted and processed |
| 14 | [image_input_multi](#openai-gpt54nano-image-input-multi) | ✅ passed | Multiple images accepted and processed |
| 15 | [image_output](#openai-gpt54nano-image-output) | ⚠️ unsupported | Model does not support native image output |
| 16 | [file_input_inline](#openai-gpt54nano-file-input-inline) | ➖ not applicable | Not applicable for this schema |
| 17 | [file_input_reference](#openai-gpt54nano-file-input-reference) | ➖ not applicable | Not applicable for this schema |
| 18 | [built_in_tools](#openai-gpt54nano-built-in-tools) | ➖ not applicable | Not applicable for this schema |
| 19 | [streaming](#openai-gpt54nano-streaming) | ✅ passed | Streaming produced 16 chunks |
| 20 | [stop_sequences](#openai-gpt54nano-stop-sequences) | ⚠️ unsupported | Stop sequence check failed: Client error '400 Bad Request' for url 'https://api. |
| 21 | [logprobs](#openai-gpt54nano-logprobs) | ✅ passed | Logprobs returned with token data |
| 22 | [seeded_determinism](#openai-gpt54nano-seeded-determinism) | ✅ passed | Deterministic output with seed=42: '4' |
| 23 | [long_prompt_acceptance](#openai-gpt54nano-long-prompt-acceptance) | ✅ passed | Long prompt (22574 chars) accepted |
| 24 | [previous_response_id](#openai-gpt54nano-previous-response-id) | ➖ not applicable | Not applicable for this schema |
| 25 | [background_mode](#openai-gpt54nano-background-mode) | ➖ not applicable | Not applicable for this schema |
| 26 | [response_retrieval](#openai-gpt54nano-response-retrieval) | ➖ not applicable | Not applicable for this schema |
| 27 | [normalization](#openai-gpt54nano-normalization) | ✅ passed | Response successfully normalized |
| 28 | [regex_constraints](#openai-gpt54nano-regex-constraints) | ⚠️ unsupported | Regex constraints check failed: Client error '400 Bad Request' for url 'https:// |
| 29 | [grammar_constraints](#openai-gpt54nano-grammar-constraints) | ⚠️ unsupported | Grammar constraints check failed: Client error '400 Bad Request' for url 'https: |
| 30 | [json_schema_constraints](#openai-gpt54nano-json-schema-constraints) | ✅ passed | JSON schema constraint enforced correctly |

---

## azure-gpt54nano

### Chat Completions

| # | Capability | Result | Details |
|---|-----------|--------|---------|
| 1 | [text_input](#azure-gpt54nano-text-input) | ✅ passed | Text input accepted and processed |
| 2 | [text_output](#azure-gpt54nano-text-output) | ✅ passed | Response contains text content |
| 3 | [json_output](#azure-gpt54nano-json-output) | ✅ passed | Response is valid JSON |
| 4 | [structured_output](#azure-gpt54nano-structured-output) | ✅ passed | Output conforms to JSON schema |
| 5 | [tool_calling](#azure-gpt54nano-tool-calling) | ✅ passed | Tool call returned: get_weather |
| 6 | [tool_choice_auto](#azure-gpt54nano-tool-choice-auto) | ✅ passed | tool_choice='auto' accepted |
| 7 | [tool_choice_none](#azure-gpt54nano-tool-choice-none) | ✅ passed | tool_choice='none' correctly suppressed tool calls |
| 8 | [tool_choice_required](#azure-gpt54nano-tool-choice-required) | ✅ passed | tool_choice='required' forced a tool call |
| 9 | [tool_choice_function](#azure-gpt54nano-tool-choice-function) | ✅ passed | tool_choice forced specific function 'get_weather' |
| 10 | [multiple_tool_calls](#azure-gpt54nano-multiple-tool-calls) | ✅ passed | Multiple tool calls returned: 2 |
| 11 | [parallel_tool_calls](#azure-gpt54nano-parallel-tool-calls) | ✅ passed | parallel_tool_calls parameter accepted |
| 12 | [image_input_url](#azure-gpt54nano-image-input-url) | ✅ passed | Image URL accepted and processed |
| 13 | [image_input_base64](#azure-gpt54nano-image-input-base64) | ✅ passed | Base64 image accepted and processed |
| 14 | [image_input_multi](#azure-gpt54nano-image-input-multi) | ✅ passed | Multiple images accepted and processed |
| 15 | [image_output](#azure-gpt54nano-image-output) | ⚠️ unsupported | Model does not support native image output |
| 16 | [file_input_inline](#azure-gpt54nano-file-input-inline) | ➖ not applicable | Not applicable for this schema |
| 17 | [file_input_reference](#azure-gpt54nano-file-input-reference) | ➖ not applicable | Not applicable for this schema |
| 18 | [built_in_tools](#azure-gpt54nano-built-in-tools) | ➖ not applicable | Not applicable for this schema |
| 19 | [streaming](#azure-gpt54nano-streaming) | ✅ passed | Streaming produced 17 chunks |
| 20 | [stop_sequences](#azure-gpt54nano-stop-sequences) | ⚠️ unsupported | Stop sequence check failed: Client error '400 Bad Request' for url 'https://<your-resource>... |
| 21 | [logprobs](#azure-gpt54nano-logprobs) | ✅ passed | Logprobs returned with token data |
| 22 | [seeded_determinism](#azure-gpt54nano-seeded-determinism) | ✅ passed | Deterministic output with seed=42: '4' |
| 23 | [long_prompt_acceptance](#azure-gpt54nano-long-prompt-acceptance) | ✅ passed | Long prompt (22574 chars) accepted |
| 24 | [previous_response_id](#azure-gpt54nano-previous-response-id) | ➖ not applicable | Not applicable for this schema |
| 25 | [background_mode](#azure-gpt54nano-background-mode) | ➖ not applicable | Not applicable for this schema |
| 26 | [response_retrieval](#azure-gpt54nano-response-retrieval) | ➖ not applicable | Not applicable for this schema |
| 27 | [normalization](#azure-gpt54nano-normalization) | ✅ passed | Response successfully normalized |
| 28 | [regex_constraints](#azure-gpt54nano-regex-constraints) | ⚠️ unsupported | Regex constraints check failed: Client error '400 Bad Request' for url 'https:// |
| 29 | [grammar_constraints](#azure-gpt54nano-grammar-constraints) | ⚠️ unsupported | Grammar constraints check failed: Client error '400 Bad Request' for url 'https: |
| 30 | [json_schema_constraints](#azure-gpt54nano-json-schema-constraints) | ✅ passed | JSON schema constraint enforced correctly |

---

## azureml-gemma4

### Chat Completions

| # | Capability | Result | Details |
|---|-----------|--------|---------|
| 1 | [text_input](#azureml-gemma4-text-input) | ✅ passed | Text input accepted and processed |
| 2 | [text_output](#azureml-gemma4-text-output) | ✅ passed | Response contains text content |
| 3 | [json_output](#azureml-gemma4-json-output) | ✅ passed | Response is valid JSON |
| 4 | [structured_output](#azureml-gemma4-structured-output) | ✅ passed | Output conforms to JSON schema |
| 5 | [tool_calling](#azureml-gemma4-tool-calling) | ✅ passed | Tool call returned: get_weather |
| 6 | [tool_choice_auto](#azureml-gemma4-tool-choice-auto) | ✅ passed | tool_choice='auto' accepted |
| 7 | [tool_choice_none](#azureml-gemma4-tool-choice-none) | ✅ passed | tool_choice='none' correctly suppressed tool calls |
| 8 | [tool_choice_required](#azureml-gemma4-tool-choice-required) | ✅ passed | tool_choice='required' forced a tool call |
| 9 | [tool_choice_function](#azureml-gemma4-tool-choice-function) | ✅ passed | tool_choice forced specific function 'get_weather' |
| 10 | [multiple_tool_calls](#azureml-gemma4-multiple-tool-calls) | ✅ passed | Multiple tool calls returned: 2 |
| 11 | [parallel_tool_calls](#azureml-gemma4-parallel-tool-calls) | ✅ passed | parallel_tool_calls parameter accepted |
| 12 | [image_input_url](#azureml-gemma4-image-input-url) | ✅ passed | Image URL accepted and processed |
| 13 | [image_input_base64](#azureml-gemma4-image-input-base64) | ✅ passed | Base64 image accepted and processed |
| 14 | [image_input_multi](#azureml-gemma4-image-input-multi) | ✅ passed | Multiple images accepted and processed |
| 15 | [image_output](#azureml-gemma4-image-output) | ⚠️ unsupported | Model does not support native image output |
| 16 | [file_input_inline](#azureml-gemma4-file-input-inline) | ➖ not applicable | Not applicable for this schema |
| 17 | [file_input_reference](#azureml-gemma4-file-input-reference) | ➖ not applicable | Not applicable for this schema |
| 18 | [built_in_tools](#azureml-gemma4-built-in-tools) | ➖ not applicable | Not applicable for this schema |
| 19 | [streaming](#azureml-gemma4-streaming) | ✅ passed | Streaming produced 15 chunks |
| 20 | [stop_sequences](#azureml-gemma4-stop-sequences) | ✅ passed | Stop sequence was respected |
| 21 | [logprobs](#azureml-gemma4-logprobs) | ✅ passed | Logprobs returned with token data |
| 22 | [seeded_determinism](#azureml-gemma4-seeded-determinism) | ✅ passed | Deterministic output with seed=42: '4' |
| 23 | [long_prompt_acceptance](#azureml-gemma4-long-prompt-acceptance) | ✅ passed | Long prompt (22574 chars) accepted |
| 24 | [previous_response_id](#azureml-gemma4-previous-response-id) | ➖ not applicable | Not applicable for this schema |
| 25 | [background_mode](#azureml-gemma4-background-mode) | ➖ not applicable | Not applicable for this schema |
| 26 | [response_retrieval](#azureml-gemma4-response-retrieval) | ➖ not applicable | Not applicable for this schema |
| 27 | [normalization](#azureml-gemma4-normalization) | ✅ passed | Response successfully normalized |
| 28 | [regex_constraints](#azureml-gemma4-regex-constraints) | ✅ passed | Output matches regex: 482-19-6305 |
| 29 | [grammar_constraints](#azureml-gemma4-grammar-constraints) | ⚠️ unsupported | Grammar constraints check failed: Client error '424 Failed Dependency' for url ' |
| 30 | [json_schema_constraints](#azureml-gemma4-json-schema-constraints) | ✅ passed | JSON schema constraint enforced correctly |

---

## Details

Request/response payloads for each check (filtered for readability).

### openai-gpt54nano

#### <a id="openai-gpt54nano-text-input"></a>✅ text_input

> Text input accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJGHRP6EaET83DClFZXocA7pTQZ",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! \ud83d\udc4b How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-text-output"></a>✅ text_output

> Response contains text content

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJIZVZ3RYx3mk9Uj15hnW85ALWh",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! \ud83d\udc4b How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-json-output"></a>✅ json_output

> Response is valid JSON

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Return a JSON object with keys \"name\" and \"age\". Only output JSON."
    }
  ],
  "response_format": {
    "type": "json_object"
  },
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJJ9x3vmZdbc75sYds2OesakGBD",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "{\"name\":\"Unknown\",\"age\":null}"
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-structured-output"></a>✅ structured_output

> Output conforms to JSON schema

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Generate a person with name, age, and city."
    }
  ],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "person",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "age": {
            "type": "integer"
          },
          "city": {
            "type": "string"
          }
        },
        "required": [
          "name",
          "age",
          "city"
        ],
        "additionalProperties": false
      }
    }
  },
  "max_completion_tokens": 150
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJKxTCNS1sh2XwPdoWlB19T8FK8",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "{\"name\":\"Maya Chen\",\"age\":29,\"city\":\"San Francisco\"}"
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-tool-calling"></a>✅ tool_calling

> Tool call returned: get_weather

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in San Francisco?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJLwkZ3nlXbPGI9mhNhM0vYNY0S",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_UPufImMhC6yiCtP8ktnjuOUB",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\":\"San Francisco\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-tool-choice-auto"></a>✅ tool_choice_auto

> tool_choice='auto' accepted

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "tool_choice": "auto",
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJM1uoWMrANeUvKPqS1eSifVQyl",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_bbGaknNa9FPNrK0XmiYI8a58",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\":\"Tokyo\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-tool-choice-none"></a>✅ tool_choice_none

> tool_choice='none' correctly suppressed tool calls

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "tool_choice": "none",
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJN6HEdp2AXIYFHUTucwTlgIACr",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "I can\u2019t access live weather data right now. If you tell me whether you want **current conditions** or a **forecast** (and for what time window), I can help you interpret what you find from a weather site/app, or suggest reliable sources to check for Tokyo."
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-tool-choice-required"></a>✅ tool_choice_required

> tool_choice='required' forced a tool call

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello to me."
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "tool_choice": "required",
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJOc0LOy5jIWWjOcOeLzwivlKPA",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_aQR3uqUx8vjtKonviYGcIdu1",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\":\"Hello\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-tool-choice-function"></a>✅ tool_choice_function

> tool_choice forced specific function 'get_weather'

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello to me."
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "calculate",
        "description": "Perform a math calculation",
        "parameters": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Math expression to evaluate"
            }
          },
          "required": [
            "expression"
          ]
        }
      }
    }
  ],
  "tool_choice": {
    "type": "function",
    "function": {
      "name": "get_weather"
    }
  },
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJPxJVEMfSvk5hrYmYlVfF9kBBR",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_nSUMh6jlKgxsU4obYrtmFL6d",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\":\"Hello\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-multiple-tool-calls"></a>✅ multiple_tool_calls

> Multiple tool calls returned: 2

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo and also calculate 42 * 17?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "calculate",
        "description": "Perform a math calculation",
        "parameters": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Math expression to evaluate"
            }
          },
          "required": [
            "expression"
          ]
        }
      }
    }
  ],
  "max_completion_tokens": 300
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJR1Anskqigw50vXYRMuM3UIef5",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_kZQ6hWvEq6RHm4wRjfgGM0Dn",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\": \"Tokyo\"}"
            }
          },
          {
            "id": "call_xMCDe5z3nXeyMLti3tLukaPr",
            "type": "function",
            "function": {
              "name": "calculate",
              "arguments": "{\"expression\": \"42 * 17\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-parallel-tool-calls"></a>✅ parallel_tool_calls

> parallel_tool_calls parameter accepted

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo and calculate 42 * 17?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "calculate",
        "description": "Perform a math calculation",
        "parameters": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Math expression to evaluate"
            }
          },
          "required": [
            "expression"
          ]
        }
      }
    }
  ],
  "parallel_tool_calls": true,
  "max_completion_tokens": 300
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJTPbq4LX4mro0U6V1Mu64AhM4S",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_U60rhwWtkkkrNSKgbidwM7T7",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\": \"Tokyo\"}"
            }
          },
          {
            "id": "call_LcrismDxJALTD8tRawASjE8s",
            "type": "function",
            "function": {
              "name": "calculate",
              "arguments": "{\"expression\": \"42 * 17\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-image-input-url"></a>✅ image_input_url

> Image URL accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Describe this image briefly."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        }
      ]
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJUW0JHETwl8cSzwH0QYKFWZhGu",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "I can\u2019t see the image you\u2019re referring to. Could you please upload it or resend it here (or describe what it shows)? Once I have it, I\u2019ll provide a brief description."
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-image-input-base64"></a>✅ image_input_base64

> Base64 image accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Describe this image briefly."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        }
      ]
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJVANO6Gu7NukplUPy22PsaKDAI",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "I can\u2019t see the image you\u2019re referring to. Please upload it (or share a link), and I\u2019ll describe it briefly."
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-image-input-multi"></a>✅ image_input_multi

> Multiple images accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Compare these two images briefly."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        }
      ]
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJXZbkHyiiFxiWJg5mUioW9ua7w",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "I can\u2019t compare them because I don\u2019t have the two images in this chat\u2014only a small colored placeholder appears.\n\nPlease upload both images (or paste them here), and tell me what kind of comparison you want (e.g., content similarity, differences in colors/layout, or text/objects)."
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-image-output"></a>⚠️ image_output

> Model does not support native image output

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Generate a simple image of a red circle on a white background."
    }
  ],
  "max_completion_tokens": 500
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJY9BQiYArCyURSY1ETERH7dUwo",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "I can\u2019t directly generate an actual image file in this chat, but here are two simple ways you can create it:\n\n### Option 1: HTML (renders a red circle on white)\n```html\n<!doctype html>\n<html>\n  <body style=\"margin:0; display:flex; align-items:center; justify-content:center; height:100vh; background:white;\">\n    <div style=\"width:200px; height:200px; background:red; border-radius:50%;\"></div>\n  </body>\n</html>\n```\n\n### Option 2: SVG (copy/paste into a file named `circle.svg`)\n```svg\n<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"200\" height=\"200\">\n  <rect width=\"100%\" height=\"100%\" fill=\"white\"/>\n  <circle cx=\"100\" cy=\"100\" r=\"50\" fill=\"red\"/>\n</svg>\n```\n\nIf you tell me the size you want (e.g., 256\u00d7256) and whether the circle should be filled or outlined, I can tailor the SVG accordingly."
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-file-input-inline"></a>➖ file_input_inline

> Not applicable for this schema

---

#### <a id="openai-gpt54nano-file-input-reference"></a>➖ file_input_reference

> Not applicable for this schema

---

#### <a id="openai-gpt54nano-built-in-tools"></a>➖ built_in_tools

> Not applicable for this schema

---

#### <a id="openai-gpt54nano-streaming"></a>✅ streaming

> Streaming produced 16 chunks

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Count from 1 to 5."
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "chunks_count": 16,
  "first_chunk": {
    "id": "chatcmpl-DWlJbLf9V3zwqKOWhSSa86mVggmGq",
    "object": "chat.completion.chunk",
    "created": 1776700747,
    "model": "gpt-5.4-nano-2026-03-17",
    "service_tier": "default",
    "system_fingerprint": null,
    "choices": [
      {
        "index": 0,
        "delta": {
          "role": "assistant",
          "content": "",
          "refusal": null
        },
        "finish_reason": null
      }
    ],
    "obfuscation": ""
  }
}
```
</details>

---

#### <a id="openai-gpt54nano-stop-sequences"></a>⚠️ stop_sequences

> Stop sequence check failed: Client error '400 Bad Request' for url 'https://api.openai.com/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

**Errors:**
- Client error '400 Bad Request' for url 'https://api.openai.com/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Count from 1 to 20. After the number 5, write the word STOPNOW then continue."
    }
  ],
  "stop": [
    "STOPNOW"
  ],
  "max_completion_tokens": 200
}
```
</details>

---

#### <a id="openai-gpt54nano-logprobs"></a>✅ logprobs

> Logprobs returned with token data

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "logprobs": true,
  "top_logprobs": 3,
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJcokDMhNcQO8sFVhl5HgOZyszD",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! \ud83d\udc4b How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-seeded-determinism"></a>✅ seeded_determinism

> Deterministic output with seed=42: '4'

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is 2 + 2? Answer with just the number."
    }
  ],
  "seed": 42,
  "temperature": 0,
  "max_completion_tokens": 10
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "response_1": {
    "id": "chatcmpl-DWlJdXcDU5P2yIayD4YFHHwoTuI6c",
    "object": "chat.completion",
    "created": 1776700749,
    "model": "gpt-5.4-nano-2026-03-17",
    "choices": [
      {
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "4",
          "refusal": null,
          "annotations": []
        },
        "finish_reason": "stop"
      }
    ],
    "usage": {
      "prompt_tokens": 20,
      "completion_tokens": 4,
      "total_tokens": 24,
      "prompt_tokens_details": {
        "cached_tokens": 0,
        "audio_tokens": 0
      },
      "completion_tokens_details": {
        "reasoning_tokens": 0,
        "audio_tokens": 0,
        "accepted_prediction_tokens": 0,
        "rejected_prediction_tokens": 0
      }
    },
    "service_tier": "default",
    "system_fingerprint": null
  },
  "response_2": {
    "id": "chatcmpl-DWlJeZ0ZqawMiTfr8YCRl7tiqBP9Q",
    "object": "chat.completion",
    "created": 1776700750,
    "model": "gpt-5.4-nano-2026-03-17",
    "choices": [
      {
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "4",
          "refusal": null,
          "annotations": []
        },
        "finish_reason": "stop"
      }
    ],
    "usage": {
      "prompt_tokens": 20,
      "completion_tokens": 4,
      "total_tokens": 24,
      "prompt_tokens_details": {
        "cached_tokens": 0,
        "audio_tokens": 0
      },
      "completion_tokens_details": {
        "reasoning_tokens": 0,
        "audio_tokens": 0,
        "accepted_prediction_tokens": 0,
        "rejected_prediction_tokens": 0
      }
    },
    "service_tier": "default",
    "system_fingerprint": null
  }
}
```
</details>

---

#### <a id="openai-gpt54nano-long-prompt-acceptance"></a>✅ long_prompt_acceptance

> Long prompt (22574 chars) accepted

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "The following is filler text. After reading it, say 'DONE'. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.  Now say DONE."
    }
  ],
  "max_completion_tokens": 20
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJezfZzEiShAAXutSFAG6XpDoDC",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "DONE"
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-previous-response-id"></a>➖ previous_response_id

> Not applicable for this schema

---

#### <a id="openai-gpt54nano-background-mode"></a>➖ background_mode

> Not applicable for this schema

---

#### <a id="openai-gpt54nano-response-retrieval"></a>➖ response_retrieval

> Not applicable for this schema

---

#### <a id="openai-gpt54nano-normalization"></a>✅ normalization

> Response successfully normalized

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJfH5kiJ6RdKmPUB4SjFNJW5O0T",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! \ud83d\udc4b How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

#### <a id="openai-gpt54nano-regex-constraints"></a>⚠️ regex_constraints

> Regex constraints check failed: Client error '400 Bad Request' for url 'https://api.openai.com/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

**Errors:**
- Client error '400 Bad Request' for url 'https://api.openai.com/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Generate a number in the format XXX-XX-XXXX (like 123-45-6789). Output ONLY the number."
    }
  ],
  "response_format": {
    "type": "text",
    "pattern": "^\\d{3}-\\d{2}-\\d{4}$"
  },
  "max_completion_tokens": 50
}
```
</details>

---

#### <a id="openai-gpt54nano-grammar-constraints"></a>⚠️ grammar_constraints

> Grammar constraints check failed: Client error '400 Bad Request' for url 'https://api.openai.com/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

**Errors:**
- Client error '400 Bad Request' for url 'https://api.openai.com/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Is the sky blue? Answer yes or no only."
    }
  ],
  "response_format": {
    "type": "grammar",
    "grammar": "root ::= \"yes\" | \"no\""
  },
  "max_completion_tokens": 10
}
```
</details>

---

#### <a id="openai-gpt54nano-json-schema-constraints"></a>✅ json_schema_constraints

> JSON schema constraint enforced correctly

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Pick a color and provide its hex code."
    }
  ],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "color",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "color": {
            "type": "string",
            "enum": [
              "red",
              "green",
              "blue"
            ]
          },
          "hex": {
            "type": "string"
          }
        },
        "required": [
          "color",
          "hex"
        ],
        "additionalProperties": false
      }
    }
  },
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-DWlJgkYKpuEzMMPN58jOObZWbTzrb",
  "model": "gpt-5.4-nano-2026-03-17",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "{\"color\":\"blue\",\"hex\":\"#1E5EFF\"}"
      },
      "finish_reason": "stop"
    }
  ]
}
```
</details>

---

### azure-gpt54nano

#### <a id="azure-gpt54nano-text-input"></a>✅ text_input

> Text input accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "Hello! \ud83d\udc4b How can I help you today?",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlJhxCXfHVso4jGJpvtl5i5PCPuA",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-text-output"></a>✅ text_output

> Response contains text content

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "Hello! \ud83d\udc4b How can I help you today?",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlJjTg4lLXCutfTBAIM0SawnWj4t",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-json-output"></a>✅ json_output

> Response is valid JSON

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Return a JSON object with keys \"name\" and \"age\". Only output JSON."
    }
  ],
  "response_format": {
    "type": "json_object"
  },
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "{\"name\":\"John Doe\",\"age\":30}",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlJkB95d2crTHsOVLMd9LqcBheDQ",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-structured-output"></a>✅ structured_output

> Output conforms to JSON schema

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Generate a person with name, age, and city."
    }
  ],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "person",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "age": {
            "type": "integer"
          },
          "city": {
            "type": "string"
          }
        },
        "required": [
          "name",
          "age",
          "city"
        ],
        "additionalProperties": false
      }
    }
  },
  "max_completion_tokens": 150
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "{\"name\":\"Ava Thompson\",\"age\":29,\"city\":\"Chicago\"}",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlJlblDf6ngr8sX3qtEykqC2g73t",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-tool-calling"></a>✅ tool_calling

> Tool call returned: get_weather

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in San Francisco?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "tool_calls",
      "message": {
        "content": null,
        "role": "assistant",
        "tool_calls": [
          {
            "function": {
              "arguments": "{\"location\":\"San Francisco\"}",
              "name": "get_weather"
            },
            "id": "call_0EhuVZcs6dmzfeK4I1ZPdQwH",
            "type": "function"
          }
        ]
      }
    }
  ],
  "id": "chatcmpl-DWlJmKqkvFA9nRJjyM2y257ew4Kcn",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-tool-choice-auto"></a>✅ tool_choice_auto

> tool_choice='auto' accepted

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "tool_choice": "auto",
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "tool_calls",
      "message": {
        "content": null,
        "role": "assistant",
        "tool_calls": [
          {
            "function": {
              "arguments": "{\"location\":\"Tokyo\"}",
              "name": "get_weather"
            },
            "id": "call_3QWVK7JBvbM4Yn9OIk5Qq3zt",
            "type": "function"
          }
        ]
      }
    }
  ],
  "id": "chatcmpl-DWlJotXJds8HJL9LUeHdvjho3CLWF",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-tool-choice-none"></a>✅ tool_choice_none

> tool_choice='none' correctly suppressed tool calls

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "tool_choice": "none",
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "I can\u2019t access live weather data right now.  \n\nIf you tell me where in Tokyo you are (or your nearest station/neighborhood) and whether you want \u201cright now,\u201d \u201ctoday,\u201d or a forecast for the next few days, I can help you interpret what to expect based on typical seasonal patterns\u2014or you can share a weather screenshot/link and I\u2019ll summarize it.",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlJpwXnpJMtvQPtFQIgfO06CKLdF",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-tool-choice-required"></a>✅ tool_choice_required

> tool_choice='required' forced a tool call

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello to me."
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "tool_choice": "required",
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "tool_calls",
      "message": {
        "content": null,
        "role": "assistant",
        "tool_calls": [
          {
            "function": {
              "arguments": "{\"location\":\"Hello\"}",
              "name": "get_weather"
            },
            "id": "call_RXaBWX40FsI2jhtIcZi0dxzu",
            "type": "function"
          }
        ]
      }
    }
  ],
  "id": "chatcmpl-DWlJrYEW5NOkbUYqxnnqMq6OwSSSh",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-tool-choice-function"></a>✅ tool_choice_function

> tool_choice forced specific function 'get_weather'

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello to me."
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "calculate",
        "description": "Perform a math calculation",
        "parameters": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Math expression to evaluate"
            }
          },
          "required": [
            "expression"
          ]
        }
      }
    }
  ],
  "tool_choice": {
    "type": "function",
    "function": {
      "name": "get_weather"
    }
  },
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "tool_calls",
      "message": {
        "content": null,
        "role": "assistant",
        "tool_calls": [
          {
            "function": {
              "arguments": "{\"location\":\"Hello City\"}",
              "name": "get_weather"
            },
            "id": "call_6hyZ89DdkpUIfEBnbstfS4bh",
            "type": "function"
          }
        ]
      }
    }
  ],
  "id": "chatcmpl-DWlJsHp3L4iP99AClZTLSMcvhc5Qc",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-multiple-tool-calls"></a>✅ multiple_tool_calls

> Multiple tool calls returned: 2

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo and also calculate 42 * 17?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "calculate",
        "description": "Perform a math calculation",
        "parameters": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Math expression to evaluate"
            }
          },
          "required": [
            "expression"
          ]
        }
      }
    }
  ],
  "max_completion_tokens": 300
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "tool_calls",
      "message": {
        "content": null,
        "role": "assistant",
        "tool_calls": [
          {
            "function": {
              "arguments": "{\"location\": \"Tokyo\"}",
              "name": "get_weather"
            },
            "id": "call_tba6MzBHKuKr5hzFtFDcXiEd",
            "type": "function"
          },
          {
            "function": {
              "arguments": "{\"expression\": \"42 * 17\"}",
              "name": "calculate"
            },
            "id": "call_70Ru2lNoqvhAerbzn1VKnpbB",
            "type": "function"
          }
        ]
      }
    }
  ],
  "id": "chatcmpl-DWlJtU0AGkgEPeabim5noO7AdaKS6",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-parallel-tool-calls"></a>✅ parallel_tool_calls

> parallel_tool_calls parameter accepted

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo and calculate 42 * 17?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "calculate",
        "description": "Perform a math calculation",
        "parameters": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Math expression to evaluate"
            }
          },
          "required": [
            "expression"
          ]
        }
      }
    }
  ],
  "parallel_tool_calls": true,
  "max_completion_tokens": 300
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "tool_calls",
      "message": {
        "content": null,
        "role": "assistant",
        "tool_calls": [
          {
            "function": {
              "arguments": "{\"location\": \"Tokyo\"}",
              "name": "get_weather"
            },
            "id": "call_r0yLfb4yOGxoMwTaryp72n8K",
            "type": "function"
          },
          {
            "function": {
              "arguments": "{\"expression\": \"42 * 17\"}",
              "name": "calculate"
            },
            "id": "call_nx6RD2z9SGbkQv04XCybVIvy",
            "type": "function"
          }
        ]
      }
    }
  ],
  "id": "chatcmpl-DWlJvghTXrOSatWDnCbT9fPG77XPn",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-image-input-url"></a>✅ image_input_url

> Image URL accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Describe this image briefly."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        }
      ]
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "I can\u2019t see the image you\u2019re referring to. Please upload it (or paste it here), and I\u2019ll describe it briefly.",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlJxwNRBVJ8GHYrXWzYJNhiLDhfO",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-image-input-base64"></a>✅ image_input_base64

> Base64 image accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Describe this image briefly."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        }
      ]
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "I can\u2019t see the image you\u2019re referring to. Please upload it (or paste a link), and I\u2019ll describe it briefly.",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlJyJ33sBKIcgbrFuU2cNZ3soGLU",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-image-input-multi"></a>✅ image_input_multi

> Multiple images accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Compare these two images briefly."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        }
      ]
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "I can\u2019t compare them yet because I don\u2019t have the two images\u2014only a small placeholder thumbnail appears.\n\nPlease upload both images (or paste them) and I\u2019ll briefly compare them (similarities and differences).",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlJz2yC4LMjTYwnPyaHCA4vyic9h",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-image-output"></a>⚠️ image_output

> Model does not support native image output

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Generate a simple image of a red circle on a white background."
    }
  ],
  "max_completion_tokens": 500
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "I can\u2019t directly generate an actual image file in this chat, but here\u2019s a simple SVG you can copy into a file (e.g., `red-circle.svg`) and open in any browser:\n\n```svg\n<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"200\" height=\"200\" viewBox=\"0 0 200 200\">\n  <rect width=\"100%\" height=\"100%\" fill=\"white\"/>\n  <circle cx=\"100\" cy=\"100\" r=\"50\" fill=\"red\"/>\n</svg>\n```",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlK06Bc0xMkzFw61CMp0PCAxuq0c",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-file-input-inline"></a>➖ file_input_inline

> Not applicable for this schema

---

#### <a id="azure-gpt54nano-file-input-reference"></a>➖ file_input_reference

> Not applicable for this schema

---

#### <a id="azure-gpt54nano-built-in-tools"></a>➖ built_in_tools

> Not applicable for this schema

---

#### <a id="azure-gpt54nano-streaming"></a>✅ streaming

> Streaming produced 17 chunks

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Count from 1 to 5."
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "chunks_count": 17,
  "first_chunk": {
    "choices": [],
    "created": 0,
    "id": "",
    "model": "",
    "object": "",
    "prompt_filter_results": [
      {
        "prompt_index": 0,
        "content_filter_results": {
          "hate": {
            "filtered": false,
            "severity": "safe"
          },
          "indirect_attack": {
            "detected": false,
            "filtered": false
          },
          "jailbreak": {
            "detected": false,
            "filtered": false
          },
          "self_harm": {
            "filtered": false,
            "severity": "safe"
          },
          "sexual": {
            "filtered": false,
            "severity": "safe"
          },
          "violence": {
            "filtered": false,
            "severity": "safe"
          }
        }
      }
    ]
  }
}
```
</details>

---

#### <a id="azure-gpt54nano-stop-sequences"></a>⚠️ stop_sequences

> Stop sequence check failed: Client error '400 Bad Request' for url 'https://<your-resource>.openai.azure.com/openai/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

**Errors:**
- Client error '400 Bad Request' for url 'https://<your-resource>.openai.azure.com/openai/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Count from 1 to 20. After the number 5, write the word STOPNOW then continue."
    }
  ],
  "stop": [
    "STOPNOW"
  ],
  "max_completion_tokens": 200
}
```
</details>

---

#### <a id="azure-gpt54nano-logprobs"></a>✅ logprobs

> Logprobs returned with token data

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "logprobs": true,
  "top_logprobs": 3,
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "Hello! \ud83d\udc4b How can I help you today?",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlK3THnDS7WeDL4TOiyLk7MMhJ2M",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-seeded-determinism"></a>✅ seeded_determinism

> Deterministic output with seed=42: '4'

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "What is 2 + 2? Answer with just the number."
    }
  ],
  "seed": 42,
  "temperature": 0,
  "max_completion_tokens": 10
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "response_1": {
    "choices": [
      {
        "content_filter_results": {
          "hate": {
            "filtered": false,
            "severity": "safe"
          },
          "protected_material_code": {
            "detected": false,
            "filtered": false
          },
          "protected_material_text": {
            "detected": false,
            "filtered": false
          },
          "self_harm": {
            "filtered": false,
            "severity": "safe"
          },
          "sexual": {
            "filtered": false,
            "severity": "safe"
          },
          "violence": {
            "filtered": false,
            "severity": "safe"
          }
        },
        "finish_reason": "stop",
        "index": 0,
        "logprobs": null,
        "message": {
          "annotations": [],
          "content": "4",
          "refusal": null,
          "role": "assistant"
        }
      }
    ],
    "created": 1776700776,
    "id": "chatcmpl-DWlK42qdA506tOfWA23svRHizFDcS",
    "model": "gpt-5.4-nano-2026-03-17",
    "object": "chat.completion",
    "prompt_filter_results": [
      {
        "prompt_index": 0,
        "content_filter_results": {
          "hate": {
            "filtered": false,
            "severity": "safe"
          },
          "indirect_attack": {
            "detected": false,
            "filtered": false
          },
          "jailbreak": {
            "detected": false,
            "filtered": false
          },
          "self_harm": {
            "filtered": false,
            "severity": "safe"
          },
          "sexual": {
            "filtered": false,
            "severity": "safe"
          },
          "violence": {
            "filtered": false,
            "severity": "safe"
          }
        }
      }
    ],
    "service_tier": "default",
    "system_fingerprint": null,
    "usage": {
      "completion_tokens": 5,
      "completion_tokens_details": {
        "accepted_prediction_tokens": 0,
        "audio_tokens": 0,
        "reasoning_tokens": 0,
        "rejected_prediction_tokens": 0
      },
      "prompt_tokens": 20,
      "prompt_tokens_details": {
        "audio_tokens": 0,
        "cached_tokens": 0
      },
      "total_tokens": 25
    }
  },
  "response_2": {
    "choices": [
      {
        "content_filter_results": {
          "hate": {
            "filtered": false,
            "severity": "safe"
          },
          "protected_material_code": {
            "detected": false,
            "filtered": false
          },
          "protected_material_text": {
            "detected": false,
            "filtered": false
          },
          "self_harm": {
            "filtered": false,
            "severity": "safe"
          },
          "sexual": {
            "filtered": false,
            "severity": "safe"
          },
          "violence": {
            "filtered": false,
            "severity": "safe"
          }
        },
        "finish_reason": "stop",
        "index": 0,
        "logprobs": null,
        "message": {
          "annotations": [],
          "content": "4",
          "refusal": null,
          "role": "assistant"
        }
      }
    ],
    "created": 1776700777,
    "id": "chatcmpl-DWlK5daOFFTSZoN3TbYC34d0Uvpsa",
    "model": "gpt-5.4-nano-2026-03-17",
    "object": "chat.completion",
    "prompt_filter_results": [
      {
        "prompt_index": 0,
        "content_filter_results": {
          "hate": {
            "filtered": false,
            "severity": "safe"
          },
          "indirect_attack": {
            "detected": false,
            "filtered": false
          },
          "jailbreak": {
            "detected": false,
            "filtered": false
          },
          "self_harm": {
            "filtered": false,
            "severity": "safe"
          },
          "sexual": {
            "filtered": false,
            "severity": "safe"
          },
          "violence": {
            "filtered": false,
            "severity": "safe"
          }
        }
      }
    ],
    "service_tier": "default",
    "system_fingerprint": null,
    "usage": {
      "completion_tokens": 5,
      "completion_tokens_details": {
        "accepted_prediction_tokens": 0,
        "audio_tokens": 0,
        "reasoning_tokens": 0,
        "rejected_prediction_tokens": 0
      },
      "prompt_tokens": 20,
      "prompt_tokens_details": {
        "audio_tokens": 0,
        "cached_tokens": 0
      },
      "total_tokens": 25
    }
  }
}
```
</details>

---

#### <a id="azure-gpt54nano-long-prompt-acceptance"></a>✅ long_prompt_acceptance

> Long prompt (22574 chars) accepted

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "The following is filler text. After reading it, say 'DONE'. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.  Now say DONE."
    }
  ],
  "max_completion_tokens": 20
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "DONE",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlK6HX1thwAiddCG0KCSd9uNHKrY",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-previous-response-id"></a>➖ previous_response_id

> Not applicable for this schema

---

#### <a id="azure-gpt54nano-background-mode"></a>➖ background_mode

> Not applicable for this schema

---

#### <a id="azure-gpt54nano-response-retrieval"></a>➖ response_retrieval

> Not applicable for this schema

---

#### <a id="azure-gpt54nano-normalization"></a>✅ normalization

> Response successfully normalized

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "Hello! \ud83d\udc4b How can I help you today?",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlK7IfoixJJ3pYPyicNTaDUXhMMm",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

#### <a id="azure-gpt54nano-regex-constraints"></a>⚠️ regex_constraints

> Regex constraints check failed: Client error '400 Bad Request' for url 'https://<your-resource>.openai.azure.com/openai/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

**Errors:**
- Client error '400 Bad Request' for url 'https://<your-resource>.openai.azure.com/openai/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Generate a number in the format XXX-XX-XXXX (like 123-45-6789). Output ONLY the number."
    }
  ],
  "response_format": {
    "type": "text",
    "pattern": "^\\d{3}-\\d{2}-\\d{4}$"
  },
  "max_completion_tokens": 50
}
```
</details>

---

#### <a id="azure-gpt54nano-grammar-constraints"></a>⚠️ grammar_constraints

> Grammar constraints check failed: Client error '400 Bad Request' for url 'https://<your-resource>.openai.azure.com/openai/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

**Errors:**
- Client error '400 Bad Request' for url 'https://<your-resource>.openai.azure.com/openai/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Is the sky blue? Answer yes or no only."
    }
  ],
  "response_format": {
    "type": "grammar",
    "grammar": "root ::= \"yes\" | \"no\""
  },
  "max_completion_tokens": 10
}
```
</details>

---

#### <a id="azure-gpt54nano-json-schema-constraints"></a>✅ json_schema_constraints

> JSON schema constraint enforced correctly

<details>
<summary>Request</summary>

```json
{
  "model": "gpt-5.4-nano",
  "messages": [
    {
      "role": "user",
      "content": "Pick a color and provide its hex code."
    }
  ],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "color",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "color": {
            "type": "string",
            "enum": [
              "red",
              "green",
              "blue"
            ]
          },
          "hex": {
            "type": "string"
          }
        },
        "required": [
          "color",
          "hex"
        ],
        "additionalProperties": false
      }
    }
  },
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "message": {
        "content": "{\"color\":\"blue\",\"hex\":\"#0000FF\"}",
        "role": "assistant"
      }
    }
  ],
  "id": "chatcmpl-DWlK9NoZtV1oNl5hjEpqFFNBSagcb",
  "model": "gpt-5.4-nano-2026-03-17"
}
```
</details>

---

### azureml-gemma4

#### <a id="azureml-gemma4-text-input"></a>✅ text_input

> Text input accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-ad0dbfa8-723e-4fec-80e2-ef1100d8a31c",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello!",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": 106,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-text-output"></a>✅ text_output

> Response contains text content

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-116f5a71-f1f9-44db-b4d7-7809b9d009d2",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello!",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": 106,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-json-output"></a>✅ json_output

> Response is valid JSON

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Return a JSON object with keys \"name\" and \"age\". Only output JSON."
    }
  ],
  "response_format": {
    "type": "json_object"
  },
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-f8cd74a4-85c0-4bcd-bc6f-0df9d4654307",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "{\n  \"name\": \"John Doe\",\n  \"age\": 30\n}",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": null,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-structured-output"></a>✅ structured_output

> Output conforms to JSON schema

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Generate a person with name, age, and city."
    }
  ],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "person",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "age": {
            "type": "integer"
          },
          "city": {
            "type": "string"
          }
        },
        "required": [
          "name",
          "age",
          "city"
        ],
        "additionalProperties": false
      }
    }
  },
  "max_completion_tokens": 150
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-c30dc7f2-a628-48eb-84e1-d8ce1cc81a2c",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "{\n  \"name\": \"Elena Rodriguez\",\n  \"age\": 32,\n  \"city\": \"Barcelona\"\n}",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": null,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-tool-calling"></a>✅ tool_calling

> Tool call returned: get_weather

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in San Francisco?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-394f5a65-bcd7-493e-ac30-d00737f57527",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "audio": null,
        "function_call": null,
        "tool_calls": [
          {
            "id": "chatcmpl-tool-958332f6eea89af9",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\": \"San Francisco\"}"
            }
          }
        ],
        "reasoning": null
      },
      "finish_reason": "tool_calls",
      "stop_reason": 50,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-tool-choice-auto"></a>✅ tool_choice_auto

> tool_choice='auto' accepted

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "tool_choice": "auto",
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-4a1accd3-db78-4e8b-adeb-96c6e02183e9",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "audio": null,
        "function_call": null,
        "tool_calls": [
          {
            "id": "chatcmpl-tool-bc270eff3923a6bc",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\": \"Tokyo\"}"
            }
          }
        ],
        "reasoning": null
      },
      "finish_reason": "tool_calls",
      "stop_reason": 50,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-tool-choice-none"></a>✅ tool_choice_none

> tool_choice='none' correctly suppressed tool calls

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "tool_choice": "none",
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-a6736e99-c90d-4308-9d4c-230a5b2c8cd2",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "call:get_weather{location:Tokyo}",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": 50,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-tool-choice-required"></a>✅ tool_choice_required

> tool_choice='required' forced a tool call

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Say hello to me."
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "tool_choice": "required",
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-8ef56a51-a271-43c3-8fd8-6d2094626830",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "",
        "audio": null,
        "function_call": null,
        "tool_calls": [
          {
            "id": "chatcmpl-tool-9505fc68f95614e9",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\": \"New York\"}"
            }
          }
        ],
        "reasoning": null
      },
      "finish_reason": "tool_calls",
      "stop_reason": null,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-tool-choice-function"></a>✅ tool_choice_function

> tool_choice forced specific function 'get_weather'

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Say hello to me."
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "calculate",
        "description": "Perform a math calculation",
        "parameters": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Math expression to evaluate"
            }
          },
          "required": [
            "expression"
          ]
        }
      }
    }
  ],
  "tool_choice": {
    "type": "function",
    "function": {
      "name": "get_weather"
    }
  },
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-5d65a9ed-e18d-43d5-b8e0-3df8b93f3d08",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "",
        "audio": null,
        "function_call": null,
        "tool_calls": [
          {
            "id": "chatcmpl-tool-b173695c2d83ed0b",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\n  \"location\": \"Hello!\"\n}"
            }
          }
        ],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": null,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-multiple-tool-calls"></a>✅ multiple_tool_calls

> Multiple tool calls returned: 2

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo and also calculate 42 * 17?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "calculate",
        "description": "Perform a math calculation",
        "parameters": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Math expression to evaluate"
            }
          },
          "required": [
            "expression"
          ]
        }
      }
    }
  ],
  "max_completion_tokens": 300
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-f10320de-d430-4b4f-91d0-f4ca4328b3a6",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "audio": null,
        "function_call": null,
        "tool_calls": [
          {
            "id": "chatcmpl-tool-8b6dfd0425ba5341",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\": \"Tokyo\"}"
            }
          },
          {
            "id": "chatcmpl-tool-893ddf6e9f3aea18",
            "type": "function",
            "function": {
              "name": "calculate",
              "arguments": "{\"expression\": \"42 * 17\"}"
            }
          }
        ],
        "reasoning": null
      },
      "finish_reason": "tool_calls",
      "stop_reason": 50,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-parallel-tool-calls"></a>✅ parallel_tool_calls

> parallel_tool_calls parameter accepted

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather in Tokyo and calculate 42 * 17?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "calculate",
        "description": "Perform a math calculation",
        "parameters": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Math expression to evaluate"
            }
          },
          "required": [
            "expression"
          ]
        }
      }
    }
  ],
  "parallel_tool_calls": true,
  "max_completion_tokens": 300
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-5dc5f8c5-78ff-4a8e-a084-c37240fe56fe",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "audio": null,
        "function_call": null,
        "tool_calls": [
          {
            "id": "chatcmpl-tool-a71781774cd76a28",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\": \"Tokyo\"}"
            }
          },
          {
            "id": "chatcmpl-tool-a1e9bab9312a2a93",
            "type": "function",
            "function": {
              "name": "calculate",
              "arguments": "{\"expression\": \"42 * 17\"}"
            }
          }
        ],
        "reasoning": null
      },
      "finish_reason": "tool_calls",
      "stop_reason": 50,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-image-input-url"></a>✅ image_input_url

> Image URL accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Describe this image briefly."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        }
      ]
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-4be9f736-5c39-4ef5-91a6-b316dbcb16a5",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "A solid red square.",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": 106,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-image-input-base64"></a>✅ image_input_base64

> Base64 image accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Describe this image briefly."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        }
      ]
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-b25e771c-8439-483f-9935-c51956d6a3ce",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "A solid, bright red square.",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": 106,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-image-input-multi"></a>✅ image_input_multi

> Multiple images accepted and processed

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Compare these two images briefly."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAEklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
          }
        }
      ]
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-2b5c63fc-dae0-458c-858f-7b848676f077",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "These two images are identical; both are solid red squares.",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": 106,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-image-output"></a>⚠️ image_output

> Model does not support native image output

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Generate a simple image of a red circle on a white background."
    }
  ],
  "max_completion_tokens": 500
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-6f0a7238-e921-4d93-a67c-34d4fece4844",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "{\n  \"action\": \"dalle.text2im\",\n  \"action_input\": \"{ \\\"prompt\\\": \\\"A simple, solid red circle perfectly centered on a plain, solid white background. Minimalist, high contrast, flat design.\\\" }\",\n  \"thought\": \"The user wants a very simple image of a red circle on a white background. I will generate a prompt that specifies a solid red circle, a plain white background, and a minimalist, flat design to ensure there are no shadows, gradients, or complex elements.\"\n}",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": 106,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-file-input-inline"></a>➖ file_input_inline

> Not applicable for this schema

---

#### <a id="azureml-gemma4-file-input-reference"></a>➖ file_input_reference

> Not applicable for this schema

---

#### <a id="azureml-gemma4-built-in-tools"></a>➖ built_in_tools

> Not applicable for this schema

---

#### <a id="azureml-gemma4-streaming"></a>✅ streaming

> Streaming produced 15 chunks

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Count from 1 to 5."
    }
  ],
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "chunks_count": 15,
  "first_chunk": {
    "id": "chatcmpl-2eca918d-4165-4a22-bd8f-b0262d2c8907",
    "object": "chat.completion.chunk",
    "created": 1776700788,
    "model": "model",
    "choices": [
      {
        "index": 0,
        "delta": {
          "role": "assistant",
          "content": ""
        },
        "logprobs": null,
        "finish_reason": null
      }
    ],
    "prompt_token_ids": null
  }
}
```
</details>

---

#### <a id="azureml-gemma4-stop-sequences"></a>✅ stop_sequences

> Stop sequence was respected

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Count from 1 to 20. After the number 5, write the word STOPNOW then continue."
    }
  ],
  "stop": [
    "STOPNOW"
  ],
  "max_completion_tokens": 200
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-e1236ee2-292f-4e8f-a6ee-b2f758228735",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "1\n2\n3\n4\n5\n",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": "STOPNOW",
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-logprobs"></a>✅ logprobs

> Logprobs returned with token data

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "logprobs": true,
  "top_logprobs": 3,
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-e2fc0a90-7d9d-4e3c-bbd1-43282a74ddd7",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello!",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": 106,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-seeded-determinism"></a>✅ seeded_determinism

> Deterministic output with seed=42: '4'

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "What is 2 + 2? Answer with just the number."
    }
  ],
  "seed": 42,
  "temperature": 0,
  "max_completion_tokens": 10
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "response_1": {
    "id": "chatcmpl-306063c4-902b-4773-8e19-52416676865e",
    "object": "chat.completion",
    "created": 1776700789,
    "model": "model",
    "choices": [
      {
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "4",
          "refusal": null,
          "annotations": null,
          "audio": null,
          "function_call": null,
          "tool_calls": [],
          "reasoning": null
        },
        "logprobs": null,
        "finish_reason": "stop",
        "stop_reason": 106,
        "token_ids": null
      }
    ],
    "service_tier": null,
    "system_fingerprint": null,
    "usage": {
      "prompt_tokens": 27,
      "total_tokens": 29,
      "completion_tokens": 2,
      "prompt_tokens_details": null
    },
    "prompt_logprobs": null,
    "prompt_token_ids": null,
    "kv_transfer_params": null
  },
  "response_2": {
    "id": "chatcmpl-379b88da-67d3-436d-9be9-b307dc58927b",
    "object": "chat.completion",
    "created": 1776700789,
    "model": "model",
    "choices": [
      {
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "4",
          "refusal": null,
          "annotations": null,
          "audio": null,
          "function_call": null,
          "tool_calls": [],
          "reasoning": null
        },
        "logprobs": null,
        "finish_reason": "stop",
        "stop_reason": 106,
        "token_ids": null
      }
    ],
    "service_tier": null,
    "system_fingerprint": null,
    "usage": {
      "prompt_tokens": 27,
      "total_tokens": 29,
      "completion_tokens": 2,
      "prompt_tokens_details": null
    },
    "prompt_logprobs": null,
    "prompt_token_ids": null,
    "kv_transfer_params": null
  }
}
```
</details>

---

#### <a id="azureml-gemma4-long-prompt-acceptance"></a>✅ long_prompt_acceptance

> Long prompt (22574 chars) accepted

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "The following is filler text. After reading it, say 'DONE'. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.  Now say DONE."
    }
  ],
  "max_completion_tokens": 20
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-881557cd-af0a-449c-b6da-3c7d4a0ba2f8",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "DONE",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": 106,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-previous-response-id"></a>➖ previous_response_id

> Not applicable for this schema

---

#### <a id="azureml-gemma4-background-mode"></a>➖ background_mode

> Not applicable for this schema

---

#### <a id="azureml-gemma4-response-retrieval"></a>➖ response_retrieval

> Not applicable for this schema

---

#### <a id="azureml-gemma4-normalization"></a>✅ normalization

> Response successfully normalized

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Say hello."
    }
  ],
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-666174e9-5d03-45d9-9e58-c3004ac68a9b",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello!",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": 106,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-regex-constraints"></a>✅ regex_constraints

> Output matches regex: 482-19-6305

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Generate a number in the format XXX-XX-XXXX (like 123-45-6789). Output ONLY the number."
    }
  ],
  "response_format": {
    "type": "text",
    "pattern": "^\\d{3}-\\d{2}-\\d{4}$"
  },
  "max_completion_tokens": 50
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-f3dfe0a4-23a0-41f2-bcb1-340fa618e43c",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "482-19-6305",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": 106,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---

#### <a id="azureml-gemma4-grammar-constraints"></a>⚠️ grammar_constraints

> Grammar constraints check failed: Client error '424 Failed Dependency' for url 'https://<your-endpoint>.inference.ml.azure.com/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/424

**Errors:**
- Client error '424 Failed Dependency' for url 'https://<your-endpoint>.inference.ml.azure.com/v1/chat/completions'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/424

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Is the sky blue? Answer yes or no only."
    }
  ],
  "response_format": {
    "type": "grammar",
    "grammar": "root ::= \"yes\" | \"no\""
  },
  "max_completion_tokens": 10
}
```
</details>

---

#### <a id="azureml-gemma4-json-schema-constraints"></a>✅ json_schema_constraints

> JSON schema constraint enforced correctly

<details>
<summary>Request</summary>

```json
{
  "model": "model",
  "messages": [
    {
      "role": "user",
      "content": "Pick a color and provide its hex code."
    }
  ],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "color",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "color": {
            "type": "string",
            "enum": [
              "red",
              "green",
              "blue"
            ]
          },
          "hex": {
            "type": "string"
          }
        },
        "required": [
          "color",
          "hex"
        ],
        "additionalProperties": false
      }
    }
  },
  "max_completion_tokens": 100
}
```
</details>

<details>
<summary>Response</summary>

```json
{
  "id": "chatcmpl-67df9b6e-e453-4b90-9350-f102a96a68c5",
  "model": "model",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "{\n  \"color\": \"red\",\n  \"hex\": \"#FF0000\"\n}",
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning": null
      },
      "finish_reason": "stop",
      "stop_reason": null,
      "token_ids": null
    }
  ],
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```
</details>

---
