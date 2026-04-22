"""Basic text input/output capability checks."""

from __future__ import annotations

from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import CapabilityResult, Capability, SchemaType


async def check_text_input(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint accepts plain text input."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.TEXT_INPUT,
    )

    request_body = adapter.build_request(prompt="Say hello.", max_tokens=50)
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True
        result.passed = True
        result.details = "Text input accepted and processed"
    except Exception as exc:
        result.supported = False
        result.passed = None
        result.errors.append(str(exc))
        result.details = f"Text input failed: {exc}"

    return result


async def check_text_output(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint returns text content."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.TEXT_OUTPUT,
    )

    request_body = adapter.build_request(prompt="Say hello.", max_tokens=50)
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        if normalized.text and len(normalized.text.strip()) > 0:
            result.passed = True
            result.details = "Response contains text content"
        else:
            result.passed = False
            result.details = "Response does not contain text content"
    except Exception as exc:
        result.supported = False
        result.passed = None
        result.errors.append(str(exc))
        result.details = f"Text output check failed: {exc}"

    return result


async def check_stop_sequences(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint respects stop sequences."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.STOP_SEQUENCES,
    )

    stop_word = "STOPNOW"
    prompt = f"Count from 1 to 20. After the number 5, write the word {stop_word} then continue."
    request_body = adapter.build_request(
        prompt=prompt,
        stop=[stop_word],
        max_tokens=200,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        text = normalized.text or ""
        if stop_word not in text:
            result.passed = True
            result.details = "Stop sequence was respected"
        else:
            result.passed = False
            result.details = f"Stop sequence '{stop_word}' appeared in output"
    except Exception as exc:
        result.supported = False
        result.passed = None
        result.errors.append(str(exc))
        result.details = f"Stop sequence check failed: {exc}"

    return result
