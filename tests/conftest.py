"""Shared test fixtures and mock response factories."""

from __future__ import annotations

from typing import Any

import pytest

from llm_api_spec.models import EndpointTarget, SchemaType


@pytest.fixture
def chat_target() -> EndpointTarget:
    return EndpointTarget(
        name="test-chat",
        base_url="https://mock.example.com/v1",
        api_key="test-key",
        model="test-model",
        schemas=[SchemaType.CHAT_COMPLETIONS],
        timeout=10.0,
    )


@pytest.fixture
def responses_target() -> EndpointTarget:
    return EndpointTarget(
        name="test-responses",
        base_url="https://mock.example.com/v1",
        api_key="test-key",
        model="test-model",
        schemas=[SchemaType.RESPONSES],
        timeout=10.0,
    )


def make_chat_response(
    content: str = "Hello!",
    tool_calls: list[dict] | None = None,
    finish_reason: str = "stop",
    model: str = "test-model",
    response_id: str = "chatcmpl-123",
    logprobs: dict | None = None,
) -> dict[str, Any]:
    """Build a mock Chat Completions response."""
    message: dict[str, Any] = {"role": "assistant", "content": content}
    if tool_calls:
        message["tool_calls"] = tool_calls

    choice: dict[str, Any] = {
        "index": 0,
        "message": message,
        "finish_reason": finish_reason,
    }
    if logprobs is not None:
        choice["logprobs"] = logprobs

    return {
        "id": response_id,
        "object": "chat.completion",
        "model": model,
        "choices": [choice],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15,
        },
    }


def make_responses_response(
    text: str = "Hello!",
    tool_calls: list[dict] | None = None,
    status: str = "completed",
    model: str = "test-model",
    response_id: str = "resp-123",
) -> dict[str, Any]:
    """Build a mock Responses API response."""
    output: list[dict[str, Any]] = []

    if text:
        output.append({
            "type": "message",
            "role": "assistant",
            "content": [{"type": "output_text", "text": text}],
        })

    if tool_calls:
        for tc in tool_calls:
            output.append({
                "type": "function_call",
                "call_id": tc.get("id", "call-1"),
                "name": tc.get("name", ""),
                "arguments": tc.get("arguments", "{}"),
            })

    return {
        "id": response_id,
        "object": "response",
        "model": model,
        "status": status,
        "output": output,
        "usage": {
            "input_tokens": 10,
            "output_tokens": 5,
        },
    }


def make_chat_stream_chunks(content: str = "Hello!") -> list[str]:
    """Build mock SSE stream lines for Chat Completions."""
    lines = []
    for i, char in enumerate(content):
        chunk = {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "model": "test-model",
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": char} if i > 0 else {"role": "assistant", "content": char},
                    "finish_reason": None,
                }
            ],
        }
        import json
        lines.append(f"data: {json.dumps(chunk)}\n\n")

    # Final chunk
    final = {
        "id": "chatcmpl-123",
        "object": "chat.completion.chunk",
        "model": "test-model",
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
    }
    import json
    lines.append(f"data: {json.dumps(final)}\n\n")
    lines.append("data: [DONE]\n\n")
    return lines
