"""Long context capability check."""

from __future__ import annotations

from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import CapabilityResult, Capability


async def check_long_prompt_acceptance(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint can handle long prompts."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.LONG_PROMPT_ACCEPTANCE,
    )

    # Generate a long prompt (~8000 tokens worth of text)
    filler = "The quick brown fox jumps over the lazy dog. " * 500
    prompt = f"The following is filler text. After reading it, say 'DONE'. {filler} Now say DONE."

    request_body = adapter.build_request(prompt=prompt, max_tokens=20)
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True
        result.passed = True
        result.details = f"Long prompt ({len(prompt)} chars) accepted"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Long prompt check failed: {exc}"

    return result
