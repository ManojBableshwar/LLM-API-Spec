"""Multimodal (image) capability checks."""

from __future__ import annotations

import base64
from typing import Any

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import CapabilityResult, Capability, SchemaType

# 8x8 red PNG — small but valid enough for all providers.
# The 1x1 pixel PNG is rejected by some APIs as too small/invalid.
TINY_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAA"
    "EklEQVR4nGP4z8DwHx9mGBkKAMLXf4EvceABAAAAAElFTkSuQmCC"
)

# Use a data URI so the image_url test doesn't depend on external hosting.
# The real purpose is verifying the endpoint accepts image_url content parts,
# not that it can fetch a remote resource.
SAMPLE_IMAGE_URL = f"data:image/png;base64,{TINY_PNG_B64}"


def _build_image_url_messages(prompt: str, url: str) -> list[dict]:
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": url}},
            ],
        }
    ]


def _build_image_b64_messages(prompt: str, b64: str) -> list[dict]:
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{b64}"},
                },
            ],
        }
    ]


def _build_responses_image_url_input(prompt: str, url: str) -> list[dict]:
    return [
        {"type": "input_text", "text": prompt},
        {"type": "input_image", "image_url": url},
    ]


def _build_responses_image_b64_input(prompt: str, b64: str) -> list[dict]:
    return [
        {"type": "input_text", "text": prompt},
        {"type": "input_image", "image_url": f"data:image/png;base64,{b64}"},
    ]


async def check_image_input_url(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint accepts an image URL."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.IMAGE_INPUT_URL,
    )

    if adapter.schema_type == SchemaType.CHAT_COMPLETIONS:
        request_body = adapter.build_request(
            messages=_build_image_url_messages("Describe this image briefly.", SAMPLE_IMAGE_URL),
            max_tokens=100,
        )
    else:
        request_body = adapter.build_request(
            input=_build_responses_image_url_input("Describe this image briefly.", SAMPLE_IMAGE_URL),
            max_tokens=100,
        )

    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        if normalized.text and len(normalized.text.strip()) > 0:
            result.passed = True
            result.details = "Image URL accepted and processed"
        else:
            result.passed = False
            result.details = "No text response after image URL input"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Image URL input failed: {exc}"

    return result


async def check_image_input_base64(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint accepts a base64 image."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.IMAGE_INPUT_BASE64,
    )

    if adapter.schema_type == SchemaType.CHAT_COMPLETIONS:
        request_body = adapter.build_request(
            messages=_build_image_b64_messages("Describe this image briefly.", TINY_PNG_B64),
            max_tokens=100,
        )
    else:
        request_body = adapter.build_request(
            input=_build_responses_image_b64_input("Describe this image briefly.", TINY_PNG_B64),
            max_tokens=100,
        )

    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        normalized = adapter.normalize(raw)
        if normalized.text and len(normalized.text.strip()) > 0:
            result.passed = True
            result.details = "Base64 image accepted and processed"
        else:
            result.passed = False
            result.details = "No text response after base64 image input"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Base64 image input failed: {exc}"

    return result


async def check_image_input_multi(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint accepts multiple images."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.IMAGE_INPUT_MULTI,
    )

    if adapter.schema_type == SchemaType.CHAT_COMPLETIONS:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Compare these two images briefly."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{TINY_PNG_B64}"}},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{TINY_PNG_B64}"}},
                ],
            }
        ]
        request_body = adapter.build_request(messages=messages, max_tokens=100)
    else:
        input_items = [
            {"type": "input_text", "text": "Compare these two images briefly."},
            {"type": "input_image", "image_url": f"data:image/png;base64,{TINY_PNG_B64}"},
            {"type": "input_image", "image_url": f"data:image/png;base64,{TINY_PNG_B64}"},
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
            result.details = "Multiple images accepted and processed"
        else:
            result.passed = False
            result.details = "No text response after multi-image input"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Multi-image input failed: {exc}"

    return result


async def check_image_output(adapter: SchemaAdapter) -> CapabilityResult:
    """Verify the endpoint can generate images."""
    result = CapabilityResult(
        target=adapter.target.name,
        schema=adapter.schema_type,
        capability=Capability.IMAGE_OUTPUT,
    )

    request_body = adapter.build_request(
        prompt="Generate a simple image of a red circle on a white background.",
        max_tokens=500,
    )
    result.raw_request = request_body

    try:
        raw, parsed = await adapter.send_and_parse(request_body)
        result.raw_response = raw
        result.supported = True

        # Check for image content in the output
        output_items = raw.get("output", raw.get("choices", []))
        has_image = False
        for item in output_items if isinstance(output_items, list) else []:
            if isinstance(item, dict):
                item_type = item.get("type", "")
                if "image" in item_type:
                    has_image = True
                    break
                content = item.get("message", {}).get("content", "")
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and "image" in c.get("type", ""):
                            has_image = True
                            break

        if has_image:
            result.passed = True
            result.details = "Image output generated"
        else:
            # Model responded successfully but with text only — it doesn't
            # support native image generation, so mark as unsupported rather
            # than failed.
            result.supported = False
            result.details = "Model does not support native image output"
    except Exception as exc:
        result.supported = False
        result.errors.append(str(exc))
        result.details = f"Image output check failed: {exc}"

    return result
