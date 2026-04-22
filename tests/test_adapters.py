"""Unit tests for schema adapters."""

from __future__ import annotations

import pytest

from llm_api_spec.adapters.chat_completions import ChatCompletionsAdapter
from llm_api_spec.adapters.responses import ResponsesAdapter
from llm_api_spec.models import EndpointTarget, SchemaType

from tests.conftest import make_chat_response, make_responses_response


@pytest.fixture
def chat_adapter():
    target = EndpointTarget(
        name="test", base_url="https://mock.example.com/v1", model="test-model"
    )
    return ChatCompletionsAdapter(target)


@pytest.fixture
def responses_adapter():
    target = EndpointTarget(
        name="test",
        base_url="https://mock.example.com/v1",
        model="test-model",
        schemas=[SchemaType.RESPONSES],
    )
    return ResponsesAdapter(target)


class TestChatCompletionsAdapter:
    def test_endpoint_path(self, chat_adapter):
        assert chat_adapter.endpoint_path() == "/chat/completions"

    def test_schema_type(self, chat_adapter):
        assert chat_adapter.schema_type == SchemaType.CHAT_COMPLETIONS

    def test_build_request_simple(self, chat_adapter):
        body = chat_adapter.build_request(prompt="Hello")
        assert body["model"] == "test-model"
        assert body["messages"] == [{"role": "user", "content": "Hello"}]

    def test_build_request_with_messages(self, chat_adapter):
        msgs = [{"role": "user", "content": "Hi"}]
        body = chat_adapter.build_request(messages=msgs)
        assert body["messages"] == msgs

    def test_build_request_with_tools(self, chat_adapter):
        tools = [{"type": "function", "function": {"name": "test"}}]
        body = chat_adapter.build_request(prompt="Hi", tools=tools, tool_choice="auto")
        assert body["tools"] == tools
        assert body["tool_choice"] == "auto"

    def test_build_request_with_stream(self, chat_adapter):
        body = chat_adapter.build_request(prompt="Hi", stream=True)
        assert body["stream"] is True

    def test_build_request_optional_keys(self, chat_adapter):
        body = chat_adapter.build_request(
            prompt="Hi",
            stop=["END"],
            seed=42,
            logprobs=True,
            top_logprobs=5,
            max_tokens=100,
            temperature=0.5,
        )
        assert body["stop"] == ["END"]
        assert body["seed"] == 42
        assert body["logprobs"] is True
        assert body["max_completion_tokens"] == 100

    def test_parse_response(self, chat_adapter):
        raw = make_chat_response(content="Hello!", finish_reason="stop")
        parsed = chat_adapter.parse_response(raw)
        assert parsed["content"] == "Hello!"
        assert parsed["finish_reason"] == "stop"
        assert parsed["id"] == "chatcmpl-123"

    def test_parse_response_with_tool_calls(self, chat_adapter):
        tool_calls = [
            {
                "id": "tc1",
                "type": "function",
                "function": {"name": "get_weather", "arguments": '{"location":"SF"}'},
            }
        ]
        raw = make_chat_response(content=None, tool_calls=tool_calls)
        parsed = chat_adapter.parse_response(raw)
        assert parsed["tool_calls"] is not None
        assert len(parsed["tool_calls"]) == 1

    def test_parse_empty_choices(self, chat_adapter):
        raw = {"id": "x", "model": "m", "object": "chat.completion", "choices": []}
        parsed = chat_adapter.parse_response(raw)
        assert parsed["content"] is None

    def test_normalize(self, chat_adapter):
        raw = make_chat_response(content="Test output")
        normalized = chat_adapter.normalize(raw)
        assert normalized.text == "Test output"
        assert normalized.finish_reason == "stop"
        assert normalized.model == "test-model"
        assert normalized.response_id == "chatcmpl-123"
        assert normalized.usage is not None
        assert normalized.usage.prompt_tokens == 10
        assert normalized.usage.total_tokens == 15

    def test_normalize_with_tool_calls(self, chat_adapter):
        tool_calls = [
            {
                "id": "tc1",
                "type": "function",
                "function": {"name": "calc", "arguments": '{"x":1}'},
            }
        ]
        raw = make_chat_response(tool_calls=tool_calls)
        normalized = chat_adapter.normalize(raw)
        assert len(normalized.tool_calls) == 1
        assert normalized.tool_calls[0].name == "calc"
        assert normalized.tool_calls[0].arguments == '{"x":1}'

    def test_normalize_empty_response(self, chat_adapter):
        raw = {"id": "x", "model": "m", "choices": [], "usage": None}
        normalized = chat_adapter.normalize(raw)
        assert normalized.text is None
        assert normalized.tool_calls == []
        assert normalized.usage is None


class TestResponsesAdapter:
    def test_endpoint_path(self, responses_adapter):
        assert responses_adapter.endpoint_path() == "/responses"

    def test_schema_type(self, responses_adapter):
        assert responses_adapter.schema_type == SchemaType.RESPONSES

    def test_build_request_simple(self, responses_adapter):
        body = responses_adapter.build_request(prompt="Hello")
        assert body["model"] == "test-model"
        assert body["input"] == "Hello"

    def test_build_request_with_input(self, responses_adapter):
        items = [{"type": "input_text", "text": "Hi"}]
        body = responses_adapter.build_request(input=items)
        assert body["input"] == items

    def test_build_request_optional_keys(self, responses_adapter):
        body = responses_adapter.build_request(
            prompt="Hi",
            previous_response_id="resp-1",
            background=True,
            stop=["END"],
        )
        assert body["previous_response_id"] == "resp-1"
        assert body["background"] is True
        assert body["stop"] == ["END"]

    def test_parse_response(self, responses_adapter):
        raw = make_responses_response(text="Hello!", status="completed")
        parsed = responses_adapter.parse_response(raw)
        assert parsed["content"] == "Hello!"
        assert parsed["status"] == "completed"
        assert parsed["id"] == "resp-123"

    def test_parse_response_with_tool_calls(self, responses_adapter):
        tool_calls = [{"id": "tc1", "name": "get_weather", "arguments": '{"loc":"SF"}'}]
        raw = make_responses_response(text="", tool_calls=tool_calls)
        parsed = responses_adapter.parse_response(raw)
        assert parsed["tool_calls"] is not None

    def test_normalize(self, responses_adapter):
        raw = make_responses_response(text="Test output")
        normalized = responses_adapter.normalize(raw)
        assert normalized.text == "Test output"
        assert normalized.finish_reason == "completed"
        assert normalized.model == "test-model"
        assert normalized.response_id == "resp-123"
        assert normalized.usage is not None
        assert normalized.usage.prompt_tokens == 10
        assert normalized.usage.completion_tokens == 5

    def test_normalize_with_tool_calls(self, responses_adapter):
        tool_calls = [{"id": "tc1", "name": "calc", "arguments": '{"x":1}'}]
        raw = make_responses_response(tool_calls=tool_calls)
        normalized = responses_adapter.normalize(raw)
        assert len(normalized.tool_calls) == 1
        assert normalized.tool_calls[0].name == "calc"

    def test_normalize_empty_output(self, responses_adapter):
        raw = {"id": "x", "model": "m", "status": "completed", "output": [], "usage": None}
        normalized = responses_adapter.normalize(raw)
        assert normalized.text is None
        assert normalized.tool_calls == []
