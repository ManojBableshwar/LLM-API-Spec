"""Seeded determinism capability check."""

from __future__ import annotations

from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import CapabilityResult, Capability


async def check_seeded_determinism(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint produces deterministic output with seed."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.SEEDED_DETERMINISM,
    )

    seed = 42
    request_body = adapter.build_request(
        prompt="What is 2 + 2? Answer with just the number.",
        seed=seed,
        max_tokens=10,
        temperature=0,
    )
    result.raw_request = request_body

    try:
        raw1, parsed1 = await adapter.send_and_parse(request_body)
        raw2, parsed2 = await adapter.send_and_parse(request_body)

        result.supported = True

        norm1 = adapter.normalize(raw1)
        norm2 = adapter.normalize(raw2)
        text1 = (norm1.text or "").strip()
        text2 = (norm2.text or "").strip()

        if text1 == text2:
            result.passed = True
            result.details = f"Deterministic output with seed={seed}: {text1!r}"
        else:
            result.passed = False
            result.details = f"Non-deterministic: {text1!r} vs {text2!r}"

        result.raw_response = {"response_1": raw1, "response_2": raw2}
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Determinism check failed: {exc}"

    return result
