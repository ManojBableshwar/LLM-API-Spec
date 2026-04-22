"""File input capability checks."""

from __future__ import annotations

from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import CapabilityResult, Capability, SchemaType


async def check_file_input_inline(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint accepts inline file content."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.FILE_INPUT_INLINE,
    )

    # Responses schema only
    if adapter.schema_type != SchemaType.RESPONSES:
        result.supported = None
        result.details = "Not applicable for chat_completions schema"
        return result

    input_items = [
        {"type": "input_text", "text": "Summarize the content of the attached file."},
        {
            "type": "input_file",
            "file_data": "This is a test document with some sample content for verification.",
            "filename": "test.txt",
        },
    ]
    request_body = adapter.build_request(input=input_items, max_tokens=100)
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        if normalized.text and len(normalized.text.strip()) > 0:
            result.passed = True
            result.details = "Inline file input accepted and processed"
        else:
            result.passed = False
            result.details = "No response after inline file input"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Inline file input failed: {exc}"

    return result


async def check_file_input_reference(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint accepts file references."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.FILE_INPUT_REFERENCE,
    )

    if adapter.schema_type != SchemaType.RESPONSES:
        result.supported = None
        result.details = "Not applicable for chat_completions schema"
        return result

    input_items = [
        {"type": "input_text", "text": "Summarize the referenced file."},
        {
            "type": "input_file",
            "file_id": "file-test-reference-id",
        },
    ]
    request_body = adapter.build_request(input=input_items, max_tokens=100)
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        if normalized.text and len(normalized.text.strip()) > 0:
            result.passed = True
            result.details = "File reference accepted and processed"
        else:
            result.passed = False
            result.details = "No response after file reference input"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"File reference input failed: {exc}"

    return result
