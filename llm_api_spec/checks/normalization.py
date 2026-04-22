"""Normalization capability check."""

from __future__ import annotations

from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import CapabilityResult, Capability


async def check_normalization(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the response can be normalized to canonical form."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.NORMALIZATION,
    )

    request_body = adapter.build_request(prompt="Say hello.", max_tokens=50)
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        try:
            normalized = adapter.normalize(raw)
            result.normalized_response = normalized.model_dump()
            result.normalized = True
            result.passed = True
            result.details = "Response successfully normalized"
        except Exception as norm_exc:
            result.normalized = False
            result.passed = False
            result.details = f"Normalization failed: {norm_exc}"
            result.errors.append(str(norm_exc))
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Normalization check failed: {exc}"

    return result
