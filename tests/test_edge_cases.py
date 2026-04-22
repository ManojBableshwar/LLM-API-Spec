"""Edge case tests — malformed JSON, partial streaming, corrupt tool calls, invalid schema."""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from llm_api_spec.adapters.chat_completions import ChatCompletionsAdapter
from llm_api_spec.adapters.responses import ResponsesAdapter
from llm_api_spec.checks.basic_text import check_text_input, check_text_output
from llm_api_spec.checks.tool_calling import check_tool_calling
from llm_api_spec.checks.structured_output import check_json_output
from llm_api_spec.checks.normalization import check_normalization
from llm_api_spec.models import EndpointTarget, SchemaType


@pytest.fixture
def chat_target():
    return EndpointTarget(
        name="edge-test",
        base_url="https://mock-edge.test/v1",
        api_key="key",
        model="model",
        timeout=5.0,
    )


@pytest.fixture
def responses_target():
    return EndpointTarget(
        name="edge-test",
        base_url="https://mock-edge.test/v1",
        api_key="key",
        model="model",
        schemas=[SchemaType.RESPONSES],
        timeout=5.0,
    )


class TestMalformedJSON:
    @respx.mock
    @pytest.mark.asyncio
    async def test_non_json_response(self, chat_target):
        """Endpoint returns non-JSON body."""
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, text="not json at all")
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_input(adapter)
            assert result.supported is False
            assert len(result.errors) > 0
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_truncated_json_response(self, chat_target):
        """Endpoint returns truncated JSON."""
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, text='{"id": "1", "choices": [{"mes')
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_input(adapter)
            assert result.supported is False
        finally:
            await adapter.close()


class TestToolCallCorruption:
    @respx.mock
    @pytest.mark.asyncio
    async def test_tool_call_invalid_arguments(self, chat_target):
        """Tool call with malformed arguments JSON."""
        response = {
            "id": "1",
            "object": "chat.completion",
            "model": "model",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "tc1",
                                "type": "function",
                                "function": {
                                    "name": "get_weather",
                                    "arguments": "NOT VALID JSON {{{",
                                },
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                    "index": 0,
                }
            ],
            "usage": {"prompt_tokens": 5, "completion_tokens": 5, "total_tokens": 10},
        }
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response)
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_tool_calling(adapter)
            assert result.supported is True
            assert result.passed is False  # Arguments are not valid JSON
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_tool_call_missing_name(self, chat_target):
        """Tool call with missing function name."""
        response = {
            "id": "1",
            "object": "chat.completion",
            "model": "model",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "tc1",
                                "type": "function",
                                "function": {"name": "", "arguments": "{}"},
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                    "index": 0,
                }
            ],
            "usage": {"prompt_tokens": 5, "completion_tokens": 5, "total_tokens": 10},
        }
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response)
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_tool_calling(adapter)
            assert result.supported is True
            assert result.passed is False  # Empty name
        finally:
            await adapter.close()


class TestInvalidSchemaResponses:
    @respx.mock
    @pytest.mark.asyncio
    async def test_missing_choices_key(self, chat_target):
        """Response completely missing the 'choices' key."""
        response = {
            "id": "1",
            "object": "chat.completion",
            "model": "model",
            "usage": {"prompt_tokens": 5, "completion_tokens": 0, "total_tokens": 5},
        }
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response)
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_output(adapter)
            assert result.supported is True
            assert result.passed is False
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_missing_output_key_responses(self, responses_target):
        """Responses API response missing 'output' key."""
        response = {
            "id": "r1",
            "object": "response",
            "model": "model",
            "status": "completed",
        }
        respx.post("https://mock-edge.test/v1/responses").mock(
            return_value=httpx.Response(200, json=response)
        )
        adapter = ResponsesAdapter(responses_target)
        try:
            result = await check_text_output(adapter)
            assert result.supported is True
            assert result.passed is False
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_empty_message_content(self, chat_target):
        """Response with null content in message."""
        response = {
            "id": "1",
            "object": "chat.completion",
            "model": "model",
            "choices": [
                {
                    "message": {"role": "assistant", "content": None},
                    "finish_reason": "stop",
                    "index": 0,
                }
            ],
            "usage": {"prompt_tokens": 5, "completion_tokens": 0, "total_tokens": 5},
        }
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response)
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_output(adapter)
            assert result.supported is True
            assert result.passed is False
        finally:
            await adapter.close()


class TestHTTPErrors:
    @respx.mock
    @pytest.mark.asyncio
    async def test_401_unauthorized(self, chat_target):
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(401, json={"error": "Unauthorized"})
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_input(adapter)
            assert result.supported is False
            assert len(result.errors) > 0
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_429_rate_limited(self, chat_target):
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(429, json={"error": "Rate limited"})
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_input(adapter)
            assert result.supported is False
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_404_not_found(self, chat_target):
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(404, json={"error": "Not found"})
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_input(adapter)
            assert result.supported is False
        finally:
            await adapter.close()


class TestDeterminismEdgeCases:
    @respx.mock
    @pytest.mark.asyncio
    async def test_normalization_with_unusual_structure(self, chat_target):
        """Response with extra/unexpected fields shouldn't break normalization."""
        response = {
            "id": "1",
            "object": "chat.completion",
            "model": "model",
            "choices": [
                {
                    "message": {"role": "assistant", "content": "ok", "extra_field": True},
                    "finish_reason": "stop",
                    "index": 0,
                }
            ],
            "usage": {"prompt_tokens": 5, "completion_tokens": 1, "total_tokens": 6},
            "system_fingerprint": "fp_abc123",
        }
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response)
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_normalization(adapter)
            assert result.supported is True
            assert result.passed is True
            assert result.normalized is True
        finally:
            await adapter.close()


class TestFailureClassification:
    @respx.mock
    @pytest.mark.asyncio
    async def test_unsupported_classification(self, chat_target):
        """4xx error should classify as unsupported, not failed."""
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(
                400, json={"error": {"message": "Unsupported parameter: logprobs"}}
            )
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_input(adapter)
            assert result.status == "unsupported"
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_passed_classification(self, chat_target):
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "1",
                    "object": "chat.completion",
                    "model": "model",
                    "choices": [
                        {"message": {"role": "assistant", "content": "Hi"}, "finish_reason": "stop", "index": 0}
                    ],
                    "usage": {"prompt_tokens": 5, "completion_tokens": 1, "total_tokens": 6},
                },
            )
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_input(adapter)
            assert result.status == "passed"
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_failed_classification(self, chat_target):
        """Supported but incorrect behavior should be 'failed'."""
        respx.post("https://mock-edge.test/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "1",
                    "object": "chat.completion",
                    "model": "model",
                    "choices": [
                        {"message": {"role": "assistant", "content": ""}, "finish_reason": "stop", "index": 0}
                    ],
                    "usage": {"prompt_tokens": 5, "completion_tokens": 0, "total_tokens": 5},
                },
            )
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_output(adapter)
            assert result.status == "failed"
        finally:
            await adapter.close()
