"""Integration tests with mocked HTTP endpoints."""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from llm_api_spec.adapters.chat_completions import ChatCompletionsAdapter
from llm_api_spec.adapters.responses import ResponsesAdapter
from llm_api_spec.checks.basic_text import check_text_input, check_text_output, check_stop_sequences
from llm_api_spec.checks.tool_calling import (
    check_tool_calling,
    check_tool_choice_none,
    check_tool_choice_required,
)
from llm_api_spec.checks.structured_output import check_json_output
from llm_api_spec.checks.normalization import check_normalization
from llm_api_spec.models import EndpointTarget, SchemaType
from tests.conftest import make_chat_response, make_responses_response


@pytest.fixture
def chat_target():
    return EndpointTarget(
        name="mock-chat",
        base_url="https://mock-api.test/v1",
        api_key="test-key",
        model="test-model",
        schemas=[SchemaType.CHAT_COMPLETIONS],
    )


@pytest.fixture
def responses_target():
    return EndpointTarget(
        name="mock-responses",
        base_url="https://mock-api.test/v1",
        api_key="test-key",
        model="test-model",
        schemas=[SchemaType.RESPONSES],
    )


class TestChatCompletionsIntegration:
    @respx.mock
    @pytest.mark.asyncio
    async def test_text_input_success(self, chat_target):
        respx.post("https://mock-api.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=make_chat_response(content="Hi there!"))
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_input(adapter)
            assert result.supported is True
            assert result.passed is True
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_text_input_server_error(self, chat_target):
        respx.post("https://mock-api.test/v1/chat/completions").mock(
            return_value=httpx.Response(500, json={"error": "Internal error"})
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_text_input(adapter)
            assert result.supported is False
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_text_output_empty(self, chat_target):
        respx.post("https://mock-api.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=make_chat_response(content=""))
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
    async def test_tool_calling_success(self, chat_target):
        tool_calls = [
            {
                "id": "tc1",
                "type": "function",
                "function": {"name": "get_weather", "arguments": '{"location":"SF"}'},
            }
        ]
        respx.post("https://mock-api.test/v1/chat/completions").mock(
            return_value=httpx.Response(
                200, json=make_chat_response(content=None, tool_calls=tool_calls)
            )
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_tool_calling(adapter)
            assert result.supported is True
            assert result.passed is True
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_tool_choice_none_respected(self, chat_target):
        respx.post("https://mock-api.test/v1/chat/completions").mock(
            return_value=httpx.Response(
                200, json=make_chat_response(content="No tools called.")
            )
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_tool_choice_none(adapter)
            assert result.supported is True
            assert result.passed is True
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_tool_choice_none_violated(self, chat_target):
        tool_calls = [
            {
                "id": "tc1",
                "type": "function",
                "function": {"name": "get_weather", "arguments": "{}"},
            }
        ]
        respx.post("https://mock-api.test/v1/chat/completions").mock(
            return_value=httpx.Response(
                200, json=make_chat_response(content=None, tool_calls=tool_calls)
            )
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_tool_choice_none(adapter)
            assert result.supported is True
            assert result.passed is False
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_tool_choice_required_success(self, chat_target):
        tool_calls = [
            {
                "id": "tc1",
                "type": "function",
                "function": {"name": "get_weather", "arguments": '{"location":"Tokyo"}'},
            }
        ]
        respx.post("https://mock-api.test/v1/chat/completions").mock(
            return_value=httpx.Response(
                200, json=make_chat_response(content=None, tool_calls=tool_calls)
            )
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_tool_choice_required(adapter)
            assert result.supported is True
            assert result.passed is True
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_json_output_valid(self, chat_target):
        respx.post("https://mock-api.test/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json=make_chat_response(content='{"name":"Alice","age":30}'),
            )
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_json_output(adapter)
            assert result.supported is True
            assert result.passed is True
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_json_output_invalid(self, chat_target):
        respx.post("https://mock-api.test/v1/chat/completions").mock(
            return_value=httpx.Response(
                200, json=make_chat_response(content="not json {broken")
            )
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_json_output(adapter)
            assert result.supported is True
            assert result.passed is False
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_normalization_success(self, chat_target):
        respx.post("https://mock-api.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=make_chat_response(content="Normalized"))
        )
        adapter = ChatCompletionsAdapter(chat_target)
        try:
            result = await check_normalization(adapter)
            assert result.supported is True
            assert result.passed is True
            assert result.normalized is True
        finally:
            await adapter.close()


class TestResponsesIntegration:
    @respx.mock
    @pytest.mark.asyncio
    async def test_text_input_success(self, responses_target):
        respx.post("https://mock-api.test/v1/responses").mock(
            return_value=httpx.Response(200, json=make_responses_response(text="Hi!"))
        )
        adapter = ResponsesAdapter(responses_target)
        try:
            result = await check_text_input(adapter)
            assert result.supported is True
            assert result.passed is True
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_text_output_success(self, responses_target):
        respx.post("https://mock-api.test/v1/responses").mock(
            return_value=httpx.Response(200, json=make_responses_response(text="Hello!"))
        )
        adapter = ResponsesAdapter(responses_target)
        try:
            result = await check_text_output(adapter)
            assert result.supported is True
            assert result.passed is True
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_tool_calling_success(self, responses_target):
        tool_calls = [{"id": "fc1", "name": "get_weather", "arguments": '{"location":"SF"}'}]
        respx.post("https://mock-api.test/v1/responses").mock(
            return_value=httpx.Response(
                200, json=make_responses_response(text="", tool_calls=tool_calls)
            )
        )
        adapter = ResponsesAdapter(responses_target)
        try:
            result = await check_tool_calling(adapter)
            assert result.supported is True
            assert result.passed is True
        finally:
            await adapter.close()
