"""Tests for the runner module."""

from __future__ import annotations

import httpx
import pytest
import respx

from llm_api_spec.models import Capability, EndpointTarget, SchemaType
from llm_api_spec.runner import run_capability_check, run_schema_checks, get_adapter
from llm_api_spec.adapters.chat_completions import ChatCompletionsAdapter
from llm_api_spec.adapters.responses import ResponsesAdapter
from tests.conftest import make_chat_response


@pytest.fixture
def target():
    return EndpointTarget(
        name="runner-test",
        base_url="https://runner-mock.test/v1",
        api_key="key",
        model="model",
        schemas=[SchemaType.CHAT_COMPLETIONS],
    )


class TestGetAdapter:
    def test_chat_completions(self, target):
        adapter = get_adapter(target, SchemaType.CHAT_COMPLETIONS)
        assert isinstance(adapter, ChatCompletionsAdapter)

    def test_responses(self, target):
        adapter = get_adapter(target, SchemaType.RESPONSES)
        assert isinstance(adapter, ResponsesAdapter)

    def test_invalid_schema(self, target):
        with pytest.raises(ValueError):
            get_adapter(target, "invalid")


class TestRunCapabilityCheck:
    @respx.mock
    @pytest.mark.asyncio
    async def test_not_applicable(self, target):
        adapter = ChatCompletionsAdapter(target)
        try:
            result = await run_capability_check(
                adapter, Capability.PREVIOUS_RESPONSE_ID
            )
            assert result.status == "not_applicable"
        finally:
            await adapter.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_successful_check(self, target):
        respx.post("https://runner-mock.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=make_chat_response(content="OK"))
        )
        adapter = ChatCompletionsAdapter(target)
        try:
            result = await run_capability_check(adapter, Capability.TEXT_INPUT)
            assert result.supported is True
            assert result.passed is True
        finally:
            await adapter.close()


class TestRunSchemaChecks:
    @respx.mock
    @pytest.mark.asyncio
    async def test_run_specific_capabilities(self, target):
        respx.post("https://runner-mock.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=make_chat_response(content="OK"))
        )
        results = await run_schema_checks(
            target,
            SchemaType.CHAT_COMPLETIONS,
            capabilities=[Capability.TEXT_INPUT, Capability.TEXT_OUTPUT],
        )
        assert len(results) == 2
        assert all(r.target == "runner-test" for r in results)
