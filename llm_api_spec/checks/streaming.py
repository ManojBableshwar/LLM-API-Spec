"""Streaming capability check."""

from __future__ import annotations

from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import CapabilityResult, Capability


async def check_streaming(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint supports streaming responses."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.STREAMING,
    )

    request_body = adapter.build_request(prompt="Count from 1 to 5.", max_tokens=100)
    result.raw_request = request_body

    try:
        chunks: list[dict[str, Any]] = []
        async for chunk in adapter.stream_response(request_body):
            chunks.append(chunk)
            if len(chunks) > 100:
                break

        result.supported = True
        if len(chunks) > 0:
            result.passed = True
            result.details = f"Streaming produced {len(chunks)} chunks"
        else:
            result.passed = False
            result.details = "Streaming produced no chunks"
        result.raw_response = {"chunks_count": len(chunks), "first_chunk": chunks[0] if chunks else None}
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Streaming check failed: {exc}"

    return result
