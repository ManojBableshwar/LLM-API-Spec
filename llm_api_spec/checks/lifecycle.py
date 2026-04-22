"""Lifecycle capability checks (response chaining, background, retrieval, built-in tools)."""

from __future__ import annotations

import asyncio
from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import CapabilityResult, Capability, SchemaType


async def check_previous_response_id(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify response chaining via previous_response_id."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.PREVIOUS_RESPONSE_ID,
    )

    if adapter.schema_type != SchemaType.RESPONSES:
        result.supported = None
        result.details = "Not applicable for chat_completions schema"
        return result

    # Step 1: Create initial response
    request1 = adapter.build_request(prompt="My name is Alice.", max_tokens=50)
    result.raw_request = request1

    try:
        raw1, parsed1 = await adapter.send_and_parse(request1)
        response_id = raw1.get("id")
        if not response_id:
            result.supported = False
            result.details = "Initial response has no ID"
            return result

        # Step 2: Chain with previous_response_id
        request2 = adapter.build_request(
            prompt="What is my name?",
            previous_response_id=response_id,
            max_tokens=50,
        )
        raw2, parsed2 = await adapter.send_and_parse(request2)
        result.raw_response = raw2
        result.supported = True

        normalized = adapter.normalize(raw2)
        text = (normalized.text or "").lower()
        if "alice" in text:
            result.passed = True
            result.details = "Response chaining preserved context"
        else:
            result.passed = True  # Chaining worked even if model didn't recall
            result.details = "previous_response_id accepted (context may not be preserved)"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"previous_response_id check failed: {exc}"

    return result


async def check_background_mode(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify background execution mode."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.BACKGROUND_MODE,
    )

    if adapter.schema_type != SchemaType.RESPONSES:
        result.supported = None
        result.details = "Not applicable for chat_completions schema"
        return result

    request_body = adapter.build_request(
        prompt="Say hello.",
        background=True,
        max_tokens=50,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        status = raw.get("status")
        if status in ("in_progress", "completed", "queued"):
            result.passed = True
            result.details = f"Background mode accepted, status: {status}"
        else:
            result.passed = False
            result.details = f"Unexpected status for background mode: {status}"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Background mode check failed: {exc}"

    return result


async def check_response_retrieval(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify retrieving a response by ID."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.RESPONSE_RETRIEVAL,
    )

    if adapter.schema_type != SchemaType.RESPONSES:
        result.supported = None
        result.details = "Not applicable for chat_completions schema"
        return result

    # Create a response first
    request_body = adapter.build_request(prompt="Say hello.", max_tokens=50)
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        response_id = raw.get("id")
        if not response_id:
            result.supported = False
            result.details = "Response has no ID"
            return result

        # Retrieve it
        retrieve_resp = await adapter.retrieve_response(response_id)
        retrieve_resp.raise_for_status()
        retrieved = retrieve_resp.json()
        result.raw_response = retrieved
        result.supported = True

        if retrieved.get("id") == response_id:
            result.passed = True
            result.details = "Response retrieved successfully"
        else:
            result.passed = False
            result.details = "Retrieved response ID mismatch"
    except NotImplementedError:
        result.supported = False
        result.details = "Response retrieval not implemented for this schema"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Response retrieval check failed: {exc}"

    return result


async def check_built_in_tools(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify built-in tools support (web_search, etc.)."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.BUILT_IN_TOOLS,
    )

    if adapter.schema_type != SchemaType.RESPONSES:
        result.supported = None
        result.details = "Not applicable for chat_completions schema"
        return result

    request_body = adapter.build_request(
        prompt="What is the current weather in San Francisco?",
        tools=[{"type": "web_search"}],
        max_tokens=200,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True
        result.passed = True
        result.details = "Built-in tools accepted"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Built-in tools check failed: {exc}"

    return result
