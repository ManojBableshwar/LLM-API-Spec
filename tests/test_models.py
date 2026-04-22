"""Unit tests for data models."""

from __future__ import annotations

import pytest

from llm_api_spec.models import (
    Capability,
    CapabilityResult,
    EndpointTarget,
    NormalizedResponse,
    NormalizedToolCall,
    NormalizedUsage,
    ReportSummary,
    SchemaType,
    is_applicable,
)


class TestEndpointTarget:
    def test_minimal_target(self):
        target = EndpointTarget(
            name="test",
            base_url="https://api.example.com/v1",
            model="gpt-4o",
        )
        assert target.name == "test"
        assert target.api_key is None
        assert target.timeout == 60.0
        assert target.schemas == [SchemaType.CHAT_COMPLETIONS]

    def test_full_target(self):
        target = EndpointTarget(
            name="full",
            base_url="https://api.example.com/v1",
            api_key="sk-test",
            model="gpt-4o",
            schemas=[SchemaType.CHAT_COMPLETIONS, SchemaType.RESPONSES],
            headers={"X-Custom": "value"},
            timeout=120.0,
        )
        assert len(target.schemas) == 2
        assert target.headers == {"X-Custom": "value"}


class TestCapabilityResult:
    def test_passed_status(self):
        result = CapabilityResult(
            target="test",
            schema=SchemaType.CHAT_COMPLETIONS,
            capability=Capability.TEXT_INPUT,
            supported=True,
            **{"pass": True},
        )
        assert result.status == "passed"

    def test_failed_status(self):
        result = CapabilityResult(
            target="test",
            schema=SchemaType.CHAT_COMPLETIONS,
            capability=Capability.TEXT_INPUT,
            supported=True,
            **{"pass": False},
        )
        assert result.status == "failed"

    def test_unsupported_status(self):
        result = CapabilityResult(
            target="test",
            schema=SchemaType.CHAT_COMPLETIONS,
            capability=Capability.TEXT_INPUT,
            supported=False,
        )
        assert result.status == "unsupported"

    def test_not_applicable_status(self):
        result = CapabilityResult(
            target="test",
            schema=SchemaType.CHAT_COMPLETIONS,
            capability=Capability.TEXT_INPUT,
        )
        assert result.status == "not_applicable"


class TestIsApplicable:
    def test_logprobs_chat_completions(self):
        assert is_applicable(Capability.LOGPROBS, SchemaType.CHAT_COMPLETIONS)

    def test_logprobs_responses(self):
        assert not is_applicable(Capability.LOGPROBS, SchemaType.RESPONSES)

    def test_previous_response_id_responses(self):
        assert is_applicable(Capability.PREVIOUS_RESPONSE_ID, SchemaType.RESPONSES)

    def test_previous_response_id_chat(self):
        assert not is_applicable(Capability.PREVIOUS_RESPONSE_ID, SchemaType.CHAT_COMPLETIONS)

    def test_text_input_both(self):
        assert is_applicable(Capability.TEXT_INPUT, SchemaType.CHAT_COMPLETIONS)
        assert is_applicable(Capability.TEXT_INPUT, SchemaType.RESPONSES)

    def test_file_input_inline_responses_only(self):
        assert is_applicable(Capability.FILE_INPUT_INLINE, SchemaType.RESPONSES)
        assert not is_applicable(Capability.FILE_INPUT_INLINE, SchemaType.CHAT_COMPLETIONS)

    def test_built_in_tools_responses_only(self):
        assert is_applicable(Capability.BUILT_IN_TOOLS, SchemaType.RESPONSES)
        assert not is_applicable(Capability.BUILT_IN_TOOLS, SchemaType.CHAT_COMPLETIONS)


class TestNormalizedModels:
    def test_normalized_response(self):
        r = NormalizedResponse(
            text="Hello",
            tool_calls=[NormalizedToolCall(id="tc1", name="func", arguments='{"a":1}')],
            finish_reason="stop",
            model="gpt-4o",
            usage=NormalizedUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
            response_id="resp-1",
        )
        assert r.text == "Hello"
        assert len(r.tool_calls) == 1
        assert r.tool_calls[0].name == "func"
        assert r.usage.total_tokens == 15

    def test_empty_normalized_response(self):
        r = NormalizedResponse()
        assert r.text is None
        assert r.tool_calls == []
        assert r.usage is None


class TestReportSummary:
    def test_default_values(self):
        s = ReportSummary()
        assert s.total == 0
        assert s.passed == 0
        assert s.failed == 0
