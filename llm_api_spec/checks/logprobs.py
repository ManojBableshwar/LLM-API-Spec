"""Logprobs capability check."""

from __future__ import annotations

from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import CapabilityResult, Capability, SchemaType


async def check_logprobs(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint can return log probabilities."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.LOGPROBS,
    )

    if adapter.schema_type != SchemaType.CHAT_COMPLETIONS:
        result.supported = None
        result.details = "Not applicable for responses schema"
        return result

    request_body = adapter.build_request(
        prompt="Say hello.",
        logprobs=True,
        top_logprobs=3,
        max_tokens=50,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        choices = raw.get("choices", [])
        if choices:
            logprobs_data = choices[0].get("logprobs")
            if logprobs_data and logprobs_data.get("content"):
                result.passed = True
                result.details = "Logprobs returned with token data"
            else:
                result.passed = False
                result.details = "No logprobs data in response"
        else:
            result.passed = False
            result.details = "No choices in response"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Logprobs check failed: {exc}"

    return result
