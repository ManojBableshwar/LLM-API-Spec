"""Unit tests for normalization logic."""

from __future__ import annotations

import pytest

from llm_api_spec.adapters.chat_completions import ChatCompletionsAdapter
from llm_api_spec.adapters.responses import ResponsesAdapter
from llm_api_spec.models import EndpointTarget, SchemaType


@pytest.fixture
def chat_adapter():
    target = EndpointTarget(
        name="test", base_url="https://mock.example.com/v1", model="m"
    )
    return ChatCompletionsAdapter(target)


@pytest.fixture
def responses_adapter():
    target = EndpointTarget(
        name="test",
        base_url="https://mock.example.com/v1",
        model="m",
        schemas=[SchemaType.RESPONSES],
    )
    return ResponsesAdapter(target)


class TestChatCompletionsNormalization:
    def test_text_normalization(self, chat_adapter):
        raw = {
            "id": "1",
            "model": "m",
            "choices": [{"message": {"content": "  Hello  "}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }
        n = chat_adapter.normalize(raw)
        assert n.text == "  Hello  "  # Normalization preserves original text
        assert n.finish_reason == "stop"

    def test_tool_call_normalization(self, chat_adapter):
        raw = {
            "id": "1",
            "model": "m",
            "choices": [
                {
                    "message": {
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "tc1",
                                "type": "function",
                                "function": {
                                    "name": "get_weather",
                                    "arguments": '{"city": "SF"}',
                                },
                            },
                            {
                                "id": "tc2",
                                "type": "function",
                                "function": {
                                    "name": "calculate",
                                    "arguments": '{"expr": "2+2"}',
                                },
                            },
                        ],
                    },
                    "finish_reason": "tool_calls",
                }
            ],
            "usage": None,
        }
        n = chat_adapter.normalize(raw)
        assert n.text is None
        assert len(n.tool_calls) == 2
        assert n.tool_calls[0].id == "tc1"
        assert n.tool_calls[0].name == "get_weather"
        assert n.tool_calls[1].name == "calculate"

    def test_missing_usage(self, chat_adapter):
        raw = {"id": "1", "model": "m", "choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}]}
        n = chat_adapter.normalize(raw)
        assert n.usage is None

    def test_empty_tool_calls(self, chat_adapter):
        raw = {
            "id": "1",
            "model": "m",
            "choices": [{"message": {"content": "hi", "tool_calls": []}, "finish_reason": "stop"}],
        }
        n = chat_adapter.normalize(raw)
        assert n.tool_calls == []


class TestResponsesNormalization:
    def test_text_normalization(self, responses_adapter):
        raw = {
            "id": "r1",
            "model": "m",
            "status": "completed",
            "output": [
                {"type": "message", "content": [{"type": "output_text", "text": "Hello"}]}
            ],
            "usage": {"input_tokens": 5, "output_tokens": 3},
        }
        n = responses_adapter.normalize(raw)
        assert n.text == "Hello"
        assert n.finish_reason == "completed"
        assert n.usage.prompt_tokens == 5
        assert n.usage.completion_tokens == 3
        assert n.usage.total_tokens == 8

    def test_multi_text_parts(self, responses_adapter):
        raw = {
            "id": "r1",
            "model": "m",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "content": [
                        {"type": "output_text", "text": "Part 1"},
                        {"type": "output_text", "text": "Part 2"},
                    ],
                }
            ],
            "usage": None,
        }
        n = responses_adapter.normalize(raw)
        assert n.text == "Part 1\nPart 2"

    def test_tool_call_normalization(self, responses_adapter):
        raw = {
            "id": "r1",
            "model": "m",
            "status": "completed",
            "output": [
                {
                    "type": "function_call",
                    "call_id": "fc1",
                    "name": "search",
                    "arguments": '{"q":"test"}',
                }
            ],
            "usage": None,
        }
        n = responses_adapter.normalize(raw)
        assert len(n.tool_calls) == 1
        assert n.tool_calls[0].id == "fc1"
        assert n.tool_calls[0].name == "search"

    def test_mixed_output(self, responses_adapter):
        raw = {
            "id": "r1",
            "model": "m",
            "status": "completed",
            "output": [
                {"type": "message", "content": [{"type": "output_text", "text": "Here:"}]},
                {"type": "function_call", "call_id": "fc1", "name": "calc", "arguments": "{}"},
            ],
            "usage": None,
        }
        n = responses_adapter.normalize(raw)
        assert n.text == "Here:"
        assert len(n.tool_calls) == 1
