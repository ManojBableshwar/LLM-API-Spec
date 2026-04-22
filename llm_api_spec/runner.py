"""Validation runner — orchestrates capability checks across targets and schemas."""

from __future__ import annotations

import asyncio
from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.adapters.chat_completions import ChatCompletionsAdapter
from llm_api_spec.adapters.responses import ResponsesAdapter
from llm_api_spec.checks import CAPABILITY_CHECK_MAP
from llm_api_spec.models import (
    Capability,
    CapabilityResult,
    EndpointTarget,
    SchemaType,
    is_applicable,
)
from llm_api_spec.openapi_validation import OpenAPIValidator


def get_adapter(target: EndpointTarget, schema: SchemaType, *, debug: bool = False) -> SchemaAdapter:
    if schema == SchemaType.CHAT_COMPLETIONS:
        return ChatCompletionsAdapter(target, debug=debug)
    elif schema == SchemaType.RESPONSES:
        return ResponsesAdapter(target, debug=debug)
    raise ValueError(f"Unknown schema type: {schema}")


async def run_capability_check(
    adapter: SchemaAdapter,
    capability: Capability,
    openapi_validator: OpenAPIValidator | None = None,
) -> CapabilityResult:
    """Run a single capability check."""
    if not is_applicable(capability, adapter.schema_type):
        return CapabilityResult(
            target=adapter.target.name,
            schema=adapter.schema_type,
            capability=capability,
            supported=None,
            details="Not applicable for this schema",
        )

    check_fn = CAPABILITY_CHECK_MAP.get(capability)
    if check_fn is None:
        return CapabilityResult(
            target=adapter.target.name,
            schema=adapter.schema_type,
            capability=capability,
            supported=None,
            details=f"No check implemented for {capability.value}",
        )

    result = await check_fn(adapter)

    # Apply OpenAPI validation if enabled
    if openapi_validator and openapi_validator.is_loaded:
        if result.raw_request:
            is_valid, errors = openapi_validator.validate_request(result.raw_request)
            result.request_schema_valid = is_valid
            if errors:
                result.errors.extend(errors)

        if result.raw_response:
            is_valid, errors = openapi_validator.validate_response(result.raw_response)
            result.response_schema_valid = is_valid
            if errors:
                result.errors.extend(errors)

    return result


async def run_schema_checks(
    target: EndpointTarget,
    schema: SchemaType,
    capabilities: list[Capability] | None = None,
    openapi_validation: bool = False,
    openapi_spec_path: str | None = None,
    verbose: bool = False,
    debug: bool = False,
) -> list[CapabilityResult]:
    """Run all capability checks for a target+schema combination."""
    adapter = get_adapter(target, schema, debug=debug)
    results: list[CapabilityResult] = []

    openapi_validator = None
    if openapi_validation:
        openapi_validator = OpenAPIValidator(schema, openapi_spec_path)

    caps = capabilities or list(Capability)

    try:
        for cap in caps:
            if verbose:
                print(f"  Checking {cap.value}...")
            result = await run_capability_check(adapter, cap, openapi_validator)
            results.append(result)
            if verbose:
                print(f"    -> {result.status}: {result.details}")
    finally:
        await adapter.close()

    return results


async def run_all_checks(
    targets: list[EndpointTarget],
    capabilities: list[Capability] | None = None,
    openapi_validation: bool = False,
    openapi_spec_path: str | None = None,
    verbose: bool = False,
    debug: bool = False,
) -> list[CapabilityResult]:
    """Run all capability checks for all targets and schemas."""
    all_results: list[CapabilityResult] = []

    for target in targets:
        if verbose:
            print(f"\nTarget: {target.name} ({target.base_url})")

        for schema in target.schemas:
            if verbose:
                print(f"\n Schema: {schema.value}")

            results = await run_schema_checks(
                target=target,
                schema=schema,
                capabilities=capabilities,
                openapi_validation=openapi_validation,
                openapi_spec_path=openapi_spec_path,
                verbose=verbose,
                debug=debug,
            )
            all_results.extend(results)

    return all_results
