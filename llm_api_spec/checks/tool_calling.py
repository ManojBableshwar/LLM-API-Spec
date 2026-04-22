"""Tool calling capability checks."""

from __future__ import annotations

import json
from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import CapabilityResult, Capability

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name",
                }
            },
            "required": ["location"],
        },
    },
}

CALCULATOR_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Perform a math calculation",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate",
                }
            },
            "required": ["expression"],
        },
    },
}


def _has_tool_calls(normalized) -> bool:
    return len(normalized.tool_calls) > 0


def _tool_call_is_valid(tc) -> bool:
    if not tc.name:
        return False
    try:
        json.loads(tc.arguments)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


async def check_tool_calling(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint can invoke tool calls."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.TOOL_CALLING,
    )

    request_body = adapter.build_request(
        prompt="What is the weather in San Francisco?",
        tools=[WEATHER_TOOL],
        max_tokens=200,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        if _has_tool_calls(normalized) and _tool_call_is_valid(normalized.tool_calls[0]):
            result.passed = True
            result.details = f"Tool call returned: {normalized.tool_calls[0].name}"
        else:
            result.passed = False
            result.details = "No valid tool call in response"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Tool calling check failed: {exc}"

    return result


async def check_tool_choice_auto(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify tool_choice='auto' works."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.TOOL_CHOICE_AUTO,
    )

    request_body = adapter.build_request(
        prompt="What is the weather in Tokyo?",
        tools=[WEATHER_TOOL],
        tool_choice="auto",
        max_tokens=200,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True
        result.passed = True
        result.details = "tool_choice='auto' accepted"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"tool_choice='auto' failed: {exc}"

    return result


async def check_tool_choice_none(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify tool_choice='none' suppresses tool calls."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.TOOL_CHOICE_NONE,
    )

    request_body = adapter.build_request(
        prompt="What is the weather in Tokyo?",
        tools=[WEATHER_TOOL],
        tool_choice="none",
        max_tokens=200,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        if not _has_tool_calls(normalized):
            result.passed = True
            result.details = "tool_choice='none' correctly suppressed tool calls"
        else:
            result.passed = False
            result.details = "tool_choice='none' did not suppress tool calls"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"tool_choice='none' failed: {exc}"

    return result


async def check_tool_choice_required(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify tool_choice='required' forces a tool call."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.TOOL_CHOICE_REQUIRED,
    )

    request_body = adapter.build_request(
        prompt="Say hello to me.",
        tools=[WEATHER_TOOL],
        tool_choice="required",
        max_tokens=200,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        if _has_tool_calls(normalized):
            result.passed = True
            result.details = "tool_choice='required' forced a tool call"
        else:
            result.passed = False
            result.details = "tool_choice='required' did not force a tool call"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"tool_choice='required' failed: {exc}"

    return result


async def check_tool_choice_function(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify tool_choice with a specific function name."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.TOOL_CHOICE_FUNCTION,
    )

    request_body = adapter.build_request(
        prompt="Say hello to me.",
        tools=[WEATHER_TOOL, CALCULATOR_TOOL],
        tool_choice={"type": "function", "function": {"name": "get_weather"}},
        max_tokens=200,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        if _has_tool_calls(normalized) and normalized.tool_calls[0].name == "get_weather":
            result.passed = True
            result.details = "tool_choice forced specific function 'get_weather'"
        elif _has_tool_calls(normalized):
            result.passed = False
            result.details = (
                f"Wrong function called: {normalized.tool_calls[0].name}"
            )
        else:
            result.passed = False
            result.details = "No tool call in response"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"tool_choice function failed: {exc}"

    return result


async def check_multiple_tool_calls(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint can return multiple tool calls."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.MULTIPLE_TOOL_CALLS,
    )

    request_body = adapter.build_request(
        prompt="What is the weather in Tokyo and also calculate 42 * 17?",
        tools=[WEATHER_TOOL, CALCULATOR_TOOL],
        max_tokens=300,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        if len(normalized.tool_calls) >= 2:
            result.passed = True
            result.details = f"Multiple tool calls returned: {len(normalized.tool_calls)}"
        else:
            result.passed = False
            result.details = f"Expected >=2 tool calls, got {len(normalized.tool_calls)}"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Multiple tool calls check failed: {exc}"

    return result


async def check_parallel_tool_calls(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the parallel_tool_calls parameter is respected."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.PARALLEL_TOOL_CALLS,
    )

    # First test with parallel enabled
    request_body = adapter.build_request(
        prompt="What is the weather in Tokyo and calculate 42 * 17?",
        tools=[WEATHER_TOOL, CALCULATOR_TOOL],
        parallel_tool_calls=True,
        max_tokens=300,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True
        result.passed = True
        result.details = "parallel_tool_calls parameter accepted"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"parallel_tool_calls check failed: {exc}"

    return result
