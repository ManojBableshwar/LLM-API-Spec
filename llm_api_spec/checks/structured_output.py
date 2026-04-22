"""Structured output capability checks."""

from __future__ import annotations

import json
import re
from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import CapabilityResult, Capability, SchemaType


async def check_json_output(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint can produce valid JSON output."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.JSON_OUTPUT,
    )

    if adapter.schema_type == SchemaType.CHAT_COMPLETIONS:
        request_body = adapter.build_request(
            prompt='Return a JSON object with keys "name" and "age". Only output JSON.',
            response_format={"type": "json_object"},
            max_tokens=100,
        )
    else:
        request_body = adapter.build_request(
            prompt='Return a JSON object with keys "name" and "age". Only output JSON.',
            text={"format": {"type": "json_object"}},
            max_tokens=100,
        )

    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        text = normalized.text or ""
        try:
            json.loads(text)
            result.passed = True
            result.details = "Response is valid JSON"
        except json.JSONDecodeError:
            result.passed = False
            result.details = "Response is not valid JSON"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"JSON output check failed: {exc}"

    return result


PERSON_SCHEMA = {
    "name": "person",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "city": {"type": "string"},
        },
        "required": ["name", "age", "city"],
        "additionalProperties": False,
    },
}


async def check_structured_output(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint can enforce a JSON schema on output."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.STRUCTURED_OUTPUT,
    )

    if adapter.schema_type == SchemaType.CHAT_COMPLETIONS:
        request_body = adapter.build_request(
            prompt="Generate a person with name, age, and city.",
            response_format={
                "type": "json_schema",
                "json_schema": PERSON_SCHEMA,
            },
            max_tokens=150,
        )
    else:
        request_body = adapter.build_request(
            prompt="Generate a person with name, age, and city.",
            text={
                "format": {
                    "type": "json_schema",
                    "json_schema": PERSON_SCHEMA,
                }
            },
            max_tokens=150,
        )

    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        text = normalized.text or ""
        try:
            data = json.loads(text)
            required_keys = {"name", "age", "city"}
            if required_keys.issubset(data.keys()):
                result.passed = True
                result.details = "Output conforms to JSON schema"
            else:
                result.passed = False
                missing = required_keys - set(data.keys())
                result.details = f"Missing keys: {missing}"
        except json.JSONDecodeError:
            result.passed = False
            result.details = "Output is not valid JSON"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Structured output check failed: {exc}"

    return result


async def check_json_schema_constraints(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify JSON schema constraint enforcement (similar to structured_output)."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.JSON_SCHEMA_CONSTRAINTS,
    )

    color_schema = {
        "name": "color",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "color": {"type": "string", "enum": ["red", "green", "blue"]},
                "hex": {"type": "string"},
            },
            "required": ["color", "hex"],
            "additionalProperties": False,
        },
    }

    if adapter.schema_type == SchemaType.CHAT_COMPLETIONS:
        request_body = adapter.build_request(
            prompt="Pick a color and provide its hex code.",
            response_format={
                "type": "json_schema",
                "json_schema": color_schema,
            },
            max_tokens=100,
        )
    else:
        request_body = adapter.build_request(
            prompt="Pick a color and provide its hex code.",
            text={
                "format": {
                    "type": "json_schema",
                    "json_schema": color_schema,
                }
            },
            max_tokens=100,
        )

    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        text = normalized.text or ""
        try:
            data = json.loads(text)
            if data.get("color") in ("red", "green", "blue") and "hex" in data:
                result.passed = True
                result.details = "JSON schema constraint enforced correctly"
            else:
                result.passed = False
                result.details = f"Schema constraint violated: {data}"
        except json.JSONDecodeError:
            result.passed = False
            result.details = "Output is not valid JSON"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"JSON schema constraints check failed: {exc}"

    return result


async def check_regex_constraints(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint can constrain output to a regex pattern."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.REGEX_CONSTRAINTS,
    )

    pattern = r"^\d{3}-\d{2}-\d{4}$"

    if adapter.schema_type == SchemaType.CHAT_COMPLETIONS:
        request_body = adapter.build_request(
            prompt="Generate a number in the format XXX-XX-XXXX (like 123-45-6789). Output ONLY the number.",
            response_format={"type": "text", "pattern": pattern},
            max_tokens=50,
        )
    else:
        request_body = adapter.build_request(
            prompt="Generate a number in the format XXX-XX-XXXX (like 123-45-6789). Output ONLY the number.",
            text={"format": {"type": "text", "pattern": pattern}},
            max_tokens=50,
        )

    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        text = (normalized.text or "").strip()
        if re.match(pattern, text):
            result.passed = True
            result.details = f"Output matches regex: {text}"
        else:
            result.passed = False
            result.details = f"Output does not match regex: {text!r}"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Regex constraints check failed: {exc}"

    return result


async def check_grammar_constraints(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint can constrain output using a formal grammar."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.GRAMMAR_CONSTRAINTS,
    )

    # Use a simple GBNF-like grammar for yes/no
    grammar = 'root ::= "yes" | "no"'

    if adapter.schema_type == SchemaType.CHAT_COMPLETIONS:
        request_body = adapter.build_request(
            prompt="Is the sky blue? Answer yes or no only.",
            response_format={"type": "grammar", "grammar": grammar},
            max_tokens=10,
        )
    else:
        request_body = adapter.build_request(
            prompt="Is the sky blue? Answer yes or no only.",
            text={"format": {"type": "grammar", "grammar": grammar}},
            max_tokens=10,
        )

    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        text = (normalized.text or "").strip().lower()
        if text in ("yes", "no"):
            result.passed = True
            result.details = f"Grammar constraint produced valid output: {text}"
        else:
            result.passed = False
            result.details = f"Grammar constraint output not matching: {text!r}"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Grammar constraints check failed: {exc}"

    return result
