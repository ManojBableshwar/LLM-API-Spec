"""Responses schema adapter (/v1/responses)."""

from __future__ import annotations

import json
from typing import Any, AsyncIterator

import httpx

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import (
    NormalizedResponse,
    NormalizedToolCall,
    NormalizedUsage,
    SchemaType,
)


class ResponsesAdapter(SchemaAdapter):
    schema_type = SchemaType.RESPONSES

    def endpoint_path(self) -> str:
        return "/responses"

    def build_request(self, **kwargs: Any) -> dict[str, Any]:
        input_val = kwargs.get("input")
        if input_val is None:
            input_val = kwargs.get("prompt", "Hello")

        body: dict[str, Any] = {
            "model": self.target.model,
            "input": input_val,
        }

        optional_keys = [
            "tools",
            "tool_choice",
            "parallel_tool_calls",
            "text",
            "stream",
            "stop",
            "previous_response_id",
            "background",
            "include",
            "max_output_tokens",
            "temperature",
        ]
        for key in optional_keys:
            if key in kwargs:
                body[key] = kwargs[key]

        return body

    def parse_response(self, response_data: dict[str, Any]) -> dict[str, Any]:
        parsed: dict[str, Any] = {
            "id": response_data.get("id"),
            "model": response_data.get("model"),
            "object": response_data.get("object"),
            "status": response_data.get("status"),
        }

        output_items = response_data.get("output", [])
        text_parts: list[str] = []
        tool_calls: list[dict[str, Any]] = []

        for item in output_items:
            item_type = item.get("type")
            if item_type == "message":
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        text_parts.append(content.get("text", ""))
            elif item_type == "function_call":
                tool_calls.append(item)

        parsed["content"] = "\n".join(text_parts) if text_parts else None
        parsed["tool_calls"] = tool_calls if tool_calls else None
        parsed["usage"] = response_data.get("usage")
        return parsed

    def normalize(self, response_data: dict[str, Any]) -> NormalizedResponse:
        output_items = response_data.get("output", [])
        text_parts: list[str] = []
        tool_calls: list[NormalizedToolCall] = []

        for item in output_items:
            item_type = item.get("type")
            if item_type == "message":
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        text_parts.append(content.get("text", ""))
            elif item_type == "function_call":
                tool_calls.append(
                    NormalizedToolCall(
                        id=item.get("call_id") or item.get("id"),
                        name=item.get("name", ""),
                        arguments=item.get("arguments", "{}"),
                    )
                )

        usage = None
        raw_usage = response_data.get("usage")
        if raw_usage:
            usage = NormalizedUsage(
                prompt_tokens=raw_usage.get("input_tokens"),
                completion_tokens=raw_usage.get("output_tokens"),
                total_tokens=(raw_usage.get("input_tokens") or 0)
                + (raw_usage.get("output_tokens") or 0),
            )

        return NormalizedResponse(
            text="\n".join(text_parts) if text_parts else None,
            tool_calls=tool_calls,
            finish_reason=response_data.get("status"),
            model=response_data.get("model"),
            usage=usage,
            response_id=response_data.get("id"),
        )

    async def stream_response(
        self, request_body: dict[str, Any]
    ) -> AsyncIterator[dict[str, Any]]:
        request_body = {**request_body, "stream": True}
        client = await self.get_client()
        async with client.stream(
            "POST", self.endpoint_path(), json=request_body
        ) as response:
            response.raise_for_status()
            buffer = ""
            async for chunk in response.aiter_text():
                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("event: "):
                        continue
                    if line == "data: [DONE]":
                        return
                    if line.startswith("data: "):
                        data_str = line[6:]
                        try:
                            yield json.loads(data_str)
                        except json.JSONDecodeError:
                            continue

    async def retrieve_response(self, response_id: str) -> httpx.Response:
        client = await self.get_client()
        return await client.get(f"/responses/{response_id}")
